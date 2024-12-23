from api_riot.lol import lol_api as lol

def main():
    nome = input("Digite seu nome de invovador:")
    game_tag = input("Digite sua #TAG:")
    
    try:
        puuid = lol.get_puuid(nome, game_tag)
        match_ids = lol.get_match_ids(puuid, 10)
        
    except Exception as ex:
        print(f"Não foi possível encontrar o invocador. Erro: {ex}")
    
    print("Invocador encontrado, o que deseja fazer?")
    print("1 - Qual meu pior campeão?    2 - Qual meu melhor campeão?    3 - Últimos 10 campeões jogados.")
    tipo_processo = input("Digite sua escolha:")
    
    if tipo_processo == "1":
        quantidade_jogos = int(input("Insira a quantidade de jogos a serem consultados:"))
        lol.get_worst_champions(nome, game_tag, quantidade_jogos)
        
    if tipo_processo == "2":
        quantidade_jogos = int(input("Insira a quantidade de jogos a serem consultados:"))
        lol.get_best_champions(nome, game_tag, quantidade_jogos)
        
    if tipo_processo == "3":
        lol.get_last_champions(match_ids, puuid)

def teste():
    lol.get_worst_champions("PowerPoint 2010", "OFFIC", 3)
    
teste()