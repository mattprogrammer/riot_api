import requests;

API_KEY = "RGAPI-e7760ebe-c3c2-48ee-982f-f54cf4db0191"
REGION = "br1" 
PLATFORM = "americas"

def get_puuid(nome, tag):
    """Obtem o PUUID do invocador."""
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nome}/{tag}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["puuid"]

def get_match_ids(puuid, count=10):
    """Obtem IDs das partidas."""
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_match_details(match_id):
    """Obtem detalhes de uma partida."""
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

nome = "PowerPoint 2010"
game_tag = "OFFIC"
puuid = get_puuid(nome, game_tag)
match_ids = get_match_ids(puuid)

for match_id in match_ids:
    match_details = get_match_details(match_id)
    
    player_data = next(player for player in match_details["info"]["participants"] if player["puuid"] == puuid)
    
    champion_name = player_data["championName"]
    print(champion_name)