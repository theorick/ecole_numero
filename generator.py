import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# URL à scraper
url = 'https://www.annuaire-mairie.fr/etablissement-scolaire-saint-pierre-974.html'

# Requête HTTP
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Création d'un fichier Excel
wb = Workbook()
ws = wb.active
ws.title = "Écoles"

# Entêtes
ws.append(["Nom de l'établissement", "Type", "Adresse", "Téléphone"])

# Récupération des données
annonces = soup.find_all('div', class_='annonce_content')

for annonce in annonces:
    titre = annonce.find('div', class_='annonce_titre').text.strip()

    # Initialisation des champs
    type_ecole = adresse = telephone = ""

    descs = annonce.find('div', class_='annonce_desc').find_all('p')
    for desc in descs:
        text = desc.text.strip()
        if "public" in text or "privé" in text:
            type_ecole = text
        elif "Chemin" in text or "Rue" in text or "avenue" in text or "boulevard" in text or "Allée" in text:
            adresse = text
        elif text.startswith("02"):
            telephone = text

    # Ajout d'une ligne dans le fichier Excel
    ws.append([titre, type_ecole, adresse, telephone])

# Sauvegarde du fichier
wb.save("ecoles_saint_pierre.xlsx")
print("Fichier Excel 'ecoles_saint_pierre.xlsx' généré avec succès.")
