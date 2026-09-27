"""Vérifications de chaque atelier. Chaque fonction renvoie un objet Atelier."""
import importlib
import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

from verif.outils import (ATTENDUS, DEPOT_ENSEIGNANT, RACINE, Atelier, api_github, depot_github,
                          derniere_erreur, empreinte, fmt, git, lancer, lire_rendu, mode_ci,
                          mode_prof, nombre)

DONNEES = RACINE / "data" / "raw" / "ventes.csv"
DONNEES_PROD = RACINE / "data" / "raw" / "ventes_prod.csv"
PREUVE_MLFLOW = RACINE / "preuves" / "mlflow_runs.json"
MODELE = RACINE / "modeles" / "modele.joblib"


def charger(module):
    """Importe (ou ré-importe) un module de l'étudiant."""
    if module in sys.modules:
        return importlib.reload(sys.modules[module])
    return importlib.import_module(module)


def entrainer_dans_dossier_temporaire(tmp, C="0.5", exporter=False):
    """Lance src.train dans un dossier temporaire, pour ne pas polluer le MLflow de l'étudiant."""
    tmp = Path(tmp)
    if not (tmp / "data").exists():
        (tmp / "data").symlink_to(RACINE / "data")
    uri = f"sqlite:///{tmp}/verif.db"
    commande = [sys.executable, "-m", "src.train", "--C", C] + (["--exporter"] if exporter else [])
    env = {**os.environ, "MLFLOW_TRACKING_URI": uri, "PYTHONPATH": str(RACINE),
           "MLFLOW_DISABLE_AGENT_HINT": "1"}
    import subprocess
    try:
        r = subprocess.run(commande, cwd=tmp, capture_output=True, text=True, timeout=600, env=env)
        return r.returncode, r.stdout + r.stderr, uri
    except subprocess.TimeoutExpired:
        return -1, "Délai dépassé", uri


def indice_entrainement(sortie):
    if "contains NaN" in sortie:
        return "Le modèle reçoit des données sales (prix manquants) : terminez d'abord l'atelier 2."
    return derniere_erreur(sortie)


# ---------------------------------------------------------------- Atelier 0
def atelier0():
    a = Atelier(0, "Prise en main", 0)

    if DONNEES.exists() and DONNEES_PROD.exists():
        a.ok("Les données sont générées dans data/raw/")
    else:
        a.ko("Les données ne sont pas générées", "Lancez :  python scripts/generer_donnees.py")

    rendu = lire_rendu()
    nom = rendu.get("0.1", "")
    if nom:
        a.ok(f"Nom renseigné dans RENDU.md : {nom}")
    else:
        a.ko("Votre nom n'est pas renseigné dans RENDU.md (ligne 0.1)",
             "Ouvrez RENDU.md et écrivez votre nom dans la dernière colonne de la ligne 0.1")

    depot = depot_github()
    if depot is None:
        a.ko("Impossible de trouver l'adresse de votre dépôt GitHub")
    elif depot.lower() == DEPOT_ENSEIGNANT.lower():
        a.ko("Vous travaillez sur le dépôt de l'enseignant, pas sur votre fork",
             "Reprenez l'étape 1 du README : faites un Fork, puis ouvrez le Codespace depuis VOTRE dépôt.")
    else:
        a.ok(f"Vous travaillez sur votre fork : {depot}")

    if not (mode_ci() or mode_prof()):
        git("fetch", "-q")
        code, contenu = git("show", "@{u}:RENDU.md")
        if code == 0 and nom and nom in contenu:
            a.ok("Votre RENDU.md avec votre nom est bien arrivé sur GitHub (push réussi)")
        else:
            a.ko("Votre nom n'est pas encore sur GitHub",
                 "Faites un commit puis un push (README, section « Enregistrer son travail sur GitHub »).")

    if depot and depot.lower() != DEPOT_ENSEIGNANT.lower():
        try:
            total = api_github(f"/repos/{depot}/actions/runs?per_page=1")["total_count"]
            if total:
                a.ok(f"GitHub Actions est activé ({total} exécution(s) trouvée(s))")
            else:
                a.ko("Aucune exécution GitHub Actions sur votre dépôt",
                     "Onglet « Actions » de votre dépôt sur github.com → bouton vert\n"
                     "« I understand my workflows, go ahead and enable them », puis refaites un push.")
        except Exception as e:
            a.info(f"Impossible de vérifier GitHub Actions ({e})")
    return a


