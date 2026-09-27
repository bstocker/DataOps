# Atelier 6 — Détecter la dérive des données (20 min)

🎯 **Objectif** : détecter que les données de production ne ressemblent plus aux données d'entraînement, puis décider s'il faut réentraîner le modèle.

---

## 🧠 Le concept

Un modèle apprend sur des données du **passé**. Si le monde change, par exemple avec de nouveaux clients ou un autre mélange de produits, ses prédictions se dégradent. Il existe deux types de dérive :

| Type | Ce qui change | Exemple |
|---|---|---|
| **Data drift** (dérive des données) | la **distribution des entrées** | les clients sont en moyenne beaucoup plus récents qu'avant |
| **Concept drift** (dérive du concept) | la **relation** entre les entrées et le résultat | à profil égal, un client retourne désormais plus souvent |

**Comment la détecter ?** On compare la distribution de chaque colonne entre les données de référence (`ventes.csv`) et les données de production (`ventes_prod.csv`) avec un test statistique :

- **colonnes numériques** → test de **Kolmogorov-Smirnov** (KS) ;
- **colonnes catégorielles** → test du **khi-deux** (χ²).

Chaque test renvoie une **p-value**. Si **p < 0,05**, les deux distributions sont probablement différentes : il y a **dérive**.

---

## 📋 Étapes

### 1. Compléter la détection

Ouvrez `src/drift.py`. Le test KS pour les colonnes numériques est fourni. Complétez le **TODO 6.1** pour les colonnes catégorielles en suivant les 3 étapes écrites en commentaire :

```python
    for col in CAT:
        table = pd.crosstab(pd.concat([ref[col], prod[col]]),
                            ["ref"] * len(ref) + ["prod"] * len(prod))
        p = chi2_contingency(table).pvalue
        resultats[col] = bool(p < seuil)
```

> ⚠️ Ce bloc doit être placé **avant** la ligne `return resultats`, avec 4 espaces d'indentation.

### 2. Exporter le modèle retenu à l'atelier 4

Remplacez `<C>` par votre meilleur C :

```bash
python -m src.train --C <C> --exporter
```

### 3. Lancer l'analyse

```bash
python -m src.drift
```

Lisez les 3 blocs du résultat :
1. **Dérive par variable** : quelles colonnes sont marquées `DÉRIVE` ?
2. **Répartition des produits** : qu'est-ce qui a changé ?
3. **Performance du modèle** : comparez l'AUC sur la référence et sur la production, ainsi que les deux taux de retour.

### 4. Décider

Dans `RENDU.md`, complétez les lignes **6.1 à 6.5** :

- **6.1** Quelles variables dérivent ?
- **6.2** Faut-il réentraîner le modèle ? Pesez le pour et le contre : l'AUC baisse-t-elle beaucoup ? Dispose-t-on des vraies valeurs de `retour` en production ?
- **6.3** Proposez une **règle de déclenchement automatique**, par exemple *« réentraîner si une variable a une p-value < 0,01 **et** si l'AUC baisse de plus de 0,05 »*.
- **6.4 / 6.5** Les deux AUC affichées.

---

## ✅ Vérification

```bash
./verifier.sh 6
```

Le point automatique porte sur la détection. Votre **décision** (6.2 et 6.3) est notée par l'enseignant.

## 📝 Rendu

- [ ] Lignes 6.1 à 6.5 de `RENDU.md`
- [ ] **commit + push** (message : `Atelier 6 terminé`)

➡️ Atelier suivant : [Atelier 7 — Exposer le modèle en API](07-api.md)
