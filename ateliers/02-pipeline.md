# Atelier 2 — Nettoyer les données (30 min)

🎯 **Objectif** : écrire un programme qui corrige **automatiquement** les erreurs trouvées à l'atelier 1.

---

## 🧠 L'idée en une phrase

Un **pipeline** est une **recette automatique** : chaque jour, le même programme transforme le nouveau fichier sale en données propres, sans que personne n'ait à le faire à la main.

```
 ventes.csv ──► Lire ──► Nettoyer ──► Normaliser ──► Calculer les KPI ──► kpi.csv
   (sale)               (supprimer    (écrire les     (déjà écrit,
                         les erreurs)  régions pareil)  rien à faire)
```

Vous allez compléter **4 lignes** dans le fichier `src/pipeline.py`.

---

## 📋 Étapes

Ouvrez **`src/pipeline.py`**.

> ⚠️ **Règle importante en Python** : les lignes à l'intérieur d'une fonction commencent par **4 espaces**. Alignez toujours votre ligne sur le commentaire `# TODO` juste au-dessus.

### 1. La fonction `nettoyer` : supprimer les lignes fausses

Sous chaque `# TODO`, ajoutez la ligne de code correspondante :

| TODO | Ce qu'on fait | Ligne à écrire |
|---|---|---|
| 2.1 | supprimer les doublons | `df = df.drop_duplicates()` |
| 2.2 | supprimer les prix manquants | `df = df.dropna(subset=["prix_unitaire"])` |
| 2.3 | garder seulement les quantités **et** les prix positifs | `df = df[(df["quantite"] > 0) & (df["prix_unitaire"] > 0)]` |

Le résultat doit ressembler à ceci :

```python
def nettoyer(df):
    """Supprime les lignes invalides."""
    # TODO 2.1 : supprimer les lignes en double
    df = df.drop_duplicates()
    # TODO 2.2 : ...
    df = df.dropna(subset=["prix_unitaire"])
    # TODO 2.3 : ...
    df = df[(df["quantite"] > 0) & (df["prix_unitaire"] > 0)]
    return df
```

Vérifiez :

```bash
./verifier.sh 2
```

Les 4 lignes « nettoyer » doivent être ✅. Les lignes « normaliser » sont encore ❌ : c'est normal, c'est l'étape suivante.

### 2. La fonction `normaliser` : écrire les régions toujours de la même façon

Dans le fichier, une région est parfois écrite `"BRETAGNE "` au lieu de `"Bretagne"`. On la corrige en 3 temps :

1. `.str.strip()` enlève les espaces au début et à la fin → `"BRETAGNE"` ;
2. `.str.upper()` met tout en majuscules → `"BRETAGNE"` (et `"Bretagne"` devient aussi `"BRETAGNE"`) ;
3. `.map(correspondance)` traduit avec le dictionnaire écrit juste au-dessus → `"Bretagne"`.

Sous le `# TODO 2.4`, ajoutez :

```python
    df["region"] = df["region"].str.strip().str.upper().map(correspondance)
```

Vérifiez :

```bash
./verifier.sh 2
```

### 3. Lancer le pipeline complet

```bash
python -m src.pipeline
```

Résultat attendu : `4927 lignes après nettoyage. KPI exportés dans data/processed/kpi.csv`

Ouvrez `data/processed/kpi.csv` (dossier `data/processed`, à gauche). Pour chaque mois et chaque région, vous voyez le nombre de commandes, le chiffre d'affaires et le taux de retour.

---

## ✅ Vérification

```bash
./verifier.sh 2
```

Objectif : **6 / 6** et « 🎉 Atelier 2 validé ! »

## 🆘 Problèmes fréquents

| Message | Solution |
|---|---|
| `IndentationError` | La ligne n'est pas bien alignée : mettez exactement 4 espaces au début, comme le `# TODO` au-dessus |
| `SyntaxError` | Il manque une parenthèse `)`, un crochet `]` ou un guillemet `"` : comparez avec le tableau |
| `KeyError: 'prix_unitaire'` | Le nom de colonne est mal écrit (accent, majuscule, espace…) |

## 💬 À discuter avec la classe

Pourquoi faut-il corriger les régions **avant** de calculer le chiffre d'affaires par région ?

➡️ N'oubliez pas : **commit + push** (message : `Atelier 2`)

➡️ Atelier suivant : [Atelier 3 — Tester la qualité](03-qualite.md)
