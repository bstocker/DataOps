# src/api.py — Atelier 7 : exposer le modèle sous forme d'API web
# Lancer avec :  uvicorn src.api:app --reload --port 8000
from functools import lru_cache

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from src.train import CHEMIN_MODELE

app = FastAPI(title="API prédiction des retours produits")


class Commande(BaseModel):
    region: str
    produit: str
    quantite: int
    prix_unitaire: float
    anciennete_mois: int


@lru_cache
def charger_modele():
    return joblib.load(CHEMIN_MODELE)


@app.get("/sante")
def sante():
    return {"statut": "ok"}


# TODO 7.1 : créer la route POST /predire
#   - elle reçoit une `commande: Commande`
#   - elle transforme la commande en tableau :  X = pd.DataFrame([commande.model_dump()])
#   - elle calcule la probabilité :  p = charger_modele().predict_proba(X)[0, 1]
#   - elle renvoie {"probabilite_retour": round(float(p), 3), "retour_probable": bool(p >= 0.5)}
