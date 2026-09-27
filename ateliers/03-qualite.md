# Atelier 3 — Tester la qualité des données (20 min)

🎯 **Objectif** : écrire des tests automatiques qui **garantissent** la qualité des données à chaque exécution du pipeline.

---

## 🧠 Le concept

Le fichier de demain peut contenir un nouveau défaut. Plutôt que de tout vérifier à la main, on écrit des **tests de qualité** : de petites fonctions qui vérifient une règle et échouent si elle n'est pas respectée. Les 5 grandes familles de contrôles :

| Famille | Question posée | Test |
|---|---|---|
| **Schéma** | Les colonnes attendues sont-elles là ? | `test_schema` ✔️ fourni |
| **Valeurs** | Les valeurs sont-elles dans les bornes ? | `test_valeurs` ✔️ fourni |
| **Règle métier** | `montant = quantité × prix` ? | `test_regle_metier` ✔️ fourni |
| **Unicité** | Chaque commande n'apparaît-elle qu'une fois ? | `test_unicite` ✍️ à écrire |
| **Référentiel** | Les régions font-elles partie de la liste officielle ? | `test_regions` ✍️ à écrire |
| **Volume** | Le nombre de lignes est-il plausible ? | `test_volume` ✍️ à écrire |

Un test Python avec **pytest** est une fonction dont le nom commence par `test_` et qui contient des `assert` :

```python
def test_exemple(df):
    assert condition_qui_doit_etre_vraie
```

---

## 📋 Étapes

### 1. Lancer les tests existants

```bash
python -m pytest -v
```

Les 3 tests fournis doivent être `PASSED` (en vert). Si ce n'est pas le cas, terminez d'abord l'atelier 2.

### 2. Écrire vos 3 tests

Ouvrez `tests/test_qualite.py` et remplacez les `TODO` :

**TODO 3.1 — `test_unicite`** : aucune `commande_id` ne doit apparaître deux fois.

```python
def test_unicite(df):
    assert df["commande_id"].is_unique
```

**TODO 3.2 — `test_regions`** : toutes les régions doivent appartenir à `REGIONS`.

> 💡 `df["region"].isin(REGIONS)` donne `True`/`False` pour chaque ligne, et `.all()` vérifie que tout est `True`.

**TODO 3.3 — `test_volume`** : entre 4 500 et 5 100 lignes après nettoyage. À vous de l'écrire entièrement.

> 💡 Le nombre de lignes s'obtient avec `len(df)`. En Python, on peut écrire `a <= x <= b`.

```bash
python -m pytest -v
```

Objectif : **6 passed**.

### 3. Expérience : un test utile doit savoir échouer

1. Dans `src/pipeline.py`, désactivez la suppression des doublons en ajoutant un `#` devant la ligne :

   ```python
   # df = df.drop_duplicates()
   ```

2. Relancez `python -m pytest -v`. Quel test passe au rouge (`FAILED`) ? Lisez le message d'erreur.
3. **Retirez le `#`** pour remettre la ligne, puis relancez : tout redevient vert.

> 🔬 Le vérificateur fait la même expérience automatiquement : il introduit 3 bugs (des « mutants ») dans le pipeline et contrôle que **vos** tests les détectent.

---

## ✅ Vérification

```bash
./verifier.sh 3
```

Objectif : **3 / 3**.

## 📝 Rendu

- [ ] Capture d'écran de `python -m pytest -v` avec les 6 tests au vert, enregistrée dans `preuves/atelier3.png`
- [ ] Question 3.1 de `RENDU.md`
- [ ] **commit + push** (message : `Atelier 3 terminé`)

Sur github.com, onglet **Actions** : votre CI devrait maintenant passer au **vert** ✅.

➡️ Atelier suivant : [Atelier 4 — Suivre les expériences avec MLflow](04-mlflow.md)
