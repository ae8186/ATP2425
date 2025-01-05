from collections import Counter
import json

# HELP
def ajuda():
    print("""
          (1) Criar Publicação
          (2) Consultar Publicação
          (3) Consultar/Filtrar Publicações
          (4) Eliminar Publicação
          (5) Relatório de Estatísticas
          (6) Listar Autores
          (7) Importar Publicações
          (8) Guardar Publicações
          (9) Sair
          """)
    return


# CRIAR ARTIGO
def cria_artigo():
    titulo = str(input("Introduza o título do artigo"))
    resumo = str(input("Pode digitar o resumo do artigo"))
    palavrachave = str(input("Introduza as palavras chaves relacionadas "))
    doi = str(input("Introduza o número identificador do artigo"))
    data = cria_data()
    num = int(input("Introduza o número de autores do artigo"))
    autores = []
    for i in range(0,num):
        nome = str(input("Introduza o nome do autor"))
        afil = str(input("Introduza a afiliação do autor"))
        autores.append({
            "name":nome,
            "affiliation":afil
        })
    url = str(input("Introduza o url do artigo"))
    pdf = str(input("Introduza o url do pdf"))
    artigo = {
        "title":titulo,
        "abstract":resumo,
        "keywords":palavrachave,
        "doi":doi,
        "url":url,
        "pdf":pdf,
        "publish_date":data,
        "authors":autores
    }
    print("Artigo criado com sucesso.")
    return artigo

def cria_data():
    a = 3000
    while a < 0 or a > 2025:
        a = int(input("Introduza o ano"))
    m = 13
    while m < 1 or m > 12:
        m = int(input("Introduza o mês"))
    d = 40
    if m in [11,4,6,9]:
        while d < 0 or d > 30:
            d = int(input("Introduza o dia"))

    elif m in [1,3,5,7,8,10,12]:
        while d < 0 or d > 31:
            d = int(input("Introduza o dia"))
    else:
        if a % 4 == 0:
            while d < 0 or d > 29:
                d = int(input("Introduza o dia"))
        else:
            while d < 0 or d > 28:
                d = int(input("Introduza o dia"))
    data = str(a) + "-" + str(m) + "-" + str(d)
    return data

# CONSULTAR PUBLICAÇÃO
def consulta_artigo(artigos, doi):
    for elem in artigos:
        if elem["doi"] == doi:
            print("Título:", elem['title'])
            print("Data:", elem['publish_date'])
            print("Resumo:", elem['abstract'])
            print("Autores:", ', '.join([aut['name'] for aut in elem['authors']]))
            print("Palavras-chave:", elem['keywords'])
            
    return


# CONSULTAR PUBLICAÇÕES

def consulta_publicacoes(artigos):
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
        resultados = [a for a in artigos if busca in [kw.strip().lower() for kw in a['keywords'].split(',')]]

    else:
        print("Opção inválida!")
        return

    for r in resultados:
        print(f"Título: {r['title']}")
        print(f"Autores: {', '.join([aut['name'] for aut in r['authors']])}")
        print(f"Data: {r['publish_date']}")
        print(f"Palavras-chave: {r['keywords']}")
        print(f"DOI: {r['doi']}")
        print(f"URL: {r['url']}")
        print("-" * 50)
    

# ELIMINAR PUBLICAÇÃO 
def eliminar_publicacao(artigos, doi):
    # Verifica se o DOI existe
    for i, artigo in enumerate(artigos):
        if artigo["doi"] == doi:
            # Remove o artigo encontrado
            del artigos[i]
            print(f"Publicação com DOI {doi} eliminada com sucesso!")
            return artigos
    # Caso o DOI não seja encontrado
    print(f"Nenhuma publicação encontrada com o DOI {doi}.")
    return artigos

# RELATÓRIO DE ESTATÍSTICAS
def estat(artigos):
    palavras = []
    for artigo in artigos:
        palavras.extend(artigo['keywords'].lower().split(','))
    contagempalchave = Counter([p.strip() for p in palavras])
    
    anos = [artigo['publish_date'][:4] for artigo in artigos]
    contagemanos = Counter(anos)
    
    autores = []
    for artigo in artigos:
        for autor in artigo['authors']:
            autores.append(autor['name'])
    contagemautores = Counter(autores)
    
    print(contagemanos, contagempalchave, contagemautores)
    return


# LISTAR AUTORES
def listar_autores(artigos):
    a = []
    autores = []
    for elem in artigos:
        a.append(elem['authors'])
        for x in a:
            if x['name'] not in autores:
                autores.append(x['name'])
    return autores

# IMPORTAR PUBLICAÇÕES
def importar_publicacoes(ficheiro, artigos):
    with open(ficheiro, 'r', encoding='utf-8') as f:
        novos_artigos = json.load(f)
        artigos.extend(novos_artigos)
    print("Publicações importadas com sucesso!")

# Exportar Publicações
def exportar_publicacoes(ficheiro, artigos):
    with open(ficheiro, 'w', encoding='utf-8') as f:
        json.dump(artigos, f, indent=4)
    print("Resultados exportados com sucesso!")

# GUARDAR PUBLICAÇÕES
def gravar(artigos,fnome): 
    f = open(fnome,"w",encoding="utf-8") 
    json.dump(artigos,f) 
    return


def menu():
    with open("ata_medica_papers.json", encoding='utf-8') as f:
        artigos = json.load(f)
    while True:
        v = str(input())
        if v == "help":
            ajuda()
        elif v == "1":
            artigos.append(cria_artigo())
        elif v == "2":
            doi = str(input("Introduza o DOI da publicação a consultar:"))
            consulta_artigo(artigos, doi)
        elif v == "3":
            consulta_publicacoes(artigos)
        elif v == "4":
            doi = str(input("Introduza o DOI da publicação a eliminar:"))
            artigos = eliminar_publicacao(artigos, doi)
        elif v == "5":
            estat(artigos)
        elif v == "6":
            listar_autores(artigos)
        elif v == "7":
            ficheiro = input("Digite o caminho do ficheiro a importar: ")
            importar_publicacoes(ficheiro, artigos)
        elif v == "8":
            ficheiro = input("Digite o caminho do ficheiro para exportar: ")
            exportar_publicacoes(ficheiro, artigos)
        elif v == "9":
            gravar(artigos, "ata_medica_papers.json")
        elif v == "10":
            break
menu()