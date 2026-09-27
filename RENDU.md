# 📝 Mon rendu — Atelier DataOps

> **Comment remplir ce fichier ?**
> - Complétez la **dernière colonne** des tableaux (entre les deux derniers `|`).
> - Ne modifiez pas les numéros (`0.1`, `1.1`…) : le vérificateur les lit automatiquement.
> - Pour les réponses rédigées, écrivez sous la ligne `✍️ Réponse :`.
> - Les captures d'écran vont dans le dossier `preuves/` avec **exactement** le nom indiqué.
> - N'oubliez pas : **commit + push** régulièrement (voir le README).

---

## Atelier 0 — Qui suis-je ?

| N° | Question | Votre réponse |
|---|---|---|
| 0.1 | Nom et prénom | |
| 0.2 | Groupe / classe | |

---

## Atelier 1 — Les défauts des données brutes

| N° | Question | Votre réponse |
|---|---|---|
| 1.1 | Nombre total de lignes dans `ventes.csv` | |
| 1.2 | Nombre de lignes en double | |
| 1.3 | Nombre de prix manquants | |
| 1.4 | Nombre de lignes avec une quantité ≤ 0 | |
| 1.5 | Nombre de lignes avec un prix ≤ 0 | |
| 1.6 | Nombre de valeurs différentes dans la colonne `region` | |

**1.7 — Parmi ces défauts, lequel vous semble le plus dangereux pour un modèle de prédiction ? Pourquoi ?**

✍️ Réponse :

---

## Atelier 2 — Le pipeline

📸 Preuve : capture du terminal montrant `./verifier.sh 2` validé → `preuves/atelier2.png`

![Atelier 2](preuves/atelier2.png)

**2.1 — Pourquoi faut-il normaliser les régions avant de calculer les KPI par région ?**

✍️ Réponse :

---

## Atelier 3 — Les tests de qualité

📸 Preuve : capture de `python -m pytest -v` avec tous les tests au vert → `preuves/atelier3.png`

![Atelier 3](preuves/atelier3.png)

**3.1 — Pourquoi tester les *données*, et pas seulement le *code* ?**

✍️ Réponse :

---

## Atelier 4 — Suivi des expériences (MLflow)

| N° | Question | Votre réponse |
|---|---|---|
| 4.1 | Valeur de C retenue (la meilleure) | |
| 4.2 | AUC obtenue avec ce C | |

**4.3 — Justifiez votre choix en 2 ou 3 phrases.**

✍️ Réponse :

📸 Preuve : capture de l'interface MLflow comparant au moins 3 runs → `preuves/mlflow.png`

![MLflow](preuves/mlflow.png)

---

## Atelier 5 — Intégration continue et Docker

📸 Preuve 1 : la CI en **échec** (croix rouge dans l'onglet Actions) → `preuves/ci-rouge.png`

![CI rouge](preuves/ci-rouge.png)

📸 Preuve 2 : la CI en **succès** (coche verte) → `preuves/ci-verte.png`

![CI verte](preuves/ci-verte.png)

**5.1 — Qu'est-ce que la CI vous a apporté quand vous avez cassé le filtre des prix ?**

✍️ Réponse :

---

## Atelier 6 — Dérive des données

| N° | Question | Votre réponse |
|---|---|---|
| 6.1 | Variables qui dérivent | |
| 6.2 | Faut-il réentraîner le modèle ? (oui / non + raison courte) | |
| 6.3 | Seuil de déclenchement automatique proposé | |
| 6.4 | AUC sur les données de référence | |
| 6.5 | AUC sur les données de production | |

---

## Atelier 7 — L'API

📸 Preuve : capture de la page `/docs` montrant une réponse de `POST /predire` → `preuves/api.png`

![API](preuves/api.png)

---

## Questions de réflexion

**Q1 — Quelle dérive observez-vous : data drift, concept drift, ou les deux ? Justifiez.**

✍️ Réponse :

**Q2 — Quelles métadonnées et quelle entrée de glossaire ajouteriez-vous pour la colonne `retour` ?**

✍️ Réponse :

**Q3 — Choisiriez-vous un déploiement Canary ou Blue/Green pour la nouvelle version du modèle ? Pourquoi ?**

✍️ Réponse :

**Q4 — Quels deux KPI DataOps suivriez-vous pour ce pipeline, et comment les mesurer ?**

✍️ Réponse :
