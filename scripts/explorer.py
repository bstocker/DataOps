# scripts/explorer.py — Atelier 1 : observer les défauts des données brutes
# Lancer avec :  python scripts/explorer.py
import pandas as pd

df = pd.read_csv("data/raw/ventes.csv")

print("=== Aperçu des 5 premières lignes ===")
print(df.head())
print()

# 1.1 Nombre total de lignes
print("1.1 Nombre de lignes :", len(df))

# 1.2 Nombre de lignes en double (lignes strictement identiques)
print("1.2 Doublons :", df.duplicated().sum())

# 1.3 Nombre de prix manquants (cellules vides)
print("1.3 Prix manquants :", df["prix_unitaire"].isna().sum())

# TODO 1.4 : nombre de lignes dont la quantité est inférieure ou égale à 0
#            Il suffit d'enlever le # au début de la ligne ci-dessous :
# print("1.4 Quantités <= 0 :", (df["quantite"] <= 0).sum())


# TODO 1.5 : nombre de lignes dont le prix unitaire est inférieur ou égal à 0
#            Même chose que 1.4, mais avec la colonne "prix_unitaire"


# 1.6 Valeurs distinctes de la colonne region (les guillemets montrent les espaces cachés)
print("1.6 Nombre de valeurs distinctes de region :", df["region"].nunique())
for valeur, nombre in df["region"].value_counts().items():
    print(f"      {valeur!r:22} {nombre}")
