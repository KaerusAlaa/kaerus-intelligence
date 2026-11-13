import json

with open ("data/ema_documents_2026-11-13.json", encoding="utf-8") as fichier :
    contenu = json.load(fichier)

import pandas as pd

documents = pd.DataFrame(contenu["data"])
print(documents["type"].value_counts().to_string())

population = pd.read_csv("data/population_v1_2026-11-12.csv")
numeros = population["EMA product number"]

rapports = documents[(documents["type"] == "assessment-report") & (documents["ema_product_number"].isin(numeros))]
print("Assessment reports found:", len(rapports))
print(rapports["ema_product_number"].value_counts().to_string())

# Dossiers without an assessment report in the EMA documents file
manquants = population[~population["EMA product number"].isin(rapports["ema_product_number"])]
print("Without assessment report:", len(manquants))
print(manquants[["Name of medicine", "Medicine status"]].to_string())

# Dossier with two assessment reports
double = rapports[rapports["ema_product_number"] == "EMEA/H/C/006494"]
print(double[["name", "first_published_date", "document_url"]].to_string())

# Authorised medicines without an assessment report: list all their documents
autorises = manquants[manquants["Medicine status"] == "Authorised"]
docs_autorises = documents[documents["ema_product_number"].isin(autorises["EMA product number"])]
print(docs_autorises[["medicine_name", "type", "name"]].to_string())

# Check: search Tuznue and Zynyz by name instead of product number
print(autorises[["Name of medicine", "EMA product number"]].to_string())
par_nom = documents[documents["medicine_name"].str.contains("Tuznue|Zynyz", case=False, na=False)]
print(par_nom[["medicine_name", "ema_product_number", "type"]].to_string())

# Check: Tuznue and Zynyz in the original EMA medicines table
medicaments = pd.read_excel("data/ema_medicines_2026-11-12.xlsx", skiprows=8)
lignes = medicaments[medicaments["Name of medicine"].isin(["Tuznue", "Zynyz"])]
print(lignes[["Name of medicine", "EMA product number", "Medicine status", "Marketing authorisation date", "Biosimilar", "Active substance"]].to_string())

rapports_autres = documents[(documents["ema_product_number"].isin(["EMEA/H/C/005066", "EMEA/H/C/005632"])) & (documents["type"] == "assessment-report")]
print(rapports_autres[["medicine_name", "name", "first_published_date"]].to_string())

# Control: population medicines whose active substance already exists in other EMA medicines
population = pd.read_csv("data/population_v1_2026-11-12.csv")
substances = population["Active substance"].dropna()
autres = medicaments[medicaments["Active substance"].isin(substances) & ~medicaments["EMA product number"].isin(population["EMA product number"])]
suspects = population[population["Active substance"].isin(autres["Active substance"])]
print(suspects[["Name of medicine", "EMA product number", "Active substance", "Medicine status", "Generic", "Biosimilar"]].to_string())
