import os
import time
import requests
import pandas as pd

table = pd.read_csv("data/documents_v1_2026-11-13.csv")
a_telecharger = table[table["Document type"] != "pending"]
print("Documents to download:", len(a_telecharger))

os.makedirs("data/rapports", exist_ok=True)

for index, ligne in a_telecharger.iterrows():
    nom_fichier = "data/rapports/" + ligne["Document URL"].split("/")[-1]
    if os.path.exists(nom_fichier):
        continue
    reponse = requests.get(ligne["Document URL"])
    print(reponse.status_code, ligne["Name of medicine"])
    with open(nom_fichier, "wb") as fichier:
        fichier.write(reponse.content)
    time.sleep(1)
