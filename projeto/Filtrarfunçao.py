def consulta_publicacoes(artigos):
    """
    Pesquisa publicações com base em filtros.
    """
    print("Filtros disponíveis:")
    print("1. Título")
    print("2. Autor")
    print("3. Afiliação")
    print("4. Data de Publicação")
    print("5. Palavras-chave")
    filtro = int(input("Escolha um filtro (1-5): "))

    resultados = []

    if filtro == 1:  # Filtro por título
        busca = input("Escreva o título ou parte dele: ").lower()
        resultados = [a for a in artigos if busca in a['title'].lower()]

    elif filtro == 2:  # Filtro por autor
        busca = input("Escreva o nome do autor: ").lower()
        resultados = [a for a in artigos if any(busca in aut['name'].lower() for aut in a['authors'])]

    elif filtro == 3:  # Filtro por afiliação
        busca = input("Escreva a afiliação: ").lower()
        resultados = [a for a in artigos if any(busca in aut['affiliation'].lower() for aut in a['authors'])]

    elif filtro == 4:  # Filtro por data de publicação
        busca = input("Escreva a data (YYYY-MM-DD): ")
        resultados = [a for a in artigos if a['publish_date'] == busca]

    elif filtro == 5:  # Filtro por palavras-chave
        busca = input("Escreva uma palavra-chave: ").lower()
        resultados = [a for a in artigos if busca in a['keywords'].lower()]

    else:
        print("Opção inválida!")
        return

    # Ordenar os resultados
    if resultados:
        print("Ordenar resultados por:")
        print("1. Título")
        print("2. Data de publicação")
        ordem = int(input("Escolha a ordenação (1-2): "))

        if ordem == 1:
            resultados = sorted(resultados, key=lambda x: x['title'].lower())
        elif ordem == 2:
            resultados = sorted(resultados, key=lambda x: x['publish_date'])

        # Mostra os resultados
        for r in resultados:
            print(f"\nTítulo: {r['title']}")
            print(f"Autores: {', '.join([aut['name'] for aut in r['authors']])}")
            print(f"Data: {r['publish_date']}")
            print(f"Palavras-chave: {r['keywords']}")
            print(f"DOI: {r['doi']}")
            print(f"URL: {r['url']}")
            print("-" * 50)
    else:
        print("Nenhuma publicação foi encontrada.")
