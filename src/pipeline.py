# src/pipeline.py — Atelier 2 : le pipeline de données
# Séquence : Ingérer → Nettoyer → Normaliser → Agréger
# Lancer avec :  python -m src.pipeline
import pandas as pd
from pathlib import Path

REGIONS = ["IDF", "Hauts-de-France", "Bretagne", "Occitanie"]


def ingerer(chemin):
    """Lit le fichier CSV brut."""
    return pd.read_csv(chemin, parse_dates=["date"])


def nettoyer(df):
    """Supprime les lignes invalides."""
    # TODO 2.1 : supprimer les lignes en double

    # TODO 2.2 : supprimer les lignes dont le prix unitaire est manquant

    # TODO 2.3 : ne garder que les lignes où quantite > 0 ET prix_unitaire > 0

    return df


def normaliser(df):
    """Écrit chaque région sous sa forme officielle (celle de la liste REGIONS)."""
    correspondance = {"IDF": "IDF", "HAUTS-DE-FRANCE": "Hauts-de-France",
                      "BRETAGNE": "Bretagne", "OCCITANIE": "Occitanie"}
    df = df.copy()
    # TODO 2.4 : enlever les espaces, passer en majuscules, puis traduire avec la correspondance

    return df


def agreger(df):
    """Calcule les indicateurs (KPI) par mois et par région. Déjà écrit : rien à faire ici."""
    df = df.assign(mois=df["date"].dt.strftime("%Y-%m"))
    return df.groupby(["mois", "region"], as_index=False).agg(
        nb_commandes=("commande_id", "count"),
        chiffre_affaires=("montant", "sum"),
        taux_retour=("retour", "mean"),
    )


def run(chemin="data/raw/ventes.csv", export_kpi=False):
    df = normaliser(nettoyer(ingerer(chemin)))
    if export_kpi:
        Path("data/processed").mkdir(parents=True, exist_ok=True)
        agreger(df).to_csv("data/processed/kpi.csv", index=False)
    return df


if __name__ == "__main__":
    df = run(export_kpi=True)
    print(f"{len(df)} lignes après nettoyage. KPI exportés dans data/processed/kpi.csv")
