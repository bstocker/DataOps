# 🛠️ Atelier DataOps — Du fichier brut au modèle surveillé

**Durée : 3 h** · **Niveau : débutant** · **Aucune installation : tout se passe dans le navigateur**

## 🎬 La mission

Un e-commerçant veut **anticiper les retours produits**. Chaque jour, son logiciel de gestion (ERP) exporte un fichier `ventes.csv` volontairement « sale » : doublons, prix manquants, quantités négatives, régions mal saisies…

En 8 ateliers de difficulté croissante, vous allez :

1. **fiabiliser** les données (pipeline + tests de qualité) ;
2. **entraîner** un modèle de prédiction et **tracer** vos expériences (MLflow) ;
3. **industrialiser** le tout (intégration continue GitHub Actions + conteneur Docker) ;
4. **surveiller** le modèle en production (détection de dérive) et **l'exposer** en API.

---

## 🚀 Démarrage (10 minutes)

### Étape 1 — Créer votre copie du projet (« Fork »)

Un *fork* est **votre copie personnelle** de ce projet, sur votre compte GitHub. Vous pourrez la modifier librement sans toucher à l'original.

1. Connectez-vous à [github.com](https://github.com) (créez un compte gratuit si besoin).
2. Revenez sur cette page, puis cliquez sur le bouton **Fork** en haut à droite.
3. Sur l'écran suivant, ne changez rien et cliquez sur le bouton vert **Create fork**.
4. ✅ **Vérification** : en haut à gauche, l'adresse doit être **`VOTRE-PSEUDO/DataOps`**, avec en dessous la mention *forked from…*

> ⚠️ À partir de maintenant, travaillez **toujours depuis votre fork** (`VOTRE-PSEUDO/DataOps`), jamais depuis le dépôt de l'enseignant.

### Étape 2 — Activer GitHub Actions sur votre fork

Sur un fork, GitHub désactive les automatisations par défaut. Il faut les réactiver une fois :

1. Dans **votre fork**, cliquez sur l'onglet **Actions** (en haut).
2. Cliquez sur le bouton vert **I understand my workflows, go ahead and enable them**.

### Étape 3 — Ouvrir votre environnement de travail (« Codespace »)

Un *Codespace* est un **ordinateur dans le cloud** avec tout le nécessaire déjà installé (Python, Docker, un éditeur de code), accessible depuis votre navigateur.

1. Dans **votre fork**, cliquez sur le bouton vert **`<> Code`**.
2. Choisissez l'onglet **Codespaces**.
3. Cliquez sur **Create codespace on main**.
4. ⏳ Patientez 2 à 4 minutes la première fois : l'environnement s'installe et les données sont générées automatiquement.
5. ✅ **Vérification** : un éditeur ressemblant à VS Code s'ouvre. En bas se trouve le **terminal**. Tapez-y :

   ```bash
   ./verifier.sh
   ```

   Un message d'aide doit s'afficher.

> 💡 **Retrouver votre Codespace plus tard** : allez sur [github.com/codespaces](https://github.com/codespaces) et cliquez sur son nom. Votre travail y est conservé.
>
> 💡 **Économiser votre quota gratuit** : à la fin de la séance, sur [github.com/codespaces](https://github.com/codespaces), cliquez sur `…` puis **Stop codespace**.

### Repères dans l'éditeur

| Zone | Où ? | À quoi ça sert ? |
|---|---|---|
| **Explorateur** | colonne de gauche (icône 📄) | voir et ouvrir les fichiers |
| **Éditeur** | au centre | modifier les fichiers (sauvegarde automatique) |
| **Terminal** | en bas | taper des commandes. S'il a disparu : menu `☰` → **Terminal** → **New Terminal** |
| **Contrôle de code source** | colonne de gauche (icône à 3 ronds reliés) | envoyer votre travail sur GitHub |

---

## 📚 Les ateliers

Faites-les **dans l'ordre** : chacun s'appuie sur le précédent.

| # | Atelier | Durée | Ce que vous faites | Points |
|---|---|---|---|---|
| 0 | [Prise en main](ateliers/00-prise-en-main.md) | 15 min | Terminal, premier commit + push | — |
| 1 | [Explorer les données](ateliers/01-explorer.md) | 15 min | **Observer** les défauts des données | 1 |
| 2 | [Construire le pipeline](ateliers/02-pipeline.md) | 25 min | **Compléter** du code guidé | 4 |
| 3 | [Tester la qualité](ateliers/03-qualite.md) | 20 min | **Écrire** vos propres tests | 3 |
| 4 | [Suivre les expériences (MLflow)](ateliers/04-mlflow.md) | 25 min | **Comparer** des modèles et choisir | 3 |
| 5 | [Intégration continue et Docker](ateliers/05-ci-docker.md) | 25 min | **Automatiser** et conteneuriser | 3 |
| 6 | [Détecter la dérive](ateliers/06-derive.md) | 20 min | **Analyser** et décider | 2 |
| 7 | [Exposer le modèle en API](ateliers/07-api.md) | 20 min | **Déployer** un service web | 2 |
| — | Questions de réflexion (dans `RENDU.md`) | 15 min | **Prendre du recul** | 2 |

Chaque atelier suit le même plan : 🎯 **Objectif** → 🧠 **Le concept** → 📋 **Étapes** → ✅ **Vérification** → 📝 **Rendu**.

### ✅ Vérifier votre travail à tout moment

```bash
./verifier.sh 2       # vérifie l'atelier 2 (remplacez 2 par le numéro voulu)
./verifier.sh tout    # vérifie tout et affiche votre note automatique
```

Chaque ligne affiche ✅ (réussi) ou ❌ (à corriger), avec un 💡 **indice** pour avancer.

---

## 💾 Enregistrer son travail sur GitHub (commit + push)

Vos modifications dans le Codespace **ne sont pas encore sur GitHub**. Pour les y envoyer, il faut deux actions :

- **commit** = prendre une « photo » de vos modifications avec un message qui la décrit ;
- **push** = envoyer cette photo sur GitHub.

👉 **Faites-le à la fin de chaque atelier.** C'est ce que l'enseignant évaluera.

### Méthode 1 — Avec la souris (recommandée)

1. Cliquez sur l'icône **Contrôle de code source** dans la colonne de gauche (3 ronds reliés). Un chiffre indique le nombre de fichiers modifiés.
2. En haut, dans la zone **Message**, écrivez ce que vous avez fait, par exemple `Atelier 2 terminé`.
3. Cliquez sur **✓ Commit**.
   - Si une fenêtre demande *« There are no staged changes… Would you like to stage all your changes? »*, cliquez sur **Yes** (ou **Always**).
4. Cliquez sur **Sync Changes** (ou **Synchroniser les modifications**), puis sur **OK** si une confirmation apparaît.

### Méthode 2 — Avec le terminal

```bash
git add -A
git commit -m "Atelier 2 terminé"
git push
```

### ✅ Vérifier que c'est bien arrivé

Ouvrez votre fork sur github.com et rafraîchissez la page : votre message de commit apparaît au-dessus de la liste des fichiers.

### 🆘 En cas de problème

| Message | Solution |
|---|---|
| `Author identity unknown` | `git config --global user.name "Prénom Nom"` puis `git config --global user.email "vous@exemple.fr"`, et recommencez |
| `rejected … fetch first` (vous avez modifié un fichier directement sur github.com) | `git pull --rebase` puis `git push` |
| `Permission denied` / `403` | Vous êtes sur le dépôt de l'enseignant : refaites l'étape 1 (Fork) et ouvrez un Codespace **depuis votre fork** |

---

## 📸 Ajouter une capture d'écran comme preuve

1. Faites une capture d'écran :
   - Windows : `Windows + Maj + S`
   - Mac : `Cmd + Maj + 4`
   - Linux : `Impr. écran`
2. Enregistrez l'image sur votre ordinateur avec le **nom exact** demandé (par exemple `mlflow.png`).
3. **Glissez-déposez** le fichier depuis votre ordinateur vers le dossier `preuves/` de l'explorateur (colonne de gauche du Codespace).
4. Faites un **commit + push**. L'image s'affichera automatiquement dans votre `RENDU.md` sur GitHub.

---

## 📝 Ce qui est évalué (/20)

| Critère | Points | Correction |
|---|---|---|
| Atelier 1 : défauts identifiés | 1 | automatique |
| Atelier 2 : pipeline (nettoyage, normalisation, KPI) | 4 | automatique |
| Atelier 3 : tests de qualité (≥ 6, au vert, et capables de détecter des bugs) | 3 | automatique |
| Atelier 4 : suivi MLflow (paramètres, métrique, modèle, ≥ 3 runs, bon choix) | 3 | automatique |
| Atelier 5 : CI opérationnelle (échec puis succès) + Dockerfile | 3 | automatique |
| Atelier 6 : détection de dérive | 1 | automatique |
| Atelier 6 : décision de réentraînement argumentée | 1 | enseignant |
| Atelier 7 : API fonctionnelle | 2 | automatique |
| Questions de réflexion | 2 | enseignant |

- La note automatique est recalculée **à chaque push** : onglet **Actions** de votre fork → dernière exécution → section **Summary**.
- ⚠️ Les captures d'écran demandées dans `RENDU.md` sont **obligatoires**. Sans elles, l'enseignant peut retirer les points de l'atelier correspondant.

**Rendu final** : le contenu de votre fork à la date limite. Communiquez son adresse (`https://github.com/VOTRE-PSEUDO/DataOps`) à l'enseignant.

---

## ❓ FAQ

- **« No such file or directory: data/raw/ventes.csv »** → régénérez les données : `python scripts/generer_donnees.py`
- **« Permission denied: ./verifier.sh »** → `chmod +x verifier.sh mlflow-ui.sh`
- **Une page web (MLflow, API) ne s'ouvre pas** → onglet **PORTS** (à côté de TERMINAL) → survolez la ligne du port → cliquez sur l'icône 🌐.
- **Le terminal est bloqué** (MLflow ou l'API tournent) → c'est normal. Ouvrez un 2ᵉ terminal avec le bouton **+** en haut à droite du terminal, ou arrêtez le programme avec `Ctrl + C`.
- **L'enseignant a mis à jour l'atelier** → sur votre fork (github.com), cliquez sur **Sync fork** → **Update branch**, puis dans le Codespace : `git pull`.
