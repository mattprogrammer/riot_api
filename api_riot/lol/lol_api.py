import requests
from fastapi import FastAPI

app = FastAPI()

API_KEY = "RGAPI-c016c62a-c0c3-4c6d-9e37-dd9201442eb4"
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
    pior_campeao = next(iter(reversed(rank.items())))
    print(f"Seu pior campeão foi {pior_campeao[0]}, com um KDA médio de {pior_campeao[1]}")
    return {"message": f"Seu pior campeão foi {pior_campeao[0]}, com um KDA médio de {pior_campeao[1]}"}

@app.get("/lol/melhores-campeoes")
def get_best_champions(nome, game_tag, numero_partidas):
    rank = obtem_rank_campeoes(nome, game_tag, numero_partidas)
    melhor_campeao = next(iter(rank.items()))
    print(f"Seu melhor campeão foi {melhor_campeao[0]}, com um KDA médio de {melhor_campeao[1]}")
    return {"message": f"Seu melhor campeão foi {melhor_campeao[0]}, com um KDA médio de {melhor_campeao[1]}"}
    
def calculo_efetividade_por_campeao(lista_campeoes):
    total_campeao = {}
    
    for registro in lista_campeoes:
        campeao = registro['campeao']
        kda = registro['kda']
        
        if campeao not in total_campeao:
            total_campeao[campeao] = {'total_kda': 0, 'jogos': 0}
            
        total_campeao[campeao]['total_kda'] += kda
        total_campeao[campeao]['jogos'] += 1
    
    medias_kda = {}
    for campeao, dados in total_campeao.items():
        medias_kda[campeao] = dados['total_kda'] / dados['jogos']
    
    rank_campeoes = dict(sorted(medias_kda.items(), key=lambda item: item[1], reverse=True))       
    return rank_campeoes

def obtem_rank_campeoes(nome, game_tag, numero_partidas):    
    puuid = get_puuid(nome, game_tag)
    partidas = get_match_ids(puuid, numero_partidas)
    
    lista_campeoes = []
    
    for partida in partidas:
        detalhes = get_match_details(partida)

        invocador = next(player for player in detalhes["info"]["participants"] if player["puuid"] == puuid)
        
        kills = invocador["kills"]
        deaths = invocador["deaths"]
        assists = invocador["assists"]
        
        kda = (kills + assists) / deaths
        kda = round(kda,2)
        
        campeoes_utilizados = {"campeao": invocador["championName"],
                                "kda": kda,
                                "vitória": invocador["win"]}
        
        lista_campeoes.append(campeoes_utilizados)
        
    rank_campeoes = calculo_efetividade_por_campeao(lista_campeoes)

    return rank_campeoes