# ---------------------------------------------------------------- Atelier 1
INDICES_A1 = {
    "1.1": "Lancez  python scripts/explorer.py  et lisez la ligne 1.1",
    "1.2": "Lisez la ligne 1.2 affichée par scripts/explorer.py",
    "1.3": "Lisez la ligne 1.3 affichée par scripts/explorer.py",
    "1.4": "Complétez le TODO 1.4 de scripts/explorer.py :  (df[\"quantite\"] <= 0).sum()",
    "1.5": "Complétez le TODO 1.5 de scripts/explorer.py (même principe que 1.4, sur prix_unitaire)",
    "1.6": "Attention aux espaces invisibles en fin de mot : « IDF » et « IDF␣ » sont deux valeurs différentes.\n"
           "Lisez la ligne « Nombre de valeurs distinctes » affichée par scripts/explorer.py",
}


def atelier1():
    a = Atelier(1, "Explorer les données brutes", 1)
    rendu = lire_rendu()
    bons = 0
    for cle, attendu in ATTENDUS["atelier1"].items():
        valeur = nombre(rendu.get(cle))
        if valeur is None:
            a.ko(f"Question {cle} : pas de réponse dans RENDU.md", INDICES_A1[cle])
        elif empreinte(cle, int(valeur)) == attendu:
            bons += 1
            a.ok(f"Question {cle} : réponse correcte ({fmt(valeur)})")
        else:
            a.ko(f"Question {cle} : réponse incorrecte ({fmt(valeur)})", INDICES_A1[cle])
    points = 1 if bons >= 5 else 0.5 if bons >= 3 else 0
    message = f"{bons}/6 bonnes réponses"
    (a.ok(message, points) if points == 1 else a.ko(message, points_max=1, points=points))
    return a


