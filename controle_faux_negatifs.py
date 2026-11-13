import pandas as pd

tableau = pd.read_excel("data/ema_medicines_2026-11-12.xlsx", skiprows=8)
population = pd.read_csv("data/population_v1_2026-11-12.csv")

humains = tableau[tableau["Category"] == "Human"].copy()
colonnes_dates = ["Marketing authorisation date", "Refusal of marketing authorisation date", "Withdrawal of application date", "Opinion adopted date"]
for colonne in colonnes_dates:
    humains[colonne] = pd.to_datetime(humains[colonne], format="%d/%m/%Y")
humains["Date d'issue"] = humains[colonnes_dates[0]].fillna(humains[colonnes_dates[1]]).fillna(humains[colonnes_dates[2]]).fillna(humains[colonnes_dates[3]])

termes = "cancer|carcinoma|neoplasm|tumour|tumor|leukaemia|leukemia|lymphoma|myeloma|melanoma|sarcoma|glioma|blastoma|mesothelioma|myelodysplastic|malignan"
texte = humains["Therapeutic indication"].fillna("") + " " + humains["Therapeutic area (MeSH)"].fillna("")
humains_cancer = humains[texte.str.contains(termes, case=False)]

print("Cancer terms, no outcome date:", humains_cancer["Date d'issue"].isna().sum())

candidats = humains_cancer[(humains_cancer["Date d'issue"] >= "2024-01-01") & ~humains_cancer["EMA product number"].isin(population["EMA product number"])]
print("Possible false negatives:", len(candidats))
print(candidats[["Name of medicine", "ATC code (human)", "Generic", "Biosimilar", "Medicine status"]].to_string())

sans_date = humains_cancer[humains_cancer["Date d'issue"].isna()]
print(sans_date[["Name of medicine", "EMA product number", "ATC code (human)", "Medicine status", "Generic", "Biosimilar"]].to_string())

a_verifier = humains[humains["Name of medicine"].isin(["Ordspono", "Anktiva", "Agilus"])]
for index, ligne in a_verifier.iterrows():
    print(ligne["Name of medicine"], "|", ligne["EMA product number"], "|", ligne["Medicine status"], "|", ligne["Date d'issue"].date())
    print(ligne["Therapeutic indication"])
    print()
