"""Point d'entrée :  python -m verif <numéro d'atelier | tout | note> [--json fichier]"""
import json
import os
import sys
import warnings

from verif.outils import RACINE, Atelier, fmt, gras, vert

NB_ATELIERS = 5

AIDE = """Utilisation :
  ./verifier.sh 0      vérifie l'atelier 0 (de 0 à 4)
  ./verifier.sh tout   vérifie tous les ateliers et affiche votre note sur 20

Pour l'enseignant (depuis un Codespace ouvert sur le dépôt d'origine) :
  ./verifier.sh etudiants          corrige tous les forks et crée prof/notes.csv
  ./verifier.sh etudiant <pseudo>  corrige le fork d'un étudiant et affiche le détail
"""

def executer(numero):
    from verif.ateliers import ATELIERS, BAREME
    try:
        return ATELIERS[numero]()
    except Exception as e:  # le vérificateur ne doit jamais planter
        a = Atelier(numero, "Erreur", BAREME[numero])
        a.ko(f"Erreur inattendue pendant la vérification : {e!r}", points_max=a.bareme)
        return a


def resume_markdown(ateliers, total, maximum):
    lignes = ["## Note automatique de l'atelier DataOps", "",
              "| Atelier | Points | Détail |", "|---|---|---|"]
    for a in ateliers:
        details = "<br>".join(("✅ " if s == "ok" else "❌ " if s == "ko" else "ℹ️ ") + m
                              for s, m, *_ in a.lignes)
        lignes.append(f"| {a.numero}. {a.titre} | {fmt(a.points)} / {fmt(a.bareme)} | {details} |")
    lignes += ["", f"**Note : {fmt(total)} / {fmt(maximum)}**"]
    return "\n".join(lignes)


def main(argv):
    warnings.filterwarnings("ignore")
    os.chdir(RACINE)
    sys.path.insert(0, str(RACINE))

    cible = argv[0] if argv else "aide"
    if cible.isdigit() and int(cible) in range(NB_ATELIERS):
        a = executer(int(cible))
        a.afficher()
        return 0
    if cible not in ("tout", "note"):
        print(AIDE)
        return 0

    ateliers = []
    for n in range(NB_ATELIERS):
        a = executer(n)
        a.afficher()
        ateliers.append(a)
    total = sum(a.points for a in ateliers)
    maximum = sum(a.bareme for a in ateliers)

    print()
    print(gras("━━━ Récapitulatif ━━━"))
    for a in ateliers:
        etat = vert("validé") if a.reussi else "à terminer"
        bareme = f"{fmt(a.points):>4} / {fmt(a.bareme)}" if a.bareme else "   —    "
        print(f"  Atelier {a.numero}  {a.titre:32} {bareme}   {etat}")
    print(gras(f"\n  Note : {fmt(total)} / {fmt(maximum)}"))

    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(resume_markdown(ateliers, total, maximum) + "\n")
    if "--json" in argv:
        chemin = argv[argv.index("--json") + 1]
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump({"total": total, "maximum": maximum,
                       "ateliers": {a.numero: a.points for a in ateliers}}, f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
