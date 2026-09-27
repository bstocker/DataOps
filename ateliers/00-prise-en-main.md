# Atelier 0 — Prise en main (15 min)

🎯 **Objectif** : savoir utiliser le terminal, modifier un fichier et envoyer son travail sur GitHub.

---

## 🧠 Le concept

En DataOps, **tout est code et tout est versionné** : scripts, tests, configuration… Git garde l'historique de chaque modification, et GitHub la partage. C'est ce qui permet de revenir en arrière, de travailler à plusieurs et d'automatiser les contrôles.

---

## 📋 Étapes

### 1. Découvrir le terminal

Cliquez dans le terminal (en bas de l'écran) et tapez les commandes suivantes une par une, en appuyant sur `Entrée` après chacune :

```bash
ls
```
➡️ affiche les fichiers du projet.

```bash
python --version
```
➡️ affiche la version de Python installée (3.12).

```bash
ls data/raw
```
➡️ affiche les 2 fichiers de données générés automatiquement : `ventes.csv` et `ventes_prod.csv`.

```bash
head -5 data/raw/ventes.csv
```
➡️ affiche les 5 premières lignes du fichier de ventes.

> 💡 Astuce : la touche `↑` rappelle la commande précédente, la touche `Tab` complète les noms de fichiers.

### 2. Se présenter dans le fichier de rendu

1. Dans l'explorateur (à gauche), ouvrez le fichier **`RENDU.md`**.
2. Dans le tableau de l'atelier 0, complétez la dernière colonne :

   ```markdown
   | 0.1 | Nom et prénom | Marie Curie |
   | 0.2 | Groupe / classe | BUT SD 2 |
   ```

3. La sauvegarde est automatique. Pour aller plus vite : `Ctrl + S`, ou `Cmd + S` sur Mac.

> 💡 Pour voir le rendu mis en forme d'un fichier `.md` : clic droit sur l'onglet du fichier → **Open Preview**.

### 3. Vérifier que GitHub Actions est activé

Sur github.com, dans **votre fork**, onglet **Actions** : si un bouton vert *I understand my workflows…* apparaît, cliquez dessus (voir l'étape 2 du README).

### 4. Envoyer votre travail sur GitHub

Suivez la section [💾 Enregistrer son travail sur GitHub](../README.md#-enregistrer-son-travail-sur-github-commit--push) du README avec le message `Atelier 0 : présentation`.

Sur github.com, ouvrez votre fork, puis le fichier `RENDU.md` : votre nom doit y apparaître.

Ouvrez ensuite l'onglet **Actions** : une exécution nommée *ci-data* a démarré. **Elle va échouer (croix rouge), c'est normal** : le pipeline n'est pas encore écrit. Vous la ferez passer au vert dans les ateliers suivants.

---

## ✅ Vérification

```bash
./verifier.sh 0
```

Toutes les lignes doivent être ✅ :

```
━━━ Atelier 0 — Prise en main ━━━
  ✅ Les données sont générées dans data/raw/
  ✅ Nom renseigné dans RENDU.md : Marie Curie
  ✅ Vous travaillez sur votre fork : mcurie/DataOps
  ✅ Votre RENDU.md avec votre nom est bien arrivé sur GitHub (push réussi)
  ✅ GitHub Actions est activé (1 exécution(s) trouvée(s))
  🎉 Atelier 0 validé !
```

➡️ Atelier suivant : [Atelier 1 — Explorer les données](01-explorer.md)
