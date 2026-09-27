# 🧑‍🏫 Guide de l'enseignant

## En résumé : comment ça marche ?

1. Les étudiants copient ce dépôt sur leur compte (**fork**), puis travaillent dans un ordinateur en ligne (**Codespace**) où tout est déjà installé.
2. Ils suivent les fiches du dossier `ateliers/`. Après chaque exercice, la commande `./verifier.sh` leur dit ✅ ou ❌, avec un indice. **Ils avancent donc en autonomie.**
3. Ils écrivent leurs réponses dans `RENDU.md` et envoient leur travail sur GitHub (commit + push).
4. Après la séance, **une seule commande** récupère tous les travaux et calcule 17 points sur 20. Vous notez les 3 points restants en lisant quelques réponses rédigées.

👉 **Vous n'avez pas besoin d'être expert en DataOps**, ni d'être propriétaire de ce dépôt : tout ce que vous faites est en lecture seule.

---

## 1. Qui fait quoi ?

| Moment | Propriétaire du dépôt | Enseignant qui anime (vous) |
|---|---|---|
| **Une fois, au départ** | Rend le dépôt public et vous donne accès au **corrigé** (dépôt privé `DataOps-prof`) | Crée un compte GitHub et accepte l'invitation reçue par e-mail |
| **Avant la séance** | — | Communique aux étudiants le lien du dépôt et fait l'atelier une fois pour s'entraîner (§ 2) |
| **Pendant la séance** | — | Anime (§ 3) et débloque les situations techniques (§ 4) |
| **Après la séance** | — | Lance la notation automatique et note 3 points à la main (§ 5) |
| **Pour modifier l'atelier** | Modifie le dépôt (§ 6) | Lui signale ce qu'il faut changer |

**Les liens dont vous avez besoin :**

- Dépôt de l'atelier, à donner aux étudiants : **https://github.com/bstocker/DataOps**
- Corrigé et réponses attendues, réservés à l'enseignant : **https://github.com/bstocker/DataOps-prof** (accès sur invitation)

---

## 2. Avant la séance

### Une semaine avant : prévenir les étudiants

Envoyez ce message :

> Pour l'atelier DataOps, créez un compte gratuit sur https://github.com et **validez votre adresse e-mail** (sans cela, l'atelier ne fonctionnera pas). Venez avec vos identifiants. Aucune installation n'est nécessaire, un navigateur suffit.

Vérifiez aussi avec le service informatique que le réseau autorise `github.com`, `*.github.dev` et `*.app.github.dev`.

### La veille : faire l'atelier comme un étudiant (45 min)

C'est la meilleure préparation : vous verrez exactement ce que verront les étudiants.

1. Ouvrez **https://github.com/bstocker/DataOps** et suivez le `README` comme un étudiant : Fork, activation d'Actions, Codespace.
2. Ouvrez le corrigé dans un autre onglet (`DataOps-prof` → `REPONSES.md` et dossier `corrige/`).
3. Faites au moins les ateliers 0 à 3 en copiant le code du corrigé, et lancez `./verifier.sh` après chacun.
4. Ensuite, **supprimez votre fork** pour qu'il ne soit pas noté avec ceux des étudiants : dans votre fork, *Settings* → tout en bas → *Delete this repository*.

---

## 3. Déroulé de la séance (3 h)

