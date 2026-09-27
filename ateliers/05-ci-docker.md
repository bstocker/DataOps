# Atelier 5 — Intégration continue et Docker (25 min)

🎯 **Objectif** : faire vérifier automatiquement votre travail par GitHub à chaque envoi, puis emballer le pipeline dans un conteneur qui fonctionne partout.

---

## 🧠 Le concept

**Intégration continue (CI)** : à chaque `push`, un robot GitHub (*GitHub Actions*) prend une machine neuve, installe le projet, régénère les données et lance les tests. Si un test échoue, vous êtes prévenu **avant** que l'erreur n'atteigne la production. C'est le filet de sécurité du DataOps.

**Conteneur (Docker)** : une « boîte » qui contient le code **et** tout son environnement (Python, bibliothèques). Ainsi, *« ça marche sur ma machine »* devient *« ça marche partout »*.

| Fichier | Rôle |
|---|---|
| `.github/workflows/ci.yml` | la recette suivie par le robot de CI |
| `Dockerfile` | la recette de fabrication de la boîte |

---

## 📋 Partie A — La CI (15 min)

### 1. Lire la recette de la CI

Ouvrez `.github/workflows/ci.yml`. Repérez :
- `on: push` → **quand** le robot se déclenche ;
- `runs-on: ubuntu-latest` → **sur quelle machine** il travaille ;
- les lignes `run:` → **ce qu'il exécute** : installation, génération des données, tests.

### 2. Casser volontairement la CI

1. Dans `src/pipeline.py`, fonction `nettoyer`, **retirez la condition sur le prix**. La ligne du TODO 2.3 devient :

   ```python
   df = df[df["quantite"] > 0]
   ```

2. **commit + push** avec le message `Test : casse volontaire du filtre des prix`.
3. Sur github.com, dans votre fork, onglet **Actions** : une nouvelle exécution démarre (rond jaune 🟡). Attendez 1 à 2 minutes.
4. Elle échoue ❌. Cliquez dessus, puis sur **Tests de qualité des données** : retrouvez le test qui a détecté le problème.
5. 📸 Capture de la CI en échec : `preuves/ci-rouge.png`

### 3. Réparer

1. Remettez la ligne d'origine :

   ```python
   df = df[(df["quantite"] > 0) & (df["prix_unitaire"] > 0)]
   ```

2. Vérifiez en local : `python -m pytest -v` → tout est vert.
3. **commit + push** avec le message `Correction du filtre des prix`.
4. Dans **Actions**, la nouvelle exécution passe au vert ✅.
5. 📸 Capture de la CI en succès : `preuves/ci-verte.png`

> 💡 Dans chaque exécution, le travail **Note automatique** affiche votre note provisoire : cliquez sur l'exécution puis descendez jusqu'à la section **Summary**.

---

## 📋 Partie B — Docker (10 min)

### 1. Compléter le Dockerfile

Ouvrez `Dockerfile` et complétez les `TODO` avec ces instructions :

| Instruction | Signification |
|---|---|
| `COPY requirements.txt .` | copie la liste des bibliothèques dans la boîte |
| `RUN pip install --no-cache-dir -r requirements.txt` | installe les bibliothèques dans la boîte |
| `COPY . .` | copie tout le projet dans la boîte |

> ❓ Pourquoi copier `requirements.txt` **avant** le reste du projet ? Indice : Docker réutilise (« met en cache ») les étapes qui n'ont pas changé.

### 2. Construire l'image

```bash
docker build -t tp-dataops .
```

⏳ 2 à 4 minutes la première fois. La construction doit se terminer sans erreur.

### 3. Lancer le conteneur

```bash
docker run --rm tp-dataops
```

Le conteneur génère les données, exécute le pipeline et affiche le contenu de `kpi.csv`, le tout dans un environnement isolé.

---

## ✅ Vérification

```bash
./verifier.sh 5
```

Objectif : **3 / 3**. Le vérificateur consulte l'historique de vos exécutions sur GitHub et reconstruit l'image Docker.

## 📝 Rendu

- [ ] `preuves/ci-rouge.png` et `preuves/ci-verte.png`
- [ ] Question 5.1 de `RENDU.md`
- [ ] **commit + push** (message : `Atelier 5 terminé`)

➡️ Atelier suivant : [Atelier 6 — Détecter la dérive](06-derive.md)
