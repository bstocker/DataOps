# 🧑‍🏫 Guide de l'enseignant

## En résumé

1. Chaque étudiant copie ce dépôt sur son compte GitHub (**fork**), puis travaille dans un ordinateur en ligne (**Codespace**) où tout est déjà installé.
2. Il suit les 5 fiches du dossier `ateliers/`. Après chaque exercice, la commande `./verifier.sh` affiche ✅ ou ❌, avec un indice 💡. **Les étudiants avancent seuls** : votre rôle est surtout de débloquer et de lancer les discussions.
3. Après la séance, **une seule commande** récupère tous les travaux et calcule la note sur 20. **Il n'y a rien à corriger à la main.**

👉 **Vous n'avez pas besoin de connaître le DataOps ni de savoir programmer.** Tout le code à écrire est donné dans les fiches. Ce guide contient aussi les réponses aux questions de discussion (§ 4).

**Lien à donner aux étudiants :** **https://github.com/bstocker/DataOps**

---

## 1. Ce que les étudiants apprennent (à dire en introduction)

Le **DataOps**, c'est rendre les données fiables **automatiquement**, comme une usine avec ses contrôles qualité. En 2 h, les étudiants vont parcourir les 4 gestes de base :

| Geste | Atelier | Image à utiliser |
|---|---|---|
| **Observer** les données | 1 | « Avant de soigner, on fait un diagnostic. » |
| **Nettoyer** automatiquement (pipeline) | 2 | « Une recette de cuisine : le même programme nettoie chaque jour le nouveau fichier. » |
| **Tester** (tests de qualité) | 3 | « Une alarme incendie : elle sonne si une règle est violée. » |
| **Automatiser** les contrôles (CI) | 4 | « Un robot vigile : il relance les alarmes à chaque modification. » |

---

## 2. Avant la séance

### Une semaine avant : prévenir les étudiants

Envoyez ce message :

> Pour l'atelier DataOps, créez un compte gratuit sur https://github.com et **validez votre adresse e-mail** (sans cela, l'atelier ne fonctionnera pas). Venez avec vos identifiants. Aucune installation n'est nécessaire, un navigateur suffit.

Vérifiez aussi avec le service informatique que le réseau autorise `github.com` et `*.github.dev`.

### La veille : faire l'atelier vous-même (45 min)

C'est **la** meilleure préparation : vous verrez exactement ce que verront les étudiants.

1. Ouvrez **https://github.com/bstocker/DataOps** et suivez le `README` comme un étudiant : Fork, activation d'Actions, Codespace.
2. Faites les 5 ateliers en copiant le code donné dans les fiches, et lancez `./verifier.sh` après chacun.
3. Ensuite, **supprimez votre fork** pour qu'il ne soit pas noté avec ceux des étudiants : dans votre fork, *Settings* → tout en bas → *Delete this repository*.

---

## 3. Déroulé de la séance (2 h)

| Horaire | Étape | Ce que vous faites | C'est réussi quand… |
|---|---|---|---|
| 0:00 | **Lancement** | Présentez la mission (README). Faites faire le Fork, l'activation d'Actions et le Codespace **tous ensemble, en projetant votre écran**. | Tout le monde a un Codespace ouvert |
| 0:10 | **Atelier 0** | « Git, c'est l'appareil photo du code : *commit* = prendre une photo, *push* = l'envoyer sur GitHub. » Montrez le commit + push à la souris une fois au tableau. | `./verifier.sh 0` tout vert |
| 0:20 | **Atelier 1** | « Avant de corriger, on mesure. » | `./verifier.sh 1` : 6/6 |
| 0:35 | **Atelier 2** | « On écrit la recette qui nettoie automatiquement. » Prévenez : *les espaces en début de ligne comptent en Python.* | `./verifier.sh 2` : 6/6 |
| 1:05 | **Atelier 3** | « Un test est une alarme. Une bonne alarme doit savoir sonner. » | `./verifier.sh 3` : 5/5 |
| 1:30 | **Atelier 4** | « Un robot relance vos alarmes à chaque envoi. On va le piéger exprès. » | Onglet Actions : vert → rouge → vert |
| 1:50 | **Bilan** | Lancez 2 ou 3 questions « 💬 À discuter » (§ 4). Tout le monde fait `./verifier.sh tout` puis un dernier commit + push. | Dernier push fait |

> 💡 Les plus rapides avancent seuls ; les autres suivent les indices 💡 du vérificateur. **Si le temps manque**, l'atelier 4 peut être terminé à la maison : la note se met à jour à chaque push.

> 📌 À la fin, demandez à chaque étudiant l'adresse de son fork (`https://github.com/SON-PSEUDO/DataOps`) pour faire le lien entre pseudo GitHub et étudiant.

---

## 4. Réponses aux questions « 💬 À discuter »

Chaque fiche se termine par une question à poser à la classe. Elles ne sont pas notées. Voici les réponses :

