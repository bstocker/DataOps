# src/train.py — Atelier 4 : entraîner et tracer le modèle avec MLflow
# Lancer avec :  python -m src.train --C 1.0
import argparse
import hashlib
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.pipeline import run

NUM = ["quantite", "prix_unitaire", "anciennete_mois"]
CAT = ["region", "produit"]
CHEMIN_MODELE = "modeles/modele.joblib"


def version_donnees(df):
    """Empreinte courte des données : si les données changent, la version change."""
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()[:8]


def construire_modele(C):
    return Pipeline([
        ("prep", ColumnTransformer([
            ("num", StandardScaler(), NUM),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
        ])),
        ("clf", LogisticRegression(C=C, max_iter=1000)),
    ])


def main(C=1.0, exporter=False):
    df = run()
    version = version_donnees(df)
    X_tr, X_te, y_tr, y_te = train_test_split(
        df[NUM + CAT], df["retour"], test_size=0.2, random_state=42, stratify=df["retour"])
    modele = construire_modele(C)

    mlflow.set_experiment("retours-produits")
    with mlflow.start_run():
        # TODO 4.1 : enregistrer les paramètres "C" et "data_version" avec mlflow.log_params

        modele.fit(X_tr, y_tr)
        auc = roc_auc_score(y_te, modele.predict_proba(X_te)[:, 1])

        # TODO 4.2 : enregistrer la métrique "roc_auc" avec mlflow.log_metric

        # TODO 4.3 : enregistrer le modèle avec mlflow.sklearn.log_model(modele, name="model")

    print(f"C={C}  AUC={auc:.3f}  data_version={version}")

    if exporter:
        Path(CHEMIN_MODELE).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(modele, CHEMIN_MODELE)
        print(f"Modèle exporté dans {CHEMIN_MODELE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entraîne le modèle de prédiction des retours")
    parser.add_argument("--C", type=float, default=1.0, help="force de régularisation (petit C = modèle plus simple)")
    parser.add_argument("--exporter", action="store_true", help="sauvegarde le modèle dans modeles/modele.joblib")
    args = parser.parse_args()
    main(C=args.C, exporter=args.exporter)
