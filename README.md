# 🛠️ Atelier DataOps — Des données propres et vérifiées

**Durée : 2 h** · **Niveau : débutant, aucune connaissance requise** · **Aucune installation : tout se passe dans le navigateur**

## 🎬 La mission

Un e-commerçant exporte chaque jour ses ventes dans un fichier `ventes.csv`. Problème : ce fichier est **plein d'erreurs** (doublons, prix manquants, quantités négatives, régions mal écrites…).

Vous êtes son équipe data. En 5 petits ateliers, vous allez :

1. **trouver** les erreurs ;
2. écrire un programme qui les **corrige automatiquement** ;
3. écrire des **tests** qui sonnent l'alarme si une erreur revient ;
4. confier ces tests à un **robot** qui les relance à chaque modification.

C'est exactement ce que fait le **DataOps** : rendre les données fiables, de façon automatique.

---

## 🚀 Démarrage (10 minutes)

### Étape 1 — Créer votre copie du projet (« Fork »)

Un *fork* est **votre copie personnelle** du projet, sur votre compte GitHub.

1. Connectez-vous à [github.com](https://github.com).
2. Revenez sur cette page, puis cliquez sur le bouton **Fork** en haut à droite.
3. Ne changez rien et cliquez sur le bouton vert **Create fork**.
4. ✅ **Vérification** : en haut à gauche, l'adresse est **`VOTRE-PSEUDO/DataOps`**, avec la mention *forked from…* en dessous.

> ⚠️ À partir de maintenant, travaillez **toujours depuis votre fork** (`VOTRE-PSEUDO/DataOps`).

### Étape 2 — Activer le robot (« Actions »)

1. Dans **votre fork**, cliquez sur l'onglet **Actions** (en haut).
2. Cliquez sur le bouton vert **I understand my workflows, go ahead and enable them**.

### Étape 3 — Ouvrir votre ordinateur en ligne (« Codespace »)

Un *Codespace* est un **ordinateur dans le cloud**, déjà prêt, que vous utilisez depuis votre navigateur.

1. Dans **votre fork**, cliquez sur le bouton vert **`<> Code`**.
2. Choisissez l'onglet **Codespaces**, puis **Create codespace on main**.
3. ⏳ Patientez 1 à 2 minutes la première fois.
4. ✅ **Vérification** : un éditeur s'ouvre. En bas se trouve le **terminal**. Tapez-y :

   ```bash
   ./verifier.sh
   ```

   Un message d'aide doit s'afficher.

> 💡 **Retrouver votre Codespace plus tard** : [github.com/codespaces](https://github.com/codespaces). Votre travail y est conservé.

### Repères dans l'éditeur

| Zone | Où ? | À quoi ça sert ? |
|---|---|---|
| **Explorateur** | colonne de gauche (icône 📄) | voir et ouvrir les fichiers |
| **Éditeur** | au centre | modifier les fichiers (sauvegarde automatique) |
| **Terminal** | en bas | taper des commandes. Disparu ? Menu `☰` → **Terminal** → **New Terminal** |
| **Contrôle de code source** | colonne de gauche (icône à 3 ronds reliés) | envoyer votre travail sur GitHub |

---

## 📚 Les ateliers

Faites-les **dans l'ordre** : chacun utilise le précédent.

| # | Atelier | Durée | Ce que vous faites | Points |
|---|---|---|---|---|
| 0 | [Prise en main](ateliers/00-prise-en-main.md) | 10 min | Premières commandes, premier envoi sur GitHub | 2 |
| 1 | [Explorer les données](ateliers/01-explorer.md) | 15 min | **Compter** les erreurs du fichier | 4 |
| 2 | [Nettoyer les données](ateliers/02-pipeline.md) | 30 min | **Corriger** les erreurs automatiquement | 6 |
| 3 | [Tester la qualité](ateliers/03-qualite.md) | 25 min | **Écrire** des alarmes (tests) | 5 |
| 4 | [Le robot de vérification](ateliers/04-ci.md) | 20 min | **Casser** puis **réparer**, sous l'œil du robot | 3 |

Chaque fiche suit le même plan : 🎯 **Objectif** → 🧠 **L'idée en une phrase** → 📋 **Étapes** → ✅ **Vérification**.

### ✅ Vérifier votre travail à tout moment

```bash
./verifier.sh 2       # vérifie l'atelier 2 (remplacez 2 par le numéro voulu)
./verifier.sh tout    # vérifie tout et affiche votre note sur 20
```

Chaque ligne affiche ✅ (réussi) ou ❌ (à corriger). Sous chaque ❌, un 💡 **indice** vous dit quoi faire.

---

## 💾 Enregistrer son travail sur GitHub (commit + push)

Vos modifications dans le Codespace **ne sont pas encore sur GitHub**. Pour les envoyer :

- **commit** = prendre une « photo » de votre travail, avec un petit message ;
- **push** = envoyer cette photo sur GitHub.

👉 **Faites-le à la fin de chaque atelier.**

### Avec la souris (recommandé)

1. Cliquez sur l'icône **Contrôle de code source** dans la colonne de gauche (3 ronds reliés).
2. Dans la zone **Message**, écrivez par exemple `Atelier 2`.
3. Cliquez sur **✓ Commit**. Si une fenêtre demande *« …stage all your changes? »*, cliquez sur **Yes**.
4. Cliquez sur **Sync Changes**, puis sur **OK** si une confirmation apparaît.

### Ou avec le terminal

```bash
git add -A
git commit -m "Atelier 2"
git push
```

✅ **Vérification** : sur github.com, rafraîchissez la page de votre fork : votre message apparaît au-dessus de la liste des fichiers.

---

## 📝 Notation (/20)

La note est **entièrement automatique** : c'est celle qu'affiche `./verifier.sh tout`. Elle est aussi recalculée à chaque push (onglet **Actions** de votre fork → dernière exécution → **Summary**).

**Rendu** : le contenu de votre fork à la fin de la séance. Donnez son adresse à l'enseignant : `https://github.com/VOTRE-PSEUDO/DataOps`.

---

## ❓ En cas de problème

| Message ou situation | Solution |
|---|---|
| `No such file or directory: data/raw/ventes.csv` | Tapez `python scripts/generer_donnees.py` |
| `Permission denied: ./verifier.sh` | Tapez `chmod +x verifier.sh` |
| `IndentationError` | Une ligne est mal alignée : 4 espaces au début, comme la ligne du dessus |
| `Author identity unknown` (au commit) | Tapez `git config --global user.name "Prénom Nom"` puis `git config --global user.email "vous@exemple.fr"`, et recommencez |
| `Permission denied` ou `403` (au push) | Vous êtes sur le dépôt de l'enseignant : refaites l'étape 1 (Fork) et ouvrez un Codespace **depuis votre fork** |
| `rejected … fetch first` (au push) | Tapez `git pull --rebase` puis `git push` |
