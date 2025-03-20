import requests
import pandas as pd

def fetch_f1_results(season: int = 2023, top_n: int = 10) -> pd.DataFrame:
    """Fetches race results for a given F1 season and includes top_n drivers per race."""
    url = f"http://ergast.com/api/f1/{season}/results.json?limit=1000"
    response = requests.get(url)
    data = response.json()

    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        print(f"No race data found for season {season}")
        return pd.DataFrame()

    # Extract relevant information
    results = []
    for race in races:
        race_name = race["raceName"]
        round_num = int(race["round"])
        circuit = race["Circuit"]["circuitName"]
        date = race["date"]
        for result in race["Results"][:top_n]:  # Now includes top N drivers
            driver = result["Driver"]["familyName"]
            constructor = result["Constructor"]["name"]
            grid_pos = int(result["grid"])
            position = int(result["position"])  # Their final race position

            results.append([season, round_num, race_name, circuit, date, driver, constructor, grid_pos, position])

    # Convert to Pandas DataFrame
    columns = ["Season", "Round", "Race", "Circuit", "Date", "Driver", "Constructor", "Grid Position", "Final Position"]
    df = pd.DataFrame(results, columns=columns)

    return df

# Example: Fetch 2023 data with top 10 drivers per race
df = fetch_f1_results(2023)
print(df.head())  # Show processed data