# ---------------------------------------------------------------- Atelier 2
def atelier2():
    a = Atelier(2, "Pipeline de données", 4)
    att = ATTENDUS["atelier2"]
    try:
        p = charger("src.pipeline")
        brut = p.ingerer(DONNEES)
    except Exception as e:
        a.ko(f"Impossible de charger src/pipeline.py : {e!r}", points_max=4)
        return a

    # --- nettoyer (2 points)
    propre = None
    try:
        propre = p.nettoyer(brut.copy())
    except Exception as e:
        a.ko(f"nettoyer() provoque une erreur : {e!r}", points_max=2)
    if propre is not None:
        n = int(propre.duplicated().sum())
        if n == 0:
            a.ok("nettoyer : plus aucun doublon", 0.5)
        else:
            a.ko(f"nettoyer : il reste {n} doublons", "TODO 2.1 :  df = df.drop_duplicates()", 0.5)

        n = int(propre["prix_unitaire"].isna().sum())
        if n == 0:
            a.ok("nettoyer : plus aucun prix manquant", 0.5)
        else:
            a.ko(f"nettoyer : il reste {n} prix manquants",
                 "TODO 2.2 :  df = df.dropna(subset=[\"prix_unitaire\"])", 0.5)

        n = int(((propre["quantite"] <= 0) | (propre["prix_unitaire"] <= 0)).sum())
        if n == 0:
            a.ok("nettoyer : toutes les quantités et tous les prix sont > 0", 0.5)
        else:
            a.ko(f"nettoyer : il reste {n} lignes avec une quantité ou un prix <= 0",
                 "TODO 2.3 :  df = df[(df[\"quantite\"] > 0) & (df[\"prix_unitaire\"] > 0)]", 0.5)

        n = len(propre)
        if n == att["lignes"]:
            a.ok(f"nettoyer : {n} lignes conservées, c'est le bon nombre", 0.5)
        else:
            a.ko(f"nettoyer : {n} lignes conservées, ce n'est pas le nombre attendu",
                 "Vous supprimez trop de lignes." if n < att["lignes"] else "Il reste des lignes à supprimer.", 0.5)

    # --- normaliser (1 point)
    norm = None
    try:
        norm = p.normaliser((propre if propre is not None else brut).copy())
    except Exception as e:
        a.ko(f"normaliser() provoque une erreur : {e!r}", points_max=1)
    if norm is not None:
        regions = set(p.REGIONS)
        valeurs = set(norm["region"].dropna().astype(str))
        intrus = sorted(valeurs - regions)
        conformes = not intrus and norm["region"].notna().all()
        if conformes:
            a.ok("normaliser : toutes les régions ont leur forme officielle", 0.5)
            if norm["region"].value_counts().to_dict() == att["regions"]:
                a.ok("normaliser : la répartition des régions est correcte", 0.5)
            else:
                a.ko("normaliser : la répartition des régions n'est pas celle attendue",
                     "Terminez d'abord nettoyer(), et vérifiez que normaliser ne supprime aucune ligne.", 0.5)
        else:
            indice = "TODO 2.4 : enlevez les espaces (.str.strip()) et ramenez chaque valeur à la forme de REGIONS."
            if any(v.strip().lower() in {r.lower() for r in regions} for v in intrus):
                indice += ("\nAttention : .str.title() donne « Hauts-De-France » (D majuscule) !\n"
                           "Astuce : correspondance = {r.upper(): r for r in REGIONS}\n"
                           "         df[\"region\"] = df[\"region\"].str.strip().str.upper().map(correspondance)")
            detail = ", ".join(repr(v) for v in intrus[:4]) or "valeurs vides"
            a.ko(f"normaliser : régions non conformes : {detail}", indice, 0.5)
            a.ko("normaliser : répartition des régions non vérifiée (corrigez d'abord les noms)", points_max=0.5)

    # --- agreger (1 point)
    if norm is not None:
        try:
            kpi = p.agreger(norm.copy())
            colonnes = {"mois", "region", "nb_commandes", "chiffre_affaires", "taux_retour"}
            manquantes = sorted(colonnes - set(kpi.columns))
            if manquantes:
                a.ko(f"agreger : colonnes manquantes : {', '.join(manquantes)}",
                     "TODO 2.5 : voir l'exemple de groupby(...).agg(...) dans ateliers/02-pipeline.md", 1)
            else:
                if len(kpi) == 24:
                    a.ok("agreger : 24 lignes (6 mois × 4 régions)", 0.5)
                else:
                    a.ko(f"agreger : {len(kpi)} lignes au lieu de 24 (6 mois × 4 régions)",
                         "Groupez par mois ET par région :  groupby([\"mois\", \"region\"], as_index=False)", 0.5)
                ligne = kpi[(kpi["mois"].astype(str) == "2026-03") & (kpi["region"] == "Bretagne")]
                correct = (
                    abs(kpi["chiffre_affaires"].sum() - att["chiffre_affaires"]) < 1
                    and int(kpi["nb_commandes"].sum()) == att["lignes"]
                    and len(ligne) == 1
                    and int(ligne["nb_commandes"].iloc[0]) == att["mars_bretagne"]["nb_commandes"]
                    and abs(ligne["taux_retour"].iloc[0] - att["mars_bretagne"]["taux_retour"]) < 1e-6
                )
                if correct:
                    a.ok("agreger : les KPI calculés sont exacts", 0.5)
                else:
                    a.ko("agreger : les valeurs des KPI ne sont pas exactes",
                         "mois au format AAAA-MM :  df[\"date\"].dt.strftime(\"%Y-%m\")\n"
                         "nb_commandes = nombre de commandes, chiffre_affaires = somme de montant,\n"
                         "taux_retour = moyenne de retour. Terminez d'abord nettoyer() et normaliser().", 0.5)
        except Exception as e:
            a.ko(f"agreger() provoque une erreur : {e!r}", points_max=1)
    return a


