import json
import pandas as pd

with open("data/ema_documents_2026-11-13.json", encoding="utf-8") as fichier:
    contenu = json.load(fichier)
documents = pd.DataFrame(contenu["data"])

population = pd.read_csv("data/population_v1_2026-11-12.csv")
print("Population:", len(population))

# Correspondence table (checked 2026-11-13): EPAR filed under the number of an earlier withdrawn
# application. Zynyz: authorised 2024-04-19 as 006194, EPAR published 2024-05-02 under 005632.
correspondance = {"EMEA/H/C/006194": "EMEA/H/C/005632"}
population["Document product number"] = population["EMA product number"].replace(correspondance)

rapports = documents[(documents["type"] == "assessment-report") & (documents["ema_product_number"].isin(population["Document product number"]))]
print("Assessment reports:", len(rapports), "for", rapports["ema_product_number"].nunique(), "dossiers")

sans_rapport = population[~population["Document product number"].isin(rapports["ema_product_number"])]
print("Without assessment report:", len(sans_rapport))
print(sans_rapport["Medicine status"].value_counts().to_string())

# Withdrawn applications: look for their documents in the "all documents" file
with open("data/ema_all_documents_2026-11-13.json", encoding="utf-8") as fichier:
    tous = pd.DataFrame(json.load(fichier)["data"])
print("All documents:", len(tous))

retires = sans_rapport[sans_rapport["Medicine status"] == "Application withdrawn"]

# Withdrawn applications: withdrawal assessment report, or the EMA Q&A as a substitute (Ifinwil, 2026-11-13)
documents_a_cribler = []
for index, ligne in retires.iterrows():
    nom = ligne["Name of medicine"]
    trouves = tous[(tous["type"] == "withdrawal-report") & (tous["name"] == "Withdrawal assessment report for " + nom)]
    substitut = "No"
    if len(trouves) == 0:
        trouves = tous[(tous["type"] == "medicine-qa") & (tous["name"].str.startswith("Questions and answers on the withdrawal of application for the marketing authorisation of " + nom))]
        substitut = "Yes"
    for index_doc, doc in trouves.iterrows():
        documents_a_cribler.append({"EMA product number": ligne["EMA product number"], "Name of medicine": nom, "Document type": doc["type"], "Document name": doc["name"], "Document URL": doc["document_url"], "Substitute": substitut})

print("Withdrawal documents:", len(documents_a_cribler))
for d in documents_a_cribler:
    print(d["Name of medicine"], "|", d["Document type"], "|", d["Substitute"])

# Assessment reports (EPAR or refusal report), matched with the correspondence table
for index, ligne in population.iterrows():
    trouves = rapports[rapports["ema_product_number"] == ligne["Document product number"]]
    for index_doc, doc in trouves.iterrows():
        documents_a_cribler.append({"EMA product number": ligne["EMA product number"], "Name of medicine": ligne["Name of medicine"], "Document type": doc["type"], "Document name": doc["name"], "Document URL": doc["document_url"], "Substitute": "No"})

# Dossiers without any published document: pending (recent opinions), re-screened when published
deja = pd.DataFrame(documents_a_cribler)
en_attente = population[~population["EMA product number"].isin(deja["EMA product number"])]
for index, ligne in en_attente.iterrows():
    documents_a_cribler.append({"EMA product number": ligne["EMA product number"], "Name of medicine": ligne["Name of medicine"], "Document type": "pending", "Document name": "", "Document URL": "", "Substitute": "No"})

table = pd.DataFrame(documents_a_cribler)
print("Rows:", len(table), "| Dossiers:", table["EMA product number"].nunique())
print(table["Document type"].value_counts().to_string())
table.to_csv("data/documents_v1_2026-11-13.csv", index=False)
