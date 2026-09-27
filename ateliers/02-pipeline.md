# Atelier 2 — Construire le pipeline de données (25 min)

🎯 **Objectif** : écrire un programme qui transforme automatiquement le fichier sale en données propres, puis en indicateurs (KPI).

---

## 🧠 Le concept

Un **pipeline** est une chaîne d'étapes automatiques et reproductibles. Chaque jour, le même code transforme le nouvel export de la même façon, sans intervention manuelle :

```
 ventes.csv ──► Ingérer ──► Nettoyer ──► Normaliser ──► Agréger ──► kpi.csv
  (sale)        (lire)     (supprimer    (uniformiser   (calculer
                            les erreurs)   les valeurs)   les KPI)
```

Chaque étape est une **fonction Python** qui reçoit un tableau (`DataFrame` pandas) et en renvoie un nouveau.

---

## 📋 Étapes

Ouvrez **`src/pipeline.py`**. Vous allez compléter les fonctions une par une et vérifier après chacune.

### 1. `nettoyer` : supprimer les lignes invalides

Remplacez les 3 lignes `# TODO` par du code. Chaque ligne transforme `df` et le remplace :

| TODO | Ce qu'il faut faire | Outil pandas |
|---|---|---|
| 2.1 | supprimer les doublons | `df = df.drop_duplicates()` |
| 2.2 | supprimer les prix manquants | `df = df.dropna(subset=["prix_unitaire"])` |
| 2.3 | garder quantités **et** prix strictement positifs | `df = df[(condition 1) & (condition 2)]` |

> 💡 Pour le TODO 2.3, une condition s'écrit `df["quantite"] > 0`. Les parenthèses autour de chaque condition sont obligatoires.

Vérifiez :

```bash
./verifier.sh 2
```

Les 4 lignes « nettoyer » doivent être ✅. Les lignes « normaliser » et « agreger » sont encore ❌, c'est normal.

### 2. `normaliser` : uniformiser les régions

Les régions sont parfois écrites `"BRETAGNE "` au lieu de `"Bretagne"`. Il faut ramener chaque valeur à sa forme officielle, celle de la liste `REGIONS`.

**Méthode proposée** :
1. enlever les espaces au début et à la fin : `.str.strip()` ;
2. tout mettre en majuscules : `.str.upper()` ;
3. traduire avec un dictionnaire de correspondance `{"BRETAGNE": "Bretagne", "IDF": "IDF", …}` : `.map(correspondance)`.

```python
def normaliser(df):
    correspondance = {r.upper(): r for r in REGIONS}   # construit le dictionnaire automatiquement
    df = df.copy()
    df["region"] = df["region"]  # ← à compléter en enchaînant .str.strip() .str.upper() .map(...)
    return df
```

> ⚠️ **Piège** : pourquoi ne pas utiliser simplement `.str.title()` ? Essayez `"HAUTS-DE-FRANCE".title()` dans un terminal Python : vous obtenez `Hauts-De-France`, avec un D majuscule, qui ne figure pas dans `REGIONS`.

```bash
./verifier.sh 2
```

### 3. `agreger` : calculer les KPI

On veut, **pour chaque mois et chaque région** : le nombre de commandes, le chiffre d'affaires et le taux de retour. Complétez les `...` :

```python
def agreger(df):
    df = df.assign(mois=df["date"].dt.strftime("%Y-%m"))    # 2026-03-14 -> "2026-03"
    return df.groupby(["mois", "region"], as_index=False).agg(
        nb_commandes=("commande_id", "count"),
        chiffre_affaires=(..., "sum"),     # somme de quelle colonne ?
        taux_retour=(..., "mean"),         # la moyenne d'une colonne de 0/1 donne un pourcentage
    )
```

### 4. Lancer le pipeline complet

```bash
python -m src.pipeline
```

Résultat attendu : `4927 lignes après nettoyage. KPI exportés dans data/processed/kpi.csv`.

Ouvrez `data/processed/kpi.csv` dans l'explorateur. Quelle région a le taux de retour le plus élevé en mars ?

---

## ✅ Vérification

```bash
./verifier.sh 2
```

Objectif : **4 / 4** et « 🎉 Atelier 2 validé ! »

## 📝 Rendu

- [ ] Capture d'écran du résultat de `./verifier.sh 2`, enregistrée dans `preuves/atelier2.png`
- [ ] Question 2.1 de `RENDU.md`
- [ ] **commit + push** (message : `Atelier 2 terminé`)

➡️ Atelier suivant : [Atelier 3 — Tester la qualité](03-qualite.md)
