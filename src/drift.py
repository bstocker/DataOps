# src/drift.py — Atelier 6 : détecter la dérive des données
# Lancer avec :  python -m src.drift
import pandas as pd
from scipy.stats import chi2_contingency, ks_2samp
from sklearn.metrics import roc_auc_score

from src.pipeline import run

NUM = ["quantite", "prix_unitaire", "anciennete_mois"]
CAT = ["region", "produit"]


def detecter_derive(ref, prod, seuil=0.05):
    """Renvoie un dictionnaire {colonne: True si la colonne a dérivé, sinon False}."""
    resultats = {}

    # Variables numériques : test de Kolmogorov-Smirnov
    for col in NUM:
        stat, p = ks_2samp(ref[col], prod[col])
        resultats[col] = bool(p < seuil)

    # TODO 6.1 : variables catégorielles (CAT) -> test du khi-deux
    #   Pour chaque col de CAT :
    #     1. construire le tableau de comptage :
    #          table = pd.crosstab(pd.concat([ref[col], prod[col]]),
    #                              ["ref"] * len(ref) + ["prod"] * len(prod))
    #     2. p = chi2_contingency(table).pvalue
    #     3. resultats[col] = bool(p < seuil)

    return resultats


def evaluer_modele(ref, prod, chemin_modele="modeles/modele.joblib"):
    """Compare l'AUC du modèle exporté sur les données d'entraînement et de production."""
    import joblib
    from src.train import CAT as CAT_MODELE, NUM as NUM_MODELE

    modele = joblib.load(chemin_modele)
    cols = NUM_MODELE + CAT_MODELE
    return {
        "auc_reference": roc_auc_score(ref["retour"], modele.predict_proba(ref[cols])[:, 1]),
        "auc_production": roc_auc_score(prod["retour"], modele.predict_proba(prod[cols])[:, 1]),
        "taux_retour_reference": ref["retour"].mean(),
        "taux_retour_production": prod["retour"].mean(),
    }


if __name__ == "__main__":
    ref = run("data/raw/ventes.csv")
    prod = run("data/raw/ventes_prod.csv")

    print("=== Dérive par variable (seuil p < 0.05) ===")
    for col, derive in detecter_derive(ref, prod).items():
        print(f"{col:18} {'DÉRIVE' if derive else 'ok'}")

    print("\n=== Répartition des produits ===")
    print(pd.DataFrame({
        "reference": ref["produit"].value_counts(normalize=True).round(2),
        "production": prod["produit"].value_counts(normalize=True).round(2),
    }))

    print("\n=== Performance du modèle ===")
    try:
        for nom, valeur in evaluer_modele(ref, prod).items():
            print(f"{nom:24} {valeur:.3f}")
    except FileNotFoundError:
        print("Aucun modèle exporté : lancez d'abord  python -m src.train --C <meilleur C> --exporter")