# ---------------------------------------------------------------- Atelier 3
def _pytest(mutant=None):
    env = {"VERIF_MUTANT": mutant} if mutant else None
    options = ["-p", "verif.mutants"] if mutant else []
    return lancer([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *options,
                   "tests/test_qualite.py"], timeout=300, env=env)


def atelier3():
    a = Atelier(3, "Tests de qualité des données", 3)
    code, sortie = lancer([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider",
                           "tests/test_qualite.py"], timeout=120)
    noms = [l.split("::")[1].split("[")[0] for l in sortie.splitlines() if "::" in l]
    manquants = [t for t in ("test_unicite", "test_regions", "test_volume") if t not in noms]
    if code != 0:
        a.ko("Les tests ne peuvent pas être chargés (erreur de syntaxe ?)", derniere_erreur(sortie), 3)
        return a
    if manquants:
        a.ko(f"Tests manquants : {', '.join(manquants)}", "Voir les TODO 3.1 à 3.3 de tests/test_qualite.py")
    elif len(noms) < 6:
        a.ko(f"Seulement {len(noms)} tests, il en faut au moins 6")
    else:
        a.ok(f"{len(noms)} tests trouvés, dont test_unicite, test_regions et test_volume")

    code, sortie = _pytest()
    vert = code == 0
    if vert and not manquants and len(noms) >= 6:
        a.ok("Tous les tests passent au vert", 1)
    elif vert:
        a.ko("Les tests passent, mais il manque des tests", points_max=1)
    else:
        echecs = [l for l in sortie.splitlines() if l.startswith("FAILED") or l.startswith("ERROR")]
        a.ko("Certains tests échouent", "\n".join(echecs[:5]) + "\nLancez  python -m pytest -v  pour le détail.", 1)

    if not vert:
        a.ko("Détection de bugs non évaluée : vos tests doivent d'abord tous passer", points_max=2)
        return a

    mutants = [
        ("doublons", 1, "un pipeline qui laisse passer des doublons", "test_unicite"),
        ("regions", 0.5, "un pipeline qui laisse passer des régions mal écrites", "test_regions"),
        ("volume", 0.5, "un pipeline qui perd des lignes", "test_volume"),
    ]
    for mutant, points, description, test in mutants:
        code, _ = _pytest(mutant)
        if code != 0:
            a.ok(f"Vos tests détectent {description}", points)
        else:
            a.ko(f"Vos tests ne détectent pas {description}",
                 f"Vérifiez votre {test} : il doit échouer dans ce cas.", points)
    return a


# ---------------------------------------------------------------- Atelier 4
def _client_mlflow(uri):
    import mlflow
    return mlflow.MlflowClient(tracking_uri=uri)


def exporter_preuve_mlflow():
    """Exporte les runs du MLflow local de l'étudiant dans preuves/mlflow_runs.json."""
    base = RACINE / "mlflow.db"
    if not base.exists():
        return None
    client = _client_mlflow(f"sqlite:///{base}")
    experience = client.get_experiment_by_name("retours-produits")
    if experience is None:
        return None
    runs = client.search_runs([experience.experiment_id], order_by=["attributes.start_time ASC"])
    preuve = [{
        "run_id": r.info.run_id,
        "C": r.data.params.get("C"),
        "data_version": r.data.params.get("data_version"),
        "roc_auc": r.data.metrics.get("roc_auc"),
    } for r in runs if r.info.status == "FINISHED"]
    PREUVE_MLFLOW.parent.mkdir(exist_ok=True)
    PREUVE_MLFLOW.write_text(json.dumps(preuve, indent=2), encoding="utf-8")
    return len(preuve)


