import pandas as pd

tableau = pd.read_excel("data/ema_medicines_2026-11-12.xlsx", skiprows=8)

humains = tableau[tableau["Category"] == "Human"]
print("Humains :", len(humains))

none_generiques = humains[humains["Generic"] != "Yes"]
print ("dont :", len(none_generiques), "non génériques.")
print ("generiques exclus:", len(humains)-len(none_generiques))

none_biosimilaires = none_generiques[none_generiques["Biosimilar"] != "Yes"]
print ("dont :", len(none_biosimilaires), "non biosimilaires.")
print ("biosimilaires exclus :", len(none_generiques)-len(none_biosimilaires))

masque_onco = none_biosimilaires["ATC code (human)"].str.startswith(("L01", "L02", "V10X"), na=False)
oncologie_atc = none_biosimilaires[masque_onco]
print ("Médicaments retenus :", len(oncologie_atc))

atc_vide = none_biosimilaires["ATC code (human)"].isna().sum()
print ("Médicaments sans ATC :", atc_vide)

sans_atc = none_biosimilaires[none_biosimilaires["ATC code (human)"].isna()]
termes = "neoplasm|carcinoma|cancer|tumor|leukemia|lymphoma|myeloma|melanoma|sarcoma|glioma|glioblastoma|blastoma|mesothelioma|myelodysplastic"
masque_mesh = sans_atc["Therapeutic area (MeSH)"].str.contains(termes, case=False, na=False)
filet_mesh = sans_atc[masque_mesh]
print(filet_mesh[["Name of medicine", "Therapeutic area (MeSH)"]])
print("Médicaments après filtre mesh :", len(filet_mesh))

oncologie = pd.concat([oncologie_atc, filet_mesh])
print("Oncologie (ATC + filet MeSH) :", len(oncologie))

colonnes_dates = ["Marketing authorisation date", "Refusal of marketing authorisation date", "Withdrawal of application date", "Opinion adopted date"]
print(oncologie[colonnes_dates].dtypes)
print(oncologie[colonnes_dates].head())

for colonne in colonnes_dates:
    oncologie[colonne] = pd.to_datetime(oncologie[colonne], format="%d/%m/%Y")
date_issue = oncologie["Marketing authorisation date"].fillna(oncologie["Refusal of marketing authorisation date"]).fillna(oncologie["Withdrawal of application date"]).fillna(oncologie["Opinion adopted date"])

oncologie["Date d'issue"] = date_issue
print("Sans aucune date :", oncologie["Date d'issue"].isna().sum())
depuis_2024 = oncologie[oncologie["Date d'issue"] >= "2024-01-01"]

print("Évalués depuis le 01/01/2024 :", len(depuis_2024))