| Horaire | Étape | Ce que vous dites (l'essentiel) | Résultat attendu |
|---|---|---|---|
| 0:00 | **Lancement** (README) | « Vous êtes l'équipe data d'un e-commerçant. Son fichier de ventes est sale ; vous allez le fiabiliser, en tirer un modèle et le surveiller. » Faites faire le Fork, l'activation d'Actions et le Codespace **tous ensemble, en même temps**. | Tout le monde a un Codespace ouvert |
| 0:10 | **Atelier 0** | « Git, c'est l'appareil photo du code : commit = prendre une photo, push = l'envoyer sur GitHub. » | `./verifier.sh 0` tout vert |
| 0:25 | **Atelier 1** | « Avant de corriger, on mesure. » | 6 bonnes réponses |
| 0:40 | **Atelier 2** | « Un pipeline, c'est une recette automatique : le même code transforme chaque jour le nouveau fichier. » | 4 / 4 |
| 1:05 | **Atelier 3** | « Un test de qualité, c'est une alarme : il sonne si une règle est violée. Un bon test doit savoir échouer. » | 3 / 3, CI verte |
| 1:25 | ☕ Pause (5 min) | | |
| 1:30 | **Atelier 4** | « MLflow est un cahier de laboratoire : chaque essai est noté avec ses réglages, ses résultats et ses données. » | 3 / 3 |
| 1:55 | **Atelier 5** | « La CI est un filet de sécurité : un robot rejoue les tests à chaque envoi. Docker met le code dans une boîte qui marche partout. » | CI rouge puis verte, image construite |
| 2:20 | **Atelier 6** | « Le monde change : les données de production s'éloignent de celles de l'entraînement. Il faut le détecter pour savoir quand réentraîner. » | Dérive détectée, décision écrite |
| 2:40 | **Atelier 7** | « Un modèle utile est un modèle accessible : on l'expose en API. » | La page `/docs` fonctionne |
| 2:45 | **Restitution** | Questions de réflexion (réponses attendues dans `REPONSES.md`). Faites présenter 2 ou 3 étudiants. | Dernier push |

> 💡 Les ateliers 0 à 3 sont très guidés. Les plus rapides avancent seuls, les autres suivent les indices 💡 du vérificateur. Si le temps manque, l'atelier 7 peut être terminé à la maison.

> 📌 À la fin, demandez à chaque étudiant de vous communiquer l'adresse de son fork (`https://github.com/SON-PSEUDO/DataOps`). Ce n'est pas indispensable pour la notation, mais c'est utile pour faire le lien entre un pseudo GitHub et un étudiant.

---

## 4. Problèmes fréquents et solutions

| Symptôme | Cause | Solution |
|---|---|---|
| Le bouton Codespaces est grisé ou affiche une erreur | E-mail GitHub non validé | Valider l'e-mail dans les réglages GitHub |
| `./verifier.sh 0` : « Vous travaillez sur le dépôt de l'enseignant » | Codespace ouvert depuis le dépôt d'origine au lieu du fork | Supprimer ce Codespace, en recréer un **depuis le fork** |
| `push` refusé avec une erreur 403 | Même cause | Même solution |
| Onglet Actions vide, « Aucune exécution » | Actions non activé sur le fork | Onglet Actions → bouton vert *I understand…*, puis refaire un push |
| La CI est rouge après le 1er push | **Normal** : le pipeline n'est pas encore écrit | Elle passe au vert après l'atelier 3 |
| `No such file: data/raw/ventes.csv` | Données non générées (création interrompue) | `python scripts/generer_donnees.py` |
| `IndentationError` | Espaces mal alignés en Python | Aligner la ligne sur celles du dessus (4 ou 8 espaces) |
| MLflow affiche une page 403 ou « Invalid Host header » | MLflow lancé avec `mlflow ui` au lieu du script | Utiliser `./mlflow-ui.sh` |
| La page MLflow ou l'API ne s'ouvre pas | Port non ouvert dans le navigateur | Onglet **PORTS** → survoler la ligne → icône 🌐 |
| Le terminal ne répond plus | MLflow ou l'API tourne au premier plan | `Ctrl + C`, ou ouvrir un 2ᵉ terminal avec le bouton **+** |
| `docker: command not found` | Codespace mal initialisé | Menu `☰` → *View* → *Command Palette* → **Codespaces: Rebuild Container** |
| Atelier 4 : « 0 valeur de C » alors que les runs existent | La preuve n'a pas été poussée | `./verifier.sh 4` puis commit + push de `preuves/mlflow_runs.json` |
| `Author identity unknown` au commit | Git non configuré (rare dans Codespaces) | Voir la FAQ du README |

---

## 5. Noter les travaux (après la date limite)

### Étape 1 — Calculer les 17 points automatiques (≈ 5 min de manipulation)

1. Ouvrez **https://github.com/bstocker/DataOps** (le dépôt d'origine, pas un fork).
2. Bouton vert **`<> Code`** → onglet **Codespaces** → **Create codespace on main**.
   *GitHub peut indiquer que vous n'avez pas le droit de modifier ce dépôt : c'est normal et sans importance, vous n'allez rien modifier.*
3. Une fois le Codespace ouvert, tapez dans le terminal :

   ```bash
   ./verifier.sh etudiants
   ```

4. Le script trouve **tout seul** tous les forks des étudiants, corrige chacun (1 à 2 minutes par étudiant) et affiche au fur et à mesure :

   ```
   [1/28] mcurie/DataOps ... 16 / 17   Marie Curie
   [2/28] aturing/DataOps ... 12.5 / 17   Alan Turing
   ...
   Notes enregistrées dans prof/notes.csv (ouvrable avec Excel)
   ```

5. Dans l'explorateur (à gauche), dossier `prof`, faites un clic droit sur **`notes.csv`** → **Download**. Ouvrez-le avec Excel.
6. Pour savoir pourquoi un étudiant a perdu des points, ouvrez `prof/_forks/<pseudo>.txt` : c'est le détail de sa correction, ligne par ligne.
7. Quand vous avez terminé, supprimez le Codespace : [github.com/codespaces](https://github.com/codespaces) → `…` → **Delete**.

**Options utiles :**

| Commande | Usage |
|---|---|
| `./verifier.sh etudiant mcurie` | Corriger un seul étudiant et afficher le détail de sa correction à l'écran (pratique pendant ou juste après la séance) |
| `./verifier.sh etudiants --sans-docker` | Correction plus rapide. Le point Docker de l'atelier 5 est alors à vérifier à la main. |

> 🔐 **Pourquoi cette correction est-elle fiable ?** Le script utilise **votre** copie du vérificateur, pas celle de l'étudiant. Un étudiant qui aurait modifié son vérificateur n'y gagne rien.
> ⚠️ Le script exécute le code des étudiants : lancez-le **uniquement dans un Codespace**, jamais sur votre ordinateur.

### Étape 2 — Noter les 3 points manuels (≈ 3 min par étudiant)

Pour chaque ligne du fichier Excel, cliquez sur le lien de la colonne `depot`, puis ouvrez **`RENDU.md`**. Les réponses attendues sont dans `REPONSES.md` (dépôt privé `DataOps-prof`).

| Ce que vous lisez dans RENDU.md | Points | Barème |
|---|---|---|
| **Atelier 6** : lignes 6.2 (décision) et 6.3 (seuil) | 1 | 1 = décision appuyée sur des chiffres **et** seuil chiffré · 0,5 = l'un des deux · 0 = vide |
| **Questions de réflexion** Q1 à Q4 | 2 | 0,5 par question : 0,5 = juste et justifiée · 0,25 = partielle · 0 = vide ou fausse |

Dans Excel, reportez ces points dans la colonne `manuel_sur_3`. Ensuite, `note_sur_20` = `total_auto_sur_17` + `manuel_sur_3`.

Profitez-en pour vérifier que les **captures d'écran** s'affichent dans le `RENDU.md` : elles sont obligatoires. En cas de doute sur l'authenticité d'un travail, le lien *commits* de la page du fork montre sa progression réelle, heure par heure.

### Et si un étudiant n'apparaît pas dans le fichier ?

- Il a travaillé sur le dépôt d'origine au lieu de son fork : son travail n'a pas pu être envoyé. Voir le § 4.
- Il a supprimé son fork, ou l'a rendu privé : demandez-lui de le recréer ou de le rendre public.

---

## 6. Modifier l'atelier (réservé au propriétaire du dépôt)

- **Après une modification du code du corrigé ou des données**, régénérer les réponses attendues du vérificateur (voir le `README` du dépôt privé).
- **Si les étudiants ont déjà forké**, ils récupèrent les modifications avec **Sync fork** (voir la FAQ du README).
- **Si le dépôt change d'adresse** (transfert vers le compte du collègue ou vers une organisation) : modifier `DEPOT_ENSEIGNANT` dans `verif/outils.py`, sinon la notation ne trouvera plus les forks.
