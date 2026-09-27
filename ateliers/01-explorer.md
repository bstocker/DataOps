# Atelier 1 — Explorer les données brutes (15 min)

🎯 **Objectif** : repérer et compter les défauts des données **avant** de les corriger.

---

## 🧠 Le concept

*« Garbage in, garbage out »* : un modèle entraîné sur des données fausses donne des prédictions fausses. La première étape d'un projet DataOps consiste donc à **observer** les données et à dresser l'inventaire de leurs défauts. Ce **profilage** sert ensuite à écrire les règles de nettoyage et les tests de qualité.

Les défauts les plus courants :

| Défaut | Exemple | Risque |
|---|---|---|
| Doublon | la même commande exportée deux fois | chiffre d'affaires gonflé |
| Valeur manquante | prix vide | calcul impossible, plantage du modèle |
| Valeur aberrante | quantité = -1, prix négatif | statistiques faussées |
| Incohérence de saisie | `IDF`, `IDF ` (avec un espace à la fin), `idf` | une même région comptée comme trois régions différentes |

---

## 📋 Étapes

### 1. Regarder le fichier

Dans l'explorateur, ouvrez `data/raw/ventes.csv`. Chaque colonne a sa couleur. Faites défiler et cherchez à l'œil nu une région écrite en MAJUSCULES.

### 2. Lancer le script d'exploration

```bash
python scripts/explorer.py
```

Le script affiche déjà les réponses aux questions 1.1, 1.2, 1.3 et 1.6.

### 3. Compléter le script

Ouvrez `scripts/explorer.py` et complétez les deux `TODO`.

- **TODO 1.4** : sur le modèle de la ligne 1.3, comptez les quantités inférieures ou égales à 0 :

  ```python
  print("1.4 Quantités <= 0 :", (df["quantite"] <= 0).sum())
  ```

  > 💡 `df["quantite"] <= 0` donne une colonne de `True`/`False`, et `.sum()` compte les `True`.

- **TODO 1.5** : écrivez vous-même la ligne équivalente pour `prix_unitaire`.

Relancez le script :

```bash
python scripts/explorer.py
```

### 4. Reporter vos réponses

Dans `RENDU.md`, complétez les lignes **1.1 à 1.6** (un nombre par case), puis répondez à la question **1.7**.

> ❓ Pour la question 1.6, regardez bien la liste : pourquoi `'IDF'` et `'IDF '` sont-elles comptées comme deux valeurs différentes ?

---

## ✅ Vérification

```bash
./verifier.sh 1
```

Le vérificateur indique pour chaque question si la réponse est correcte, sans donner la solution.

## 📝 Rendu

- [ ] Lignes 1.1 à 1.6 et question 1.7 complétées dans `RENDU.md`
- [ ] **commit + push** (message : `Atelier 1 terminé`)

➡️ Atelier suivant : [Atelier 2 — Construire le pipeline](02-pipeline.md)
