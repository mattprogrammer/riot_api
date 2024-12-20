import requests;

API_KEY = "RGAPI-e52ac9f7-af74-43ba-9d7a-df97c57bda33"
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