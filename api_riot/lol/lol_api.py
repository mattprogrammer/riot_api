import requests
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

API_KEY = "RGAPI-cc058fdd-87dc-4149-9c1d-cff3e7bb22ae"
REGION = "br1" 
PLATFORM = "americas"

def get_puuid(nome, tag):
    """Obtem o PUUID do invocador."""
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nome}/{tag}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["puuid"]

def get_match_ids(puuid, count):
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

@app.get("/lol/ultimos_campeoes")
def get_last_champions(partidas, puuid):
        champion_name_formatted = ""
        for match_id in partidas:
            match_details = get_match_details(match_id)
                
            player_data = next(player for player in match_details["info"]["participants"] if player["puuid"] == puuid)
                
            champion_name = player_data["championName"]
            champion_name_formatted += f", {champion_name}" if champion_name_formatted != "" else champion_name

        print(f"Seus últimos 10 campeões foram: {champion_name_formatted}")
    
    
@app.get("/lol/piores-campeoes")
def get_worst_champions(nome, game_tag, numero_partidas):
    rank = obtem_rank_campeoes(nome, game_tag, numero_partidas)
    print(f"Seu pior campeão foi {rank.iloc[-1]['campeao']}, com um KDA médio de {rank.iloc[-1]['media_kda']}")
    return {"message": f"Seu pior campeão foi {rank.iloc[-1]['campeao']}, com um KDA médio de {rank.iloc[-1]['media_kda']}"}

@app.get("/lol/melhores-campeoes")
def get_best_champions(nome, game_tag, numero_partidas):
    rank = obtem_rank_campeoes(nome, game_tag, numero_partidas)
    print(f"Seu melhor campeão foi {rank.iloc[0]['campeao']}, com um KDA médio de {rank.iloc[0]['media_kda']}")
    return {"message": f"Seu melhor campeão foi {rank.iloc[0]['campeao']}, com um KDA médio de {rank.iloc[0]['media_kda']}"}
    
def calculo_efetividade_por_campeao(lista_campeoes):
    resultado = lista_campeoes.groupby('campeao').agg(
        total_kda=('kda', 'sum'), 
        num_partidas=('kda', 'count'))

    resultado['media_kda'] = resultado['total_kda'] / resultado['num_partidas']

    return resultado.sort_values(by='media_kda', ascending=False).reset_index()

def obtem_rank_campeoes(nome, game_tag, numero_partidas):    
    puuid = get_puuid(nome, game_tag)
    partidas = get_match_ids(puuid, numero_partidas)
    lista_campeoes = pd.DataFrame(columns=["campeao", "kda", "vitória"])
    
    for partida in partidas:
        detalhes = get_match_details(partida)

        invocador = next(player for player in detalhes["info"]["participants"] if player["puuid"] == puuid)
        
        kills = invocador["kills"]
        deaths = invocador["deaths"]
        assists = invocador["assists"]

        kda = (kills + assists) / deaths if deaths != 0 else kills + assists
        kda = round(kda, 2)
        
        dados = [invocador["championName"], kda, invocador["win"]]
        lista_campeoes.loc[len(lista_campeoes)] = dados

        # usando .concat, que seria uma maneira de resposta mais rápida
        # lista_campeoes = pd.concat([lista_campeoes, pd.DataFrame(dados, columns=lista_campeoes.columns)], ignore_index=True)
    
    rank_campeoes = calculo_efetividade_por_campeao(lista_campeoes)

    return rank_campeoes