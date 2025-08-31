import requests
import pandas as pd
import defs

# Création d'un objet session avec requests
session = requests.Session()

# Construction de l'URL basée sur la doc de l'API OANDA
url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"

# # Requêtes pour récupérer les données
response = session.get(url, params=None, headers=defs.SECURE_HEADER)

if response.status_code == 200:
    print("Données récupérées avec succès ✅")


# DATA CLEANING
data = response.json()

instruments = data["instruments"]

print(f"Nous avons accés a {len(instruments)} instruments différents")

instrument_data = []

for item in instruments:
    # Pour chaque item, je récupère uniquement les données qui m'intéressent
    new_obj = dict(
        name=item["name"],
        type=item["type"],
        displayName=item["displayName"],
        pipLocation=item["pipLocation"],
        marginRate=item["marginRate"],
    )
    instrument_data.append(new_obj)


# Insertion des données dans un dataframe pandas pour faciliter leur exportation
instrument_df = pd.DataFrame.from_dict(instrument_data)

# Exportation du dataframe dans un fichier pickle (binaire)
# Possibilité de le sauvegarder dans un autre format comme CSV, etc.
instrument_df.to_pickle("instruments_perso.pkl")
print("Exportation terminée avec succès ✅")