def atelier4():
    a = Atelier(4, "Suivi des expériences avec MLflow", 3)

    # --- 1 point : train.py enregistre bien paramètres, métrique et modèle
    with tempfile.TemporaryDirectory() as tmp:
        code, sortie, uri = entrainer_dans_dossier_temporaire(tmp)
        if code != 0:
            a.ko("python -m src.train provoque une erreur", indice_entrainement(sortie), 1)
        else:
            import mlflow
            client = _client_mlflow(uri)
            experience = client.get_experiment_by_name("retours-produits")
            runs = client.search_runs([experience.experiment_id]) if experience else []
            if not runs:
                a.ko("Aucun run MLflow créé par src/train.py", points_max=1)
            else:
                run = runs[0]
                if {"C", "data_version"} <= set(run.data.params):
                    a.ok("train.py enregistre les paramètres C et data_version", 0.5)
                else:
                    a.ko("train.py n'enregistre pas les paramètres C et data_version",
                         "TODO 4.1 :  mlflow.log_params({\"C\": C, \"data_version\": version})", 0.5)
                if "roc_auc" in run.data.metrics:
                    a.ok("train.py enregistre la métrique roc_auc", 0.25)
                else:
                    a.ko("train.py n'enregistre pas la métrique roc_auc",
                         "TODO 4.2 :  mlflow.log_metric(\"roc_auc\", auc)", 0.25)
                mlflow.set_tracking_uri(uri)
                modeles = mlflow.search_logged_models(experiment_ids=[experience.experiment_id],
                                                      output_format="list")
                if any(m.source_run_id == run.info.run_id for m in modeles):
                    a.ok("train.py enregistre le modèle", 0.25)
                else:
                    a.ko("train.py n'enregistre pas le modèle",
                         "TODO 4.3 :  mlflow.sklearn.log_model(modele, name=\"model\")", 0.25)

    # --- 1 point : au moins 3 runs avec des C différents
    if not (mode_ci() or mode_prof()):
        n = exporter_preuve_mlflow()
        if n is not None:
            a.info(f"{n} run(s) exporté(s) dans preuves/mlflow_runs.json (pensez à commit + push)")
    runs = []
    if PREUVE_MLFLOW.exists():
        runs = [r for r in json.loads(PREUVE_MLFLOW.read_text(encoding="utf-8"))
                if r.get("C") is not None and r.get("roc_auc") is not None and r.get("data_version")]
    valeurs_c = sorted({float(r["C"]) for r in runs})
    if len(valeurs_c) >= 3:
        a.ok(f"{len(valeurs_c)} valeurs de C comparées : {', '.join(fmt(c) for c in valeurs_c)}", 1)
    else:
        a.ko(f"{len(valeurs_c)} valeur(s) de C complète(s) (avec C, data_version et roc_auc) dans "
             "preuves/mlflow_runs.json, il en faut au moins 3",
             "Lancez  python -m src.train --C 0.001  puis avec 0.01, 0.1 et 1,\n"
             "puis  ./verifier.sh 4  qui exporte la preuve, puis commit + push.", 1)

    # --- 1 point : le C retenu dans RENDU.md est bien le meilleur
    choix = nombre(lire_rendu().get("4.1"))
    if choix is None:
        a.ko("Pas de C retenu dans RENDU.md (ligne 4.1)", points_max=1)
    elif not runs:
        a.ko(f"C retenu = {fmt(choix)}, mais aucun run à comparer", points_max=1)
    else:
        meilleure = max(r["roc_auc"] for r in runs)
        auc_choix = [r["roc_auc"] for r in runs if math.isclose(float(r["C"]), choix)]
        if not auc_choix:
            a.ko(f"C retenu = {fmt(choix)}, mais aucun run MLflow avec cette valeur", points_max=1)
        elif max(auc_choix) >= meilleure - 0.002:
            a.ok(f"C retenu = {fmt(choix)} : c'est bien l'un des meilleurs runs (AUC {max(auc_choix):.3f})", 1)
        else:
            a.ko(f"C retenu = {fmt(choix)} (AUC {max(auc_choix):.3f}) : un autre run fait mieux ({meilleure:.3f})",
                 "Dans l'interface MLflow, triez les runs par roc_auc.", 1)
    return a


