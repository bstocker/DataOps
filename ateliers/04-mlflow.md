# Atelier 4 — Suivre les expériences avec MLflow (25 min)

🎯 **Objectif** : entraîner plusieurs versions d'un modèle, **enregistrer** chaque essai, puis choisir le meilleur de façon objective.

---

## 🧠 Le concept

Entraîner un modèle, c'est faire de nombreux essais : réglages différents, données différentes. Sans trace écrite, impossible de savoir quel essai était le meilleur, ni avec quelles données il a été obtenu. **MLflow** est un « cahier de laboratoire » automatique. Pour chaque essai (appelé *run*), il enregistre :

| Élément | Exemple | Fonction MLflow |
|---|---|---|
| **Paramètres** (les réglages) | `C = 0.1` | `mlflow.log_params(...)` |
| **Version des données** | `data_version = 60241538` | `mlflow.log_params(...)` |
| **Métriques** (les résultats) | `roc_auc = 0.714` | `mlflow.log_metric(...)` |
| **Modèle** (le fichier entraîné) | `model` | `mlflow.sklearn.log_model(...)` |

**Le modèle utilisé ici** : une régression logistique qui prédit la probabilité qu'une commande soit retournée. Le réglage **C** contrôle sa complexité : un petit C donne un modèle simple et prudent, un grand C un modèle qui colle davantage aux données.

**La métrique** : l'**AUC** (entre 0,5 et 1) mesure la capacité du modèle à distinguer les commandes retournées des autres. 0,5 = hasard, 1 = parfait.

---

## 📋 Étapes

### 1. Compléter l'enregistrement MLflow

Ouvrez `src/train.py` et complétez les 3 `TODO` :

```python
mlflow.log_params({"C": C, "data_version": version})     # TODO 4.1
mlflow.log_metric("roc_auc", auc)                        # TODO 4.2
mlflow.sklearn.log_model(modele, name="model")           # TODO 4.3
```

> ⚠️ Respectez l'indentation : ces lignes sont **à l'intérieur** du bloc `with mlflow.start_run():` (8 espaces).

### 2. Lancer 4 entraînements

```bash
python -m src.train --C 0.001
python -m src.train --C 0.01
python -m src.train --C 0.1
python -m src.train --C 1
```

Chaque commande affiche l'AUC obtenue. Notez-les.

### 3. Comparer dans l'interface MLflow

```bash
./mlflow-ui.sh
```

1. Une fenêtre propose **Open in Browser** : cliquez dessus. Sinon, allez dans l'onglet **PORTS**, ligne `5000`, puis cliquez sur 🌐.
2. Dans MLflow, cliquez sur l'expérience **retours-produits** à gauche.
3. Cochez vos 4 runs, puis cliquez sur **Compare**.
4. Observez comment l'AUC évolue en fonction de C, et vérifiez que `data_version` est identique pour tous les runs.
5. 📸 Faites une capture de cette comparaison : `preuves/mlflow.png`

> 💡 Le terminal est occupé par MLflow. Pour l'arrêter : cliquez dans le terminal, puis `Ctrl + C`.

### 4. Choisir et justifier

Dans `RENDU.md`, complétez **4.1** (le meilleur C), **4.2** (son AUC) et **4.3** (la justification).

> ❓ Si deux valeurs de C donnent presque la même AUC, laquelle préférer ? (Pensez à la simplicité du modèle.)

### 5. Exporter la preuve

```bash
./verifier.sh 4
```

Le vérificateur crée le fichier `preuves/mlflow_runs.json` à partir de vos runs. **Il doit être envoyé sur GitHub** avec le commit + push.

---

## ✅ Vérification

Objectif de `./verifier.sh 4` : **3 / 3**.

## 📝 Rendu

- [ ] `preuves/mlflow.png` et `preuves/mlflow_runs.json`
- [ ] Lignes 4.1, 4.2 et 4.3 de `RENDU.md`
- [ ] **commit + push** (message : `Atelier 4 terminé`)

➡️ Atelier suivant : [Atelier 5 — Intégration continue et Docker](05-ci-docker.md)
