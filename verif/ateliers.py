"""Vérifications de chaque atelier. Chaque fonction renvoie un objet Atelier."""
import importlib
import sys

from verif.outils import (ATTENDUS, DEPOT_ENSEIGNANT, RACINE, Atelier, api_github, depot_github,
                          derniere_erreur, empreinte, fmt, git, lancer, lire_rendu, mode_ci,
                          mode_prof, nombre)

DONNEES = RACINE / "data" / "raw" / "ventes.csv"

# Points de chaque atelier (total : 20)
BAREME = {0: 2, 1: 4, 2: 6, 3: 5, 4: 3}


def charger(module):
    """Importe (ou ré-importe) un module de l'étudiant."""
    if module in sys.modules:
        return importlib.reload(sys.modules[module])
    return importlib.import_module(module)


# ---------------------------------------------------------------- Atelier 0
def atelier0():
    a = Atelier(0, "Prise en main", BAREME[0])

    if DONNEES.exists():
        a.ok("Les données sont générées dans data/raw/")
    else:
        a.ko("Les données ne sont pas générées", "Lancez :  python scripts/generer_donnees.py")

    rendu = lire_rendu()
    nom = rendu.get("0.1", "")
    if nom:
        a.ok(f"Nom renseigné dans RENDU.md : {nom}", 1)
    else:
        a.ko("Votre nom n'est pas renseigné dans RENDU.md (ligne 0.1)",
             "Ouvrez RENDU.md et écrivez votre nom dans la dernière colonne de la ligne 0.1", 1)

    depot = depot_github()
    if depot is None:
        a.ko("Impossible de trouver l'adresse de votre dépôt GitHub", points_max=1)
    elif depot.lower() == DEPOT_ENSEIGNANT.lower():
        a.ko("Vous travaillez sur le dépôt de l'enseignant, pas sur votre fork",
             "Reprenez l'étape 1 du README : faites un Fork, puis ouvrez le Codespace depuis VOTRE dépôt.", 1)
    else:
        a.ok(f"Vous travaillez sur votre fork : {depot}", 1)

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
    "1.4": "Dans scripts/explorer.py, enlevez le # devant la ligne print(\"1.4 ...\"), puis relancez le script",
    "1.5": "Complétez le TODO 1.5 de scripts/explorer.py (même ligne que 1.4, avec \"prix_unitaire\")",
    "1.6": "Attention aux espaces invisibles en fin de mot : « IDF » et « IDF␣ » sont deux valeurs différentes.\n"
           "Lisez la ligne « Nombre de valeurs distinctes » affichée par scripts/explorer.py",
}


def atelier1():
    a = Atelier(1, "Explorer les données brutes", BAREME[1])
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
    points = round(bons * BAREME[1] / 6 * 2) / 2
    message = f"{bons}/6 bonnes réponses"
    (a.ok(message, points) if bons == 6 else a.ko(message, points_max=BAREME[1], points=points))
    return a


# ---------------------------------------------------------------- Atelier 2
def atelier2():
    a = Atelier(2, "Nettoyer les données", BAREME[2])
    att = ATTENDUS["atelier2"]
    try:
        p = charger("src.pipeline")
        brut = p.ingerer(DONNEES)
    except Exception as e:
        a.ko(f"Impossible de charger src/pipeline.py : {e!r}",
             "Regardez la ligne indiquée dans le message : souvent une parenthèse ou un guillemet oublié,\n"
             "ou une ligne mal alignée (4 espaces au début).", BAREME[2])
        return a

    # --- nettoyer (4 points)
    propre = None
    try:
        propre = p.nettoyer(brut.copy())
    except Exception as e:
        a.ko(f"nettoyer() provoque une erreur : {e!r}", points_max=4)
    if propre is not None:
        n = int(propre.duplicated().sum())
        if n == 0:
            a.ok("nettoyer : plus aucun doublon", 1)
        else:
            a.ko(f"nettoyer : il reste {n} doublons", "TODO 2.1 :  df = df.drop_duplicates()", 1)

        n = int(propre["prix_unitaire"].isna().sum())
        if n == 0:
            a.ok("nettoyer : plus aucun prix manquant", 1)
        else:
            a.ko(f"nettoyer : il reste {n} prix manquants",
                 "TODO 2.2 :  df = df.dropna(subset=[\"prix_unitaire\"])", 1)

        n = int(((propre["quantite"] <= 0) | (propre["prix_unitaire"] <= 0)).sum())
        if n == 0:
            a.ok("nettoyer : toutes les quantités et tous les prix sont > 0", 1)
        else:
            a.ko(f"nettoyer : il reste {n} lignes avec une quantité ou un prix <= 0",
                 "TODO 2.3 :  df = df[(df[\"quantite\"] > 0) & (df[\"prix_unitaire\"] > 0)]", 1)

        n = len(propre)
        if n == att["lignes"]:
            a.ok(f"nettoyer : {n} lignes conservées, c'est le bon nombre", 1)
        else:
            a.ko(f"nettoyer : {n} lignes conservées au lieu de {att['lignes']}",
                 "Vous supprimez trop de lignes." if n < att["lignes"] else "Il reste des lignes à supprimer.", 1)

    # --- normaliser (2 points)
    norm = None
    try:
        norm = p.normaliser((propre if propre is not None else brut).copy())
    except Exception as e:
        a.ko(f"normaliser() provoque une erreur : {e!r}", points_max=2)
    if norm is not None:
        regions = set(p.REGIONS)
        intrus = sorted(set(norm["region"].dropna().astype(str)) - regions)
        if not intrus and norm["region"].notna().all():
            a.ok("normaliser : toutes les régions ont leur forme officielle", 1)
            if norm["region"].value_counts().to_dict() == att["regions"]:
                a.ok("normaliser : la répartition des régions est correcte", 1)
            else:
                a.ko("normaliser : la répartition des régions n'est pas celle attendue",
                     "Terminez d'abord nettoyer(), et vérifiez que normaliser ne supprime aucune ligne.", 1)
        else:
            detail = ", ".join(repr(v) for v in intrus[:4]) or "valeurs vides"
            a.ko(f"normaliser : régions non conformes : {detail}",
                 "TODO 2.4 :  df[\"region\"] = df[\"region\"].str.strip().str.upper().map(correspondance)", 1)
            a.ko("normaliser : répartition des régions non vérifiée (corrigez d'abord les noms)", points_max=1)
    return a