| Atelier | Question | Réponse attendue |
|---|---|---|
| 1 | Pourquoi 8 régions au lieu de 4 ? | Certaines régions sont écrites en MAJUSCULES avec un espace à la fin (`'IDF '`). Pour l'ordinateur, `'IDF'` et `'IDF '` sont deux textes différents : chaque région est donc comptée deux fois. |
| 2 | Pourquoi corriger les régions avant de calculer le chiffre d'affaires par région ? | Sinon, les ventes d'une même région sont réparties sur deux lignes (`IDF` et `IDF `) et le total de chaque région est faux. |
| 3 | Pourquoi des tests si le code est juste ? | Le code est juste **pour le fichier d'aujourd'hui**. Demain, le fichier peut contenir une nouvelle erreur, ou quelqu'un peut modifier le code par mégarde. Le test le détecte tout de suite. |
| 4 | À quoi sert le robot dans une équipe de 10 personnes ? | Personne n'oublie de lancer les tests : le robot le fait à chaque modification, pour tout le monde. Une erreur est repérée en quelques minutes, et on sait quelle modification l'a causée. |

---

## 5. Problèmes fréquents et solutions

| Symptôme | Cause | Solution |
|---|---|---|
| Le bouton Codespaces est grisé ou affiche une erreur | E-mail GitHub non validé | Valider l'e-mail dans les réglages GitHub |
| `./verifier.sh 0` : « Vous travaillez sur le dépôt de l'enseignant » | Codespace ouvert depuis le dépôt d'origine au lieu du fork | Supprimer ce Codespace et en recréer un **depuis le fork** |
| `push` refusé avec une erreur 403 | Même cause | Même solution |
| Onglet Actions vide, « Aucune exécution » | Actions non activé sur le fork | Onglet Actions → bouton vert *I understand…*, puis refaire un push |
| La CI est rouge au début | **Normal** : le code n'est pas encore écrit | Elle passe au vert après l'atelier 3 |
| `IndentationError` | Espaces mal alignés en Python | Aligner la ligne sur le `# TODO` du dessus (4 espaces) |
| `SyntaxError` | Parenthèse, crochet ou guillemet oublié | Comparer caractère par caractère avec la fiche |
| `No such file: data/raw/ventes.csv` | Données non générées | `python scripts/generer_donnees.py` |
| Atelier 4 : « Pas encore de casse volontaire » alors que la CI est rouge | La casse a été poussée **avant** la première CI verte | Terminer l'atelier 3 (CI verte), puis refaire la casse et la réparation |
| `Author identity unknown` au commit | Git non configuré (rare) | Voir le tableau « En cas de problème » du README |

---

## 6. Noter les travaux (après la séance, ≈ 5 min)

La note sur 20 est **100 % automatique**. Barème : atelier 0 = 2 pts, atelier 1 = 4, atelier 2 = 6, atelier 3 = 5, atelier 4 = 3.

1. Ouvrez **https://github.com/bstocker/DataOps** (le dépôt d'origine, pas un fork).
2. Bouton vert **`<> Code`** → onglet **Codespaces** → **Create codespace on main**.
   *GitHub peut dire que vous n'avez pas le droit de modifier ce dépôt : c'est normal, vous n'allez rien modifier.*
3. Dans le terminal, tapez :

   ```bash
   ./verifier.sh etudiants
   ```

4. Le script trouve **tout seul** les forks des étudiants et les corrige un par un (quelques secondes chacun) :

   ```
   [1/28] mcurie/DataOps ... 20 / 20   Marie Curie
   [2/28] aturing/DataOps ... 15 / 20   Alan Turing
   ...
   Notes enregistrées dans prof/notes.csv (ouvrable avec Excel)
   ```

5. À gauche, dossier `prof`, clic droit sur **`notes.csv`** → **Download**, puis ouvrez-le avec Excel.
6. Pour savoir pourquoi un étudiant a perdu des points : ouvrez `prof/_forks/<pseudo>.txt`, c'est le détail de sa correction.
7. Quand vous avez terminé, supprimez le Codespace : [github.com/codespaces](https://github.com/codespaces) → `…` → **Delete**.

Pour corriger **un seul** étudiant et voir le détail à l'écran : `./verifier.sh etudiant <pseudo>`.

> 🔐 **La note est fiable** : le script utilise **votre** copie du vérificateur, pas celle de l'étudiant. Modifier son vérificateur ne sert à rien.
> ⚠️ Le script exécute le code des étudiants : lancez-le **uniquement dans un Codespace**, jamais sur votre ordinateur.

**Un étudiant n'apparaît pas dans le fichier ?** Il a sans doute travaillé sur le dépôt d'origine au lieu de son fork (voir § 5), ou a supprimé son fork, ou l'a rendu privé.

---

## 7. Modifier l'atelier (réservé au propriétaire du dépôt)

- **Si les données ou les réponses attendues changent** : mettre à jour `verif/attendus.json`.
- **Si les étudiants ont déjà forké** : ils récupèrent les modifications sur leur fork avec **Sync fork** → **Update branch**, puis `git pull` dans le Codespace.
- **Si le dépôt change d'adresse** : modifier `DEPOT_ENSEIGNANT` dans `verif/outils.py`, sinon la notation ne trouvera plus les forks.
