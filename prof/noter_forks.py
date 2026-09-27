"""Note automatiquement tous les forks de l'atelier et produit prof/notes.csv.

À lancer depuis un Codespace ouvert sur le dépôt de l'enseignant :
    python prof/noter_forks.py                     # tous les forks
    python prof/noter_forks.py --etudiant pseudo   # un seul étudiant
    python prof/noter_forks.py --sans-docker       # plus rapide, sans vérifier Docker

Pour chaque fork, le script clone le dépôt de l'étudiant, remplace le vérificateur et le
générateur de données par ceux de l'enseignant (un étudiant ne peut donc pas les truquer),
puis calcule la note. Le détail de chaque correction est écrit dans prof/_forks/<pseudo>.txt.

⚠️ Ce script exécute le code des étudiants : lancez-le dans un Codespace, pas sur votre ordinateur.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))
from verif.outils import DEPOT_ENSEIGNANT, api_github  # noqa: E402

DOSSIER = RACINE / "prof" / "_forks"
FICHIER_NOTES = RACINE / "prof" / "notes.csv"


def lister_forks(depot):
    forks, page = [], 1
    while True:
        lot = api_github(f"/repos/{depot}/forks?per_page=100&page={page}")
        if not lot:
            return forks
        forks += lot
        page += 1


def nom_etudiant(dossier):
    rendu = dossier / "RENDU.md"
    if rendu.exists():
        m = re.search(r"^\|\s*0\.1\s*\|[^|]*\|(.*)\|\s*$", rendu.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip()
    return ""


def noter(nom_complet, url_clone, sans_docker=False):
    pseudo = nom_complet.split("/")[0]
    cible = DOSSIER / pseudo
    shutil.rmtree(cible, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", url_clone, str(cible)], check=True, timeout=600)

    # Outils de l'enseignant : ils écrasent ceux du fork
    shutil.rmtree(cible / "verif", ignore_errors=True)
    shutil.copytree(RACINE / "verif", cible / "verif", ignore=shutil.ignore_patterns("__pycache__"))
    for fichier in ("scripts/generer_donnees.py", "pytest.ini"):
        (cible / fichier).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(RACINE / fichier, cible / fichier)

    env = {**os.environ, "VERIF_MODE": "prof", "VERIF_DEPOT": nom_complet, "NO_COLOR": "1",
           "MLFLOW_DISABLE_AGENT_HINT": "1"}
    if sans_docker:
        env["VERIF_SANS_DOCKER"] = "1"
    subprocess.run([sys.executable, "scripts/generer_donnees.py"], cwd=cible, env=env, capture_output=True)
    resultat = cible / "note.json"
    execution = subprocess.run([sys.executable, "-m", "verif", "note", "--json", str(resultat)],
                               cwd=cible, env=env, capture_output=True, text=True, timeout=3600)
    (DOSSIER / f"{pseudo}.txt").write_text(execution.stdout + execution.stderr, encoding="utf-8")
    if not resultat.exists():
        raise RuntimeError(f"le vérificateur a échoué, voir prof/_forks/{pseudo}.txt")
    note = json.loads(resultat.read_text())
    note["nom"] = nom_etudiant(cible)
    return note


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--depot", default=DEPOT_ENSEIGNANT, help="dépôt de l'enseignant")
    parser.add_argument("--etudiant", help="ne noter que le fork de ce pseudo GitHub")
    parser.add_argument("--sans-docker", action="store_true", help="ne pas reconstruire les images Docker")
    args = parser.parse_args()

    DOSSIER.mkdir(parents=True, exist_ok=True)
    forks = lister_forks(args.depot)
    if args.etudiant:
        forks = [f for f in forks if f["owner"]["login"].lower() == args.etudiant.lower()]
    if not forks:
        qui = f"de l'étudiant « {args.etudiant} »" if args.etudiant else "d'étudiant"
        print(f"Aucun fork {qui} trouvé sur https://github.com/{args.depot}/forks")
        print("Vérifiez que l'étudiant a bien fait un Fork (et non une copie ou un dépôt privé).")
        sys.exit(1)
    print(f"{len(forks)} fork(s) à noter\n")

    lignes = []
    for i, fork in enumerate(forks, 1):
        nom_complet = fork["full_name"]
        print(f"[{i}/{len(forks)}] {nom_complet} ...", end=" ", flush=True)
        try:
            note = noter(nom_complet, fork["clone_url"], args.sans_docker)
            print(f"{note['total']:g} / {note['maximum']:g}   {note['nom']}")
            lignes.append({"pseudo_github": fork["owner"]["login"], "nom": note["nom"],
                           "depot": fork["html_url"],
                           **{f"atelier_{k}": v for k, v in note["ateliers"].items() if k != "0"},
                           "total_auto_sur_17": note["total"],
                           "manuel_sur_3": "", "note_sur_20": ""})
        except Exception as e:
            print(f"ERREUR : {e}")
            lignes.append({"pseudo_github": fork["owner"]["login"], "depot": fork["html_url"],
                           "nom": f"ERREUR : {e}"})

    if lignes:
        colonnes = list(dict.fromkeys(k for ligne in lignes for k in ligne))
        with open(FICHIER_NOTES, "w", newline="", encoding="utf-8-sig") as f:
            ecrivain = csv.DictWriter(f, fieldnames=colonnes, delimiter=";")
            ecrivain.writeheader()
            ecrivain.writerows(lignes)
        print(f"\nNotes enregistrées dans {FICHIER_NOTES.relative_to(RACINE)} (ouvrable avec Excel)")
        print(f"Détail de chaque correction : {DOSSIER.relative_to(RACINE)}/<pseudo>.txt")


if __name__ == "__main__":
    main()
