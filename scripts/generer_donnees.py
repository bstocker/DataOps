# scripts/generer_donnees.py
# Génère les données de l'atelier. NE PAS MODIFIER ce fichier.
#   data/raw/ventes.csv : export ERP "sale" (doublons, prix manquants, quantités négatives…)
import numpy as np
import pandas as pd
from pathlib import Path


def generer(n=5000, seed=42, drift=False):
    rng = np.random.default_rng(seed)
    anciennete = rng.integers(1, 40 if drift else 120, n)
    produits = rng.choice(["A", "B", "C", "D"], n,
                          p=[0.1, 0.2, 0.2, 0.5] if drift else [0.25] * 4)
    quantite = rng.integers(1, 20, n)
    logit = -2 + 0.08 * quantite - 0.015 * anciennete + 0.8 * (produits == "D")
    df = pd.DataFrame({
        "commande_id": np.arange(1, n + 1),
        "date": pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),
        "region": rng.choice(["IDF", "Hauts-de-France", "Bretagne", "Occitanie"], n),
        "produit": produits,
        "quantite": quantite,
        "prix_unitaire": rng.normal(50, 15, n).round(2),
        "anciennete_mois": anciennete,
        "retour": (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int),
    })
    df["montant"] = (df["quantite"] * df["prix_unitaire"]).round(2)
    return df


def salir(df, seed=0):
    rng = np.random.default_rng(seed)
    df = df.copy()
    df.loc[rng.choice(len(df), 50, replace=False), "prix_unitaire"] = np.nan
    df.loc[rng.choice(len(df), 20, replace=False), "quantite"] = -1
    idx = rng.choice(len(df), 200, replace=False)
    df.loc[idx, "region"] = df.loc[idx, "region"].str.upper() + " "
    return pd.concat([df, df.sample(30, random_state=1)], ignore_index=True)


if __name__ == "__main__":
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    salir(generer()).to_csv("data/raw/ventes.csv", index=False)
    print("Données générées : data/raw/ventes.csv")
