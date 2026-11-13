import requests

adresse = "https://www.ema.europa.eu/en/documents/report/documents-output-epar_documents_json-report_en.json"
reponse = requests.get(adresse)
print("Status:", reponse.status_code)

with open("data/ema_documents_2026-11-13.json", "wb") as fichier:
    fichier.write(reponse.content)
print("Size (MB):", len(reponse.content) / 1_000_000)
