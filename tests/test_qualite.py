# tests/test_qualite.py — Atelier 3 : tests de qualité des données
# Lancer avec :  python -m pytest -v
import pytest
from src.pipeline import run, REGIONS


@pytest.fixture(scope="module")
def df():
    return run("data/raw/ventes.csv")


def test_schema(df):
    attendues = {"commande_id", "date", "region", "produit",
                 "quantite", "prix_unitaire", "montant", "retour"}
    assert attendues <= set(df.columns)


def test_valeurs(df):
    assert (df["quantite"] > 0).all()
    assert (df["prix_unitaire"] > 0).all()


def test_regle_metier(df):
    ecart = (df["quantite"] * df["prix_unitaire"] - df["montant"]).abs()
    assert ecart.max() < 0.01


# TODO 3.1 : écrire test_unicite  -> aucune commande_id ne doit apparaître deux fois


# TODO 3.2 : écrire test_regions  -> toutes les régions doivent appartenir à REGIONS


# TODO 3.3 : écrire test_volume   -> entre 4 500 et 5 100 lignes après nettoyage
