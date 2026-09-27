# src/pipeline.py — Atelier 2 : pipeline de données
# Séquence : Ingérer → Nettoyer → Normaliser → Agréger
import pandas as pd
from pathlib import Path

REGIONS = ["IDF", "Hauts-de-France", "Bretagne", "Occitanie"]


def ingerer(chemin):
    return pd.read_csv(chemin, parse_dates=["date"])


def nettoyer(df):
    # TODO 2.1 : supprimer les lignes en double
    # TODO 2.2 : supprimer les lignes dont le prix unitaire est manquant
    # TODO 2.3 : ne garder que les lignes où quantite > 0 ET prix_unitaire > 0
    return df


def normaliser(df):
    # TODO 2.4 : ramener chaque région à sa forme officielle (voir la liste REGIONS)
    #            "BRETAGNE " -> "Bretagne", "HAUTS-DE-FRANCE " -> "Hauts-de-France", etc.
    return df


def agreger(df):
    # TODO 2.5 : calculer les KPI par mois et par région.
    #            Colonnes attendues : mois, region, nb_commandes, chiffre_affaires, taux_retour
    return df


def run(chemin="data/raw/ventes.csv", export_kpi=False):
    df = normaliser(nettoyer(ingerer(chemin)))
    if export_kpi:
        Path("data/processed").mkdir(parents=True, exist_ok=True)
        agreger(df).to_csv("data/processed/kpi.csv", index=False)
    return df


if __name__ == "__main__":
    df = run(export_kpi=True)
    print(f"{len(df)} lignes après nettoyage. KPI exportés dans data/processed/kpi.csv")
