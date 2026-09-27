# Atelier 7 — Exposer le modèle en API (20 min)

🎯 **Objectif** : rendre le modèle utilisable par d'autres applications (site web, ERP…) grâce à une API web.

---

## 🧠 Le concept

Un modèle enfermé dans un notebook ne sert à personne. Pour l'utiliser, on le **déploie** derrière une **API** : un service web qui reçoit une demande (une commande au format JSON) et renvoie une réponse (la probabilité de retour).

```
 Site e-commerce ──(POST /predire + commande JSON)──►  API  ──► modèle
                ◄──── {"probabilite_retour": 0.49} ────
```

**FastAPI** permet de créer une API en quelques lignes de Python. Il génère aussi automatiquement une **page de documentation interactive** (`/docs`) pour la tester.

---

## 📋 Étapes

### 1. Vérifier que le modèle est exporté

Le modèle a été exporté à l'atelier 6. Sinon :

```bash
python -m src.train --C <votre meilleur C> --exporter
```

### 2. Créer la route de prédiction

Ouvrez `src/api.py`. La route `/sante` est fournie : elle sert à vérifier que le service fonctionne. Complétez le **TODO 7.1** en vous inspirant de la route `/sante` et des 4 indications du commentaire :

```python
@app.post("/predire")
def predire(commande: Commande):
    X = pd.DataFrame([commande.model_dump()])     # la commande devient un tableau d'une ligne
    p = ...                                       # probabilité de retour (voir le commentaire du TODO)
    return {"probabilite_retour": round(float(p), 3), "retour_probable": bool(p >= 0.5)}
```

### 3. Démarrer l'API

```bash
uvicorn src.api:app --reload --port 8000
```

Le terminal affiche `Uvicorn running on http://127.0.0.1:8000`. Laissez-le tourner.

### 4. Tester l'API dans le navigateur

1. Cliquez sur **Open in Browser**, ou onglet **PORTS** → ligne `8000` → 🌐.
2. Ajoutez **`/docs`** à la fin de l'adresse dans la barre du navigateur.
3. Cliquez sur **GET /sante** → **Try it out** → **Execute**. Réponse attendue : `{"statut": "ok"}`.
4. Cliquez sur **POST /predire** → **Try it out**, remplacez l'exemple par :

   ```json
   {
     "region": "IDF",
     "produit": "D",
     "quantite": 19,
     "prix_unitaire": 50,
     "anciennete_mois": 2
   }
   ```

   puis cliquez sur **Execute**.
5. Essayez avec un client ancien (`"anciennete_mois": 110`) et un produit `"A"` : la probabilité baisse-t-elle ?
6. 📸 Capture de la page `/docs` montrant une réponse de `/predire` : `preuves/api.png`

> 💡 Test sans navigateur, dans un **2ᵉ terminal** (bouton **+**) :
> ```bash
> curl -X POST localhost:8000/predire -H "Content-Type: application/json" \
>   -d '{"region":"IDF","produit":"D","quantite":19,"prix_unitaire":50,"anciennete_mois":2}'
> ```

Arrêtez l'API avec `Ctrl + C` dans son terminal.

---

## ✅ Vérification

```bash
./verifier.sh 7
```

Objectif : **2 / 2**.

## 🚀 Pour aller plus loin (facultatif, non noté)

Faites tourner l'API **dans le conteneur Docker** :

```bash
docker build -t tp-dataops .
docker run --rm -p 8000:8000 tp-dataops sh -c \
  "python scripts/generer_donnees.py && python -m src.train --exporter && uvicorn src.api:app --host 0.0.0.0 --port 8000"
```

---

## 🏁 Fin de l'atelier

1. Répondez aux **questions de réflexion** à la fin de `RENDU.md`.
2. Lancez le bilan complet :

   ```bash
   ./verifier.sh tout
   ```

3. Vérifiez que toutes les captures d'écran sont dans `preuves/`.
4. **Dernier commit + push** (message : `Rendu final`).
5. Sur github.com, ouvrez votre `RENDU.md` : les images doivent s'afficher.
6. Onglet **Actions** → dernière exécution → **Summary** : votre note automatique.
7. Arrêtez votre Codespace ([github.com/codespaces](https://github.com/codespaces) → `…` → **Stop codespace**).

🎉 **Bravo, vous avez construit une chaîne DataOps + MLOps complète !**