# ---------------------------------------------------------------- Atelier 5
def atelier5():
    a = Atelier(5, "Intégration continue et Docker", 3)

    depot = depot_github()
    try:
        reponse = api_github(f"/repos/{depot}/actions/workflows/ci.yml/runs?per_page=100")
        termines = sorted((r for r in reponse["workflow_runs"] if r["status"] == "completed"),
                          key=lambda r: r["created_at"])
        succes = [r for r in termines if r["conclusion"] == "success"]
        echecs = [r for r in termines if r["conclusion"] == "failure"]
        if succes:
            a.ok(f"La CI est passée au vert sur GitHub ({len(succes)} fois)", 1)
        else:
            a.ko("Aucune exécution verte de la CI sur GitHub",
                 "Terminez les ateliers 2 et 3, faites un push, puis regardez l'onglet Actions.", 1)
        if echecs and any(s["created_at"] > echecs[0]["created_at"] for s in succes):
            a.ok("Un échec de la CI a été détecté puis corrigé", 1)
        else:
            a.ko("Pas d'échec de CI suivi d'une correction",
                 "Suivez la partie « Casser volontairement la CI » de l'atelier 5.", 1)
    except Exception as e:
        a.ko(f"Impossible de lire l'historique GitHub Actions de {depot} ({e})",
             "Vérifiez que GitHub Actions est activé sur votre fork (atelier 0).", 2)

    if os.environ.get("VERIF_SANS_DOCKER"):
        a.ko("Docker non vérifié (VERIF_SANS_DOCKER) : à vérifier manuellement", points_max=1)
        return a
    dockerfile = (RACINE / "Dockerfile").read_text(encoding="utf-8") if (RACINE / "Dockerfile").exists() else ""
    if "COPY" not in dockerfile.upper():
        a.ko("Le Dockerfile n'est pas complété", "Complétez les TODO 5.1 et 5.2 du Dockerfile", 1)
        return a
    code, sortie = lancer(["docker", "build", "-t", "tp-dataops-verif", "."], timeout=1500)
    if code == -2:
        a.ko("Docker n'est pas disponible sur cette machine", "Utilisez un Codespace (Docker y est installé).", 1)
    elif code != 0:
        a.ko("docker build échoue", derniere_erreur(sortie, 6), 1)
    else:
        code, sortie = lancer(["docker", "run", "--rm", "tp-dataops-verif"], timeout=600)
        if code == 0 and "lignes après nettoyage" in sortie:
            a.ok("L'image Docker se construit et exécute le pipeline", 1)
        else:
            a.ko("L'image se construit mais le conteneur n'exécute pas le pipeline correctement",
                 derniere_erreur(sortie, 6), 1)
    return a


