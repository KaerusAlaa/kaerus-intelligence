# Importer requests pour interroger l'API

import requests

# préparer la requete

adresse = "https://clinicaltrials.gov/api/v2/studies"
criteres = {
    "query.cond": "cancer",
    "query.term": "artificial intelligence",
    "pageSize": 5
}

# envoyer la requete et recuperer la reponse

reponse = requests.get(adresse, params=criteres)
donnees = reponse.json()

print(reponse.status_code)

# boucle de données

for etude in donnees["studies"]:
    identifiant = etude["protocolSection"]["identificationModule"]["nctId"]
    titre = etude["protocolSection"]["identificationModule"]["briefTitle"]
    status = etude["protocolSection"]["statusModule"]["overallStatus"]
    print(identifiant, titre, status)
