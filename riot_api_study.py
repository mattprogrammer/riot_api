from api_riot.lol import lol_api as lol

def main():
    nome = input("Digite seu nome de invovador:")
    game_tag = input("Digite sua #TAG:")
    
    try:
        puuid = lol.get_puuid(nome, game_tag)
        match_ids = lol.get_match_ids(puuid)
    except Exception as ex:
        print(f"Não foi possível encontrar o invocador. Erro: {ex}")
    
    print("O que deseja fazer?")
    tipo_processo = input("1 - Saber meu pior campeão.    2 - Saber meu melhor campeão.     3 - Últimos 10 campeões jogados.")
    
    
    if tipo_processo == "3":
        for match_id in match_ids:
            match_details = lol.get_match_details(match_id)
                
            player_data = next(player for player in match_details["info"]["participants"] if player["puuid"] == puuid)
                
            champion_name = player_data["championName"]
            print(champion_name)
            

    if tipo_processo == "1":
        