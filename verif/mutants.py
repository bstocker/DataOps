"""Plugin pytest : introduit volontairement un bug dans le pipeline ("mutant").

Un bon jeu de tests doit échouer quand le pipeline est cassé.
Utilisé par le vérificateur :  VERIF_MUTANT=doublons python -m pytest -p verif.mutants
"""
import os


def pytest_configure(config):
    mutant = os.environ.get("VERIF_MUTANT")
    if not mutant:
        return

    import pandas as pd
    import src.pipeline as pipeline

    nettoyer, normaliser = pipeline.nettoyer, pipeline.normaliser

    if mutant == "doublons":
        def nettoyer_mutant(df):
            propre = nettoyer(df)
            return pd.concat([propre, propre.head(30)])
        pipeline.nettoyer = nettoyer_mutant

    elif mutant == "regions":
        def normaliser_mutant(df):
            propre = normaliser(df).copy()
            col = propre.columns.get_loc("region")
            propre.iloc[:40, col] = propre["region"].iloc[:40].str.lower()
            return propre
        pipeline.normaliser = normaliser_mutant
