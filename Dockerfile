# Dockerfile — Atelier 5 : mettre le pipeline dans un conteneur
FROM python:3.12-slim

WORKDIR /app

# TODO 5.1 : copier le fichier requirements.txt dans l'image
#            puis installer les dépendances avec :  pip install --no-cache-dir -r requirements.txt


# TODO 5.2 : copier tout le reste du projet dans l'image


CMD ["sh", "-c", "python scripts/generer_donnees.py && python -m src.pipeline && cat data/processed/kpi.csv"]
