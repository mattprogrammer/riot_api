from api_riot.lol import lol_api as lol

def main():
    nome = input("Digite seu nome de invovador:")
    game_tag = input("Digite sua #TAG:")
    
    try:
        puuid = lol.get_puuid(nome, game_tag)
        
    except Exception as ex:
        print(f"Não foi possível encontrar o invocador. Erro: {ex}")
        return
    
    print("Invocador encontrado, o que deseja fazer?")
    print("1 - Qual meu pior campeão?")
    print("2 - Qual meu melhor campeão?")
    print("3 - Meus ultimos 10 campeões jogados.")
    print("0 - Cancelar")
    
    while True:
        tipo_processo = input("Digite sua escolha: ")

        if tipo_processo == "1":
            quantidade_jogos = int(input("Insira a quantidade de jogos a serem consultados: "))
            lol.get_worst_champions(nome, game_tag, quantidade_jogos)

        elif tipo_processo == "2":
            quantidade_jogos = int(input("Insira a quantidade de jogos a serem consultados: "))
            if nome == "caçaratoprime": 
                print("Este invocador é péssimo com todos campeões.") 
                return
            lol.get_best_champions(nome, game_tag, quantidade_jogos)

        elif tipo_processo == "3":
            match_ids = lol.get_match_ids(puuid, 10)
            lol.get_last_champions(match_ids, puuid)

        elif tipo_processo == "0":
            return

        else:
            print("Opção inválida!")

main()