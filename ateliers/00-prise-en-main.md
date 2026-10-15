# Atelier 0 — Prise en main (10 min)

🎯 **Objectif** : savoir taper une commande, modifier un fichier et envoyer son travail sur GitHub.

---

## 🧠 L'idée en une phrase

En DataOps, **tout est du code, et tout le code est sauvegardé avec son historique** (grâce à Git et GitHub). On peut ainsi revenir en arrière, travailler à plusieurs, et laisser des robots vérifier le travail.

---

## 📋 Étapes

### 1. Taper vos premières commandes

Cliquez dans le **terminal** (en bas de l'écran). Tapez chaque commande, puis appuyez sur `Entrée` :

```bash
ls
```
➡️ affiche la liste des fichiers du projet.

```bash
head -5 data/raw/ventes.csv
```
➡️ affiche les 5 premières lignes du fichier de ventes.

> 💡 La touche `↑` rappelle la commande précédente.

### 2. Écrire votre nom dans le fichier de rendu

1. À gauche, ouvrez le fichier **`RENDU.md`**.
2. Dans le tableau de l'atelier 0, écrivez votre nom et votre groupe **dans la dernière colonne** :

   ```markdown
   | 0.1 | Nom et prénom | Marie Curie |
   | 0.2 | Groupe / classe | BUT 1 |
   ```

3. La sauvegarde est automatique.

### 3. Envoyer votre travail sur GitHub (commit + push)

Suivez la section [💾 Enregistrer son travail sur GitHub](../README.md#-enregistrer-son-travail-sur-github-commit--push) du README. Comme message, écrivez `Atelier 0`.

Ensuite, sur github.com, ouvrez votre fork puis l'onglet **Actions** : une exécution a démarré.
**Elle va échouer (croix rouge ❌), c'est normal !** Votre code n'est pas encore écrit. Vous la ferez passer au vert plus tard.

---

## ✅ Vérification

```bash
./verifier.sh 0
```

Toutes les lignes doivent être ✅ :

```
━━━ Atelier 0 — Prise en main ━━━
  ✅ Les données sont générées dans data/raw/
  ✅ Nom renseigné dans RENDU.md : Marie Curie  (1/1 pt)
  ✅ Vous travaillez sur votre fork : mcurie/DataOps  (1/1 pt)
  ✅ Votre RENDU.md avec votre nom est bien arrivé sur GitHub (push réussi)
  ✅ GitHub Actions est activé (1 exécution(s) trouvée(s))
  Score : 2 / 2
  🎉 Atelier 0 validé !
```

Une ligne ❌ ? Lisez l'indice 💡 juste en dessous : il explique quoi faire.

➡️ Atelier suivant : [Atelier 1 — Explorer les données](01-explorer.md)
