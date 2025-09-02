# Ce script collecte les données des 10 dernières bougies de l'EURUSD si elles sont complètes

import requests
import pandas as pd
import sys, os

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.insert(0, parent_dir)

import defs

# Création d'un objet session
session = requests.Session()

# Défintion de mes paramètres
instrument = "EUR_USD"

params = dict(
    count = 10,
    granularity = "H1",
    price= 'MBA'
)
    

# Construction de l'URL
url = f'{defs.OANDA_URL}/instruments/{instrument}/candles'

response = session.get(url, params=params, headers= defs.SECURE_HEADER)

print(response.status_code)

if response.status_code == 200:
    print("Données récupérées avec succès ✅")

data = response.json()

# Vérification du nombre de bougies récupérer 
print(f"Nombre de bougies récupérées : {len(data["candles"])}")

# Récupération des données qui nous intéressent pour chaque bougie
prices = ["mid", "bid", "ask"]
ohlc = ["o", "h", "l", "c"]

clean_data = []

for candle in data["candles"]:
    if candle["complete"] == False:
        continue
    new_dict = {}
    new_dict["time"] = candle["time"]
    new_dict["volume"] = candle["volume"]
    for price in prices:
        for oh in ohlc:
            new_dict[f"{price}_{oh}"] = candle[price][oh]
    clean_data.append(new_dict)


candles_df = pd.DataFrame.from_dict(clean_data)

# Exportation des données en CSV

candles_df.to_csv("eu_data.csv")
print("Exportation terminée avec succès ✅")