# ---------------------------------------------------------------- Atelier 3
def _pytest(mutant=None):
    env = {"VERIF_MUTANT": mutant} if mutant else None
    options = ["-p", "verif.mutants"] if mutant else []
    return lancer([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *options,
                   "tests/test_qualite.py"], timeout=300, env=env)


def atelier3():
    a = Atelier(3, "Tester la qualité des données", BAREME[3])
    code, sortie = lancer([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider",
                           "tests/test_qualite.py"], timeout=120)
    if code != 0:
        a.ko("Les tests ne peuvent pas être chargés (erreur de syntaxe ?)", derniere_erreur(sortie), BAREME[3])
        return a
    noms = [l.split("::")[1].split("[")[0] for l in sortie.splitlines() if "::" in l]
    manquants = [t for t in ("test_unicite", "test_regions") if t not in noms]
    if manquants:
        a.ko(f"Tests manquants : {', '.join(manquants)}", "Voir les TODO 3.1 et 3.2 de tests/test_qualite.py")
    else:
        a.ok(f"{len(noms)} tests trouvés, dont test_unicite et test_regions")

    code, sortie = _pytest()
    vert = code == 0
    if vert and not manquants:
        a.ok("Tous les tests passent au vert", 2)
    elif vert:
        a.ko("Les tests passent, mais il manque vos 2 tests", points_max=2)
    else:
        echecs = [l for l in sortie.splitlines() if l.startswith("FAILED") or l.startswith("ERROR")]
        a.ko("Certains tests échouent", "\n".join(echecs[:5]) + "\nLancez  python -m pytest -v  pour le détail.", 2)

    if not vert:
        a.ko("Détection de bugs non évaluée : vos tests doivent d'abord tous passer", points_max=3)
        return a

    mutants = [
        ("doublons", "un pipeline qui laisse passer des doublons", "test_unicite"),
        ("regions", "un pipeline qui laisse passer des régions mal écrites", "test_regions"),
    ]
    for mutant, description, test in mutants:
        code, _ = _pytest(mutant)
        if code != 0:
            a.ok(f"Vos tests détectent {description}", 1.5)
        else:
            a.ko(f"Vos tests ne détectent pas {description}",
                 f"Vérifiez votre {test} : il doit échouer dans ce cas.", 1.5)
    return a


# ---------------------------------------------------------------- Atelier 4
def atelier4():
    a = Atelier(4, "Le robot de vérification (CI)", BAREME[4])

    depot = depot_github()
    try:
        reponse = api_github(f"/repos/{depot}/actions/workflows/ci.yml/runs?per_page=100")
    except Exception as e:
        a.ko(f"Impossible de lire l'historique GitHub Actions de {depot} ({e})",
             "Vérifiez que GitHub Actions est activé sur votre fork (atelier 0).", BAREME[4])
        return a

    termines = sorted((r for r in reponse["workflow_runs"] if r["status"] == "completed"),
                      key=lambda r: r["created_at"])
    succes = [r for r in termines if r["conclusion"] == "success"]
    if succes:
        a.ok(f"La CI est passée au vert sur GitHub ({len(succes)} fois)", 1)
    else:
        a.ko("Aucune exécution verte de la CI sur GitHub",
             "Terminez les ateliers 2 et 3, faites un commit + push, puis regardez l'onglet Actions.", 1)

    # Le scénario attendu : vert → rouge (casse volontaire) → vert (réparation)
    casse = next((r for r in termines if r["conclusion"] == "failure"
                  and succes and r["created_at"] > succes[0]["created_at"]), None)
    repare = casse and any(s["created_at"] > casse["created_at"] for s in succes)
    if repare:
        a.ok("La CI a détecté votre casse volontaire, puis elle est repassée au vert", 2)
    elif casse:
        a.ko("La CI a détecté la casse, mais elle n'est pas encore repassée au vert",
             "Enlevez le # ajouté dans src/pipeline.py, puis commit + push.", 2)
    else:
        a.ko("Pas encore de casse volontaire détectée par la CI (après une première CI verte)",
             "Suivez l'étape « Casser volontairement » de l'atelier 4.", 2)
    return a


ATELIERS = {0: atelier0, 1: atelier1, 2: atelier2, 3: atelier3, 4: atelier4}
