# Atelier 1 — Explorer les données (15 min)

🎯 **Objectif** : repérer et **compter** les erreurs du fichier de ventes avant de les corriger.

---

## 🧠 L'idée en une phrase

*« Garbage in, garbage out »* (« des déchets en entrée donnent des déchets en sortie ») : si les données sont fausses, tous les calculs faits avec seront faux. On commence donc toujours par **regarder** les données.

Les 4 erreurs que vous allez chercher :

| Erreur | Exemple | Pourquoi c'est grave |
|---|---|---|
| **Doublon** | la même commande apparaît deux fois | le chiffre d'affaires est gonflé |
| **Valeur manquante** | un prix vide | le calcul est impossible |
| **Valeur absurde** | une quantité de -1 | les moyennes sont faussées |
| **Saisie incohérente** | `IDF`, `IDF ` (avec un espace à la fin) | une même région est comptée deux fois |

---

## 📋 Étapes

### 1. Regarder le fichier

À gauche, ouvrez `data/raw/ventes.csv`. Chaque colonne a sa couleur. Faites défiler : trouvez-vous une région écrite en MAJUSCULES ?

### 2. Lancer le script d'exploration

```bash
python scripts/explorer.py
```

Le script affiche déjà les réponses 1.1, 1.2, 1.3 et 1.6. Il manque 1.4 et 1.5.

### 3. Compléter le script

Ouvrez `scripts/explorer.py`.

- **TODO 1.4** : la ligne est déjà écrite. Il suffit d'**enlever le `#`** au début de la ligne `# print("1.4 ...`.
  Un `#` en Python veut dire « ceci est un commentaire, ne l'exécute pas ».
- **TODO 1.5** : écrivez la même ligne, mais pour la colonne `prix_unitaire` :

  ```python
  print("1.5 Prix <= 0 :", (df["prix_unitaire"] <= 0).sum())
  ```

> ⚠️ Vos lignes doivent commencer **tout à gauche**, sans espace devant.

Relancez le script :

```bash
python scripts/explorer.py
```

### 4. Reporter les réponses

Dans `RENDU.md`, recopiez les 6 nombres affichés dans les lignes **1.1 à 1.6**.

---

## ✅ Vérification

```bash
./verifier.sh 1
```

Le vérificateur vous dit si chaque réponse est juste, sans donner la solution.

## 💬 À discuter avec la classe

Pourquoi le script compte-t-il **8** régions différentes alors qu'il n'en existe que 4 ?

➡️ N'oubliez pas : **commit + push** (message : `Atelier 1`)

➡️ Atelier suivant : [Atelier 2 — Nettoyer les données](02-pipeline.md)
