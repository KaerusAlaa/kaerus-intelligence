import pandas as pd

tableau = pd.read_excel("data/ema_medicines_2026-11-12.xlsx", skiprows=8)

# Criterion v1.2 (2026-11-13): "Not yet assigned" is a missing ATC code, not a value.
# Found by the false-negative control (Ordspono). These rows now go through the MeSH safety net.
print("ATC 'Not yet assigned':", (tableau["ATC code (human)"] == "Not yet assigned").sum())
tableau.loc[tableau["ATC code (human)"] == "Not yet assigned", "ATC code (human)"] = None

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

# Criterion v1.2 (2026-11-13): dossiers added after the false-negative control (manual review).
# Anktiva (EMEA/H/C/006622): BCG-unresponsive bladder cancer, ATC L03AC03 (immunostimulant), outside L01/L02/V10X.
ajouts = none_biosimilaires[none_biosimilaires["EMA product number"].isin(["EMEA/H/C/006622"])]
print("Added after false-negative control:", len(ajouts))
oncologie = pd.concat([oncologie_atc, filet_mesh, ajouts])

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

# Manual exclusion (2026-11-13): Tuznue (EMEA/H/C/006252, trastuzumab) is a biosimilar of Herceptin
# according to its EMA page, but is flagged Biosimilar = No in the EMA file.
depuis_2024 = depuis_2024[depuis_2024["EMA product number"] != "EMEA/H/C/006252"]

# Criterion clarification v1.1 (2026-11-13): an oncology dossier also needs a cancer indication.
# ATC classes the molecule, not the indication (e.g. Orblid, bevacizumab, hereditary haemorrhagic telangiectasia).
# Dossiers without any cancer term in their indication are flagged for manual review.
termes_indication = "cancer|carcinoma|neoplasm|tumour|tumor|leukaemia|leukemia|lymphoma|myeloma|melanoma|sarcoma|glioma|blastoma|mesothelioma|myelodysplastic|malignan"
masque_cancer = depuis_2024["Therapeutic indication"].str.contains(termes_indication, case=False, na=False)
sans_cancer = depuis_2024[~masque_cancer]
print("Indication without cancer term (manual review):", len(sans_cancer))
for index, ligne in sans_cancer.iterrows():
    print(ligne["Name of medicine"], "|", ligne["EMA product number"])
    print(ligne["Therapeutic indication"])
    print()

# Manual review of indications (2026-11-13), criterion v1.1:
# kept: Kinselby (cutaneous T-cell lymphoma), Ezmekly (plexiform neurofibromas, benign tumour included)
# excluded, no tumour indication: Vijoice (PROS), Orblid (hereditary haemorrhagic telangiectasia),
# Yartemlea (transplant-associated thrombotic microangiopathy), Masitinib AB Science (ALS),
# Theralugand and Ilumira (radiopharmaceutical precursors, no indication of their own)
exclus_indication = ["EMEA/H/C/006539", "EMEA/H/C/006392", "EMEA/H/C/005247", "EMEA/H/C/005897", "EMEA/H/C/005882", "EMEA/H/C/006596"]
avant = len(depuis_2024)
depuis_2024 = depuis_2024[~depuis_2024["EMA product number"].isin(exclus_indication)]
print("Excluded (no tumour indication):", avant - len(depuis_2024))

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