# ---------------------------------------------------------------- Atelier 6
def atelier6():
    a = Atelier(6, "Détecter la dérive", 1)
    try:
        pipeline = charger("src.pipeline")
        drift = charger("src.drift")
        ref, prod = pipeline.run(str(DONNEES)), pipeline.run(str(DONNEES_PROD))
        resultats = drift.detecter_derive(ref, prod)
    except Exception as e:
        a.ko(f"detecter_derive() provoque une erreur : {e!r}", points_max=1)
    else:
        attendu = ATTENDUS["atelier6"]
        num_ok = all(resultats.get(c) == attendu[c] for c in ["quantite", "prix_unitaire", "anciennete_mois"])
        cat = ["region", "produit"]
        if not num_ok:
            a.ko("La détection sur les variables numériques n'est pas correcte",
                 "Terminez d'abord l'atelier 2 (nettoyage), puis relancez.", 1)
        elif not all(c in resultats for c in cat):
            a.ko("Les variables catégorielles (region, produit) ne sont pas encore testées",
                 "Complétez le TODO 6.1 de src/drift.py (test du khi-deux)", 1)
        elif not all(resultats[c] == attendu[c] for c in cat):
            a.ko("La détection sur region / produit n'est pas correcte",
                 "Si region est signalée en dérive, vérifiez normaliser() (atelier 2).", 1)
        else:
            a.ok("Dérive correctement détectée sur les 5 variables", 1)

    rendu = lire_rendu()
    vides = [c for c in ("6.1", "6.2", "6.3") if not rendu.get(c)]
    if vides:
        a.ko(f"Réponses manquantes dans RENDU.md : {', '.join(vides)} (notées par l'enseignant)")
    else:
        a.ok("Décision et seuil renseignés dans RENDU.md (notés par l'enseignant, 1 pt)")
    return a


# ---------------------------------------------------------------- Atelier 7
def atelier7():
    a = Atelier(7, "Exposer le modèle en API", 2)

    if mode_ci() or mode_prof() or not MODELE.exists():
        with tempfile.TemporaryDirectory() as tmp:
            code, sortie, _ = entrainer_dans_dossier_temporaire(tmp, C="1", exporter=True)
            if code != 0:
                a.ko("Impossible d'exporter le modèle avec  python -m src.train --exporter",
                     indice_entrainement(sortie), 2)
                return a
            MODELE.parent.mkdir(exist_ok=True)
            shutil.copy(Path(tmp) / "modeles" / "modele.joblib", MODELE)

    try:
        from fastapi.testclient import TestClient
        api = charger("src.api")
        client = TestClient(api.app)
    except Exception as e:
        a.ko(f"Impossible de charger src/api.py : {e!r}", points_max=2)
        return a

    r = client.get("/sante")
    if r.status_code == 200 and r.json().get("statut") == "ok":
        a.ok("GET /sante répond {\"statut\": \"ok\"}", 0.5)
    else:
        a.ko(f"GET /sante ne répond pas correctement (code {r.status_code})", points_max=0.5)

    risquee = {"region": "IDF", "produit": "D", "quantite": 19, "prix_unitaire": 50.0, "anciennete_mois": 2}
    sure = {"region": "Bretagne", "produit": "A", "quantite": 1, "prix_unitaire": 50.0, "anciennete_mois": 110}
    try:
        r1, r2 = client.post("/predire", json=risquee), client.post("/predire", json=sure)
        if r1.status_code == 404:
            a.ko("La route POST /predire n'existe pas", "Complétez le TODO 7.1 de src/api.py", 1.5)
            return a
        p1, p2 = r1.json().get("probabilite_retour"), r2.json().get("probabilite_retour")
        if r1.status_code == 200 and isinstance(p1, (int, float)) and 0 <= p1 <= 1 \
                and isinstance(r1.json().get("retour_probable"), bool):
            a.ok(f"POST /predire renvoie une probabilité ({p1}) et retour_probable", 1)
            if p1 > p2:
                a.ok("Les prédictions sont cohérentes (commande risquée > commande sûre)", 0.5)
            else:
                a.ko("Prédictions incohérentes : la commande risquée n'a pas une probabilité plus forte",
                     points_max=0.5)
        else:
            a.ko(f"POST /predire ne renvoie pas le format attendu : {r1.text[:150]}",
                 "Format attendu : {\"probabilite_retour\": 0.42, \"retour_probable\": false}", 1.5)
    except Exception as e:
        a.ko(f"POST /predire provoque une erreur : {e!r}", points_max=1.5)
    return a


ATELIERS = {0: atelier0, 1: atelier1, 2: atelier2, 3: atelier3,
            4: atelier4, 5: atelier5, 6: atelier6, 7: atelier7}
