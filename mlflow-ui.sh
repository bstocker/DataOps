#!/usr/bin/env bash
# Lance l'interface MLflow sur le port 5000, accessible depuis le navigateur via Codespaces.
# (MLflow 3 bloque par défaut les adresses *.app.github.dev : on les autorise ici.)
# Arrêter avec Ctrl+C.
mlflow ui --port 5000 \
  --allowed-hosts "*.app.github.dev,localhost:*,127.0.0.1:*" \
  --cors-allowed-origins "https://*.app.github.dev"
