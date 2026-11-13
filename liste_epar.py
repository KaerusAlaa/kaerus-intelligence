import pandas as pd

tableau = pd.read_excel("data/ema_medicines_2026-11-12.xlsx", skiprows=8)

humains = tableau[tableau["Category"] == "Human"]
print("Human medicines:", len(humains))

none_generiques = humains[humains["Generic"] != "Yes"]
print ("Non-generics : ", len(none_generiques))
print ("generics excluded", len(humains)-len(none_generiques))

none_biosimilaires = none_generiques[none_generiques["Biosimilar"] != "Yes"]
print ("non-biosimilars :", len(none_biosimilaires))
print ("biosimilars excluded :", len(none_generiques)-len(none_biosimilaires))

masque_onco = none_biosimilaires["ATC code (human)"].str.startswith(("L01", "L02", "V10X"), na=False)
oncologie_atc = none_biosimilaires[masque_onco]
print ("Oncology ATC :", len(oncologie_atc))

atc_vide = none_biosimilaires["ATC code (human)"].isna().sum()
print ("ATC-less drugs :", atc_vide)

sans_atc = none_biosimilaires[none_biosimilaires["ATC code (human)"].isna()]
termes = "neoplasm|carcinoma|cancer|tumor|leukemia|lymphoma|myeloma|melanoma|sarcoma|glioma|glioblastoma|blastoma|mesothelioma|myelodysplastic"
masque_mesh = sans_atc["Therapeutic area (MeSH)"].str.contains(termes, case=False, na=False)
filet_mesh = sans_atc[masque_mesh]
print("oncology MeSH safety net :", len(filet_mesh))

oncologie = pd.concat([oncologie_atc, filet_mesh])
print("Oncology (ATC + MeSH) :", len(oncologie))

colonnes_dates = ["Marketing authorisation date", "Refusal of marketing authorisation date", "Withdrawal of application date", "Opinion adopted date"]

for colonne in colonnes_dates:
    oncologie[colonne] = pd.to_datetime(oncologie[colonne], format="%d/%m/%Y")
date_issue = oncologie["Marketing authorisation date"].fillna(oncologie["Refusal of marketing authorisation date"]).fillna(oncologie["Withdrawal of application date"]).fillna(oncologie["Opinion adopted date"])

oncologie["Date d'issue"] = date_issue

# Missing dates from the EMA file. Source : EMA Zumrad page, withdrew on 13/02/2026 and Ema Aplidin withdrew on 23/07/2025 (checked : 13/11/2026)
oncologie.loc[oncologie["Name of medicine"] == "Zumrad", "Date d'issue"] = pd.Timestamp("2026-02-13")
oncologie.loc[oncologie["Name of medicine"] == "Aplidin", "Date d'issue"] = pd.Timestamp("2025-07-23")

print("Without any outcome date :", oncologie["Date d'issue"].isna().sum())
depuis_2024 = oncologie[oncologie["Date d'issue"] >= "2024-01-01"]

print("Evaluated since 2024-01-01 :", len(depuis_2024))

# Manual review of the MeSH safety net: medicines without an ATC code

a_revoir = depuis_2024[depuis_2024["ATC code (human)"].isna()]
print ("Manual review :", len(a_revoir))

# Revue manuelle du 13/11/2026 : Lifyorli, Gevalka, Itovebi = traitements du cancer, inclus. Aucune exclusion.
# The other medicines without ATC were removed by the earlier filters
for index, ligne in a_revoir.iterrows():
    print(ligne["Name of medicine"], "|", ligne["Medicine status"], "|", ligne["Date d'issue"].date())
    print(ligne["Therapeutic indication"])
    print()

# Conclusion
print ("Conclusion : Out of", len(humains), "human medicines,", len(depuis_2024), "oncology applications evaluated by the EMA since 1 January 2024 form the screening population.")

depuis_2024.to_csv("data/population_v1_2026-11-12.csv", index=False)
