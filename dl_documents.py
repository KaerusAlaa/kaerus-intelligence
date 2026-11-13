import requests

adresse = "https://www.ema.europa.eu/en/documents/report/documents-output-epar_documents_json-report_en.json"
reponse = requests.get(adresse)
print("Status:", reponse.status_code)

with open("data/ema_documents_2026-11-13.json", "wb") as fichier:
    fichier.write(reponse.content)
print("Size (MB):", len(reponse.content) / 1_000_000)

adresse_tous = "https://www.ema.europa.eu/en/documents/report/documents-output-json-report_en.json"
reponse_tous = requests.get(adresse_tous)
print("Status (all documents):", reponse_tous.status_code)

with open("data/ema_all_documents_2026-11-13.json", "wb") as fichier:
    fichier.write(reponse_tous.content)
print("Size (MB):", len(reponse_tous.content) / 1_000_000)
