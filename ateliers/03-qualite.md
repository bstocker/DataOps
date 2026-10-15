# Atelier 3 — Tester la qualité des données (25 min)

🎯 **Objectif** : écrire des **tests automatiques** qui sonnent l'alarme si les données ne sont plus propres.

---

## 🧠 L'idée en une phrase

Un **test** est une **alarme** : une petite fonction qui vérifie une règle (« il n'y a pas de doublon ») et qui **échoue** si la règle n'est pas respectée. Demain, si le fichier contient une nouvelle erreur, l'alarme sonnera tout de suite.

Un test s'écrit comme ceci :

```python
def test_quelque_chose(df):
    assert <ce qui doit être vrai>
```

- le nom de la fonction commence par **`test_`** ;
- `assert` veut dire « je vérifie que… ». Si ce n'est pas vrai, le test échoue.

Le fichier contient déjà 3 tests. Vous allez en écrire 2 :

| Test | Ce qu'il vérifie | |
|---|---|---|
| `test_schema` | toutes les colonnes sont présentes | ✔️ déjà écrit |
| `test_valeurs` | quantités et prix sont positifs | ✔️ déjà écrit |
| `test_regle_metier` | montant = quantité × prix | ✔️ déjà écrit |
| `test_unicite` | aucune commande n'apparaît deux fois | ✍️ **à écrire** |
| `test_regions` | toutes les régions sont dans la liste officielle | ✍️ **à écrire** |

---

## 📋 Étapes

### 1. Lancer les tests existants

```bash
python -m pytest -v
```

Les 3 tests doivent afficher `PASSED` en vert. Sinon, terminez d'abord l'atelier 2.

### 2. Écrire vos 2 tests

Ouvrez `tests/test_qualite.py`, descendez tout en bas et ajoutez sous les `TODO` :

**TODO 3.1** : chaque numéro de commande doit être unique.

```python
def test_unicite(df):
    assert df["commande_id"].is_unique
```

**TODO 3.2** : chaque région doit faire partie de la liste `REGIONS`.

```python
def test_regions(df):
    assert df["region"].isin(REGIONS).all()
```

> 💡 `def` commence **tout à gauche**. La ligne `assert` commence par **4 espaces**.

Relancez :

```bash
python -m pytest -v
```

Objectif : **5 passed**, tout en vert.

### 3. Expérience : faire sonner l'alarme

Un bon test doit savoir **échouer**. Vérifions-le :

1. Dans `src/pipeline.py`, ajoutez un `#` devant la ligne qui supprime les doublons :

   ```python
       # df = df.drop_duplicates()
   ```

2. Relancez `python -m pytest -v`. Quel test devient rouge (`FAILED`) ?
3. **Enlevez le `#`** pour remettre la ligne, puis relancez : tout redevient vert.

> 🔬 Le vérificateur fait la même expérience tout seul : il casse volontairement le pipeline et contrôle que **vos** tests le remarquent.

---

## ✅ Vérification

```bash
./verifier.sh 3
```

Objectif : **5 / 5**.

## 💬 À discuter avec la classe

Le code était juste à l'atelier 2. Pourquoi a-t-on quand même besoin de tests ? *(Indice : le fichier de demain sera différent.)*

➡️ N'oubliez pas : **commit + push** (message : `Atelier 3`)

Sur github.com, onglet **Actions** : la dernière exécution devrait maintenant être **verte** ✅.

➡️ Atelier suivant : [Atelier 4 — Le robot de vérification](04-ci.md)
