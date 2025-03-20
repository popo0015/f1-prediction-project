import requests
import pandas as pd

def fetch_f1_results(year=2024):
    url = f"http://ergast.com/api/f1/{year}/results.json"
    response = requests.get(url)
    return response.json()

data = fetch_f1_results()
df = pd.json_normalize(data["MRData"]["RaceTable"]["Races"])
print(df.head())  # Display live data, no storage
