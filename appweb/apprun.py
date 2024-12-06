from flask import Flask, render_template
import requests
from collections import Counter
import os
from waitress import serve

API_BASE_URL = "https://api.opendota.com/api"

#load the API key from environment variables
API_KEY = os.getenv("API_KEY")

GAME_MODE_NAMES = {
    3: "Random Draft",
    4: "Single Draft",
    22: "All Pick Ranked",
}

app = Flask(__name__)

#fetch public matches
def get_recent_matches(limit=1000):
    endpoint = f"{API_BASE_URL}/publicMatches"
    matches = []
    last_match_id = None

    while len(matches) < limit:
        params = {"less_than_match_id": last_match_id, "api_key": API_KEY} if last_match_id else {"api_key": API_KEY}
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            matches.extend(data)
            last_match_id = data[-1].get("match_id")
        else:
            print(f"Failed to fetch matches: {response.status_code}")
            break

    return matches[:limit]

#Calculate winrate
def calculate_winrate(matches):
    radiant_wins = sum(1 for match in matches if match.get("radiant_win"))
    total_matches = len(matches)
    radiant_winrate = (radiant_wins / total_matches) * 100 if total_matches > 0 else 0
    dire_winrate = 100 - radiant_winrate
    return radiant_winrate, dire_winrate

#Calculate match duration distribution
def get_match_duration_distribution(matches):
    bins = [0, 20, 40, 60, 80]
    distribution = {f"{bins[i]}-{bins[i+1]}": 0 for i in range(len(bins) - 1)}
    distribution["80+"] = 0

    for match in matches:
        duration_minutes = match.get("duration", 0) // 60
        added_to_bin = False
        for i in range(len(bins) - 1):
            if bins[i] <= duration_minutes < bins[i + 1]:
                distribution[f"{bins[i]}-{bins[i+1]}"] += 1
                added_to_bin = True
                break
        if not added_to_bin and duration_minutes >= 80:
            distribution["80+"] += 1

    return distribution

#Count games by game mode
def get_games_per_game_mode(matches):
    game_modes = Counter()
    for match in matches:
        game_mode = match.get("game_mode")
        if game_mode is not None:
            game_modes[game_mode] += 1
    return {GAME_MODE_NAMES.get(mode, f"Mode {mode}"): count for mode, count in game_modes.items()}

@app.route("/")
def index():
    #Fetch data
    matches = get_recent_matches(limit=1000)
    radiant, dire = calculate_winrate(matches)
    duration_distribution = get_match_duration_distribution(matches)
    game_mode_distribution = get_games_per_game_mode(matches)

    #Pass the data to the template
    return render_template(
        "index.html",
        radiant=radiant,
        dire=dire,
        duration_distribution=duration_distribution,
        game_mode_distribution=game_mode_distribution,
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

