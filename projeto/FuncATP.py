import json
from collections import Counter
import matplotlib.pyplot as plt
import PySimpleGUI as sg

# Importa o dataset e atualiza-o (PONTO 1 e 8)
def abre_ficheiro(fnome):
    f = open(fnome, encoding='utf-8')
    novo = json.load(f)
    for elem in novo:
        elem['publish_date'] = "2025-01-05"
        elem['keywords'] = "oi"
    f.close()
    return novo

def barra_pesquisa(artigos, titulo):
    for elem in artigos:
        if elem['title'] == titulo:
            return elem
    return None

def cria_dados(artigos):
    l = []
    for elem in artigos:
        autores = elem["authors"]
        nomes = []
        afiliacao = []
        for aut in autores:
            nomes.append(aut["name"])
        nl = [str(elem["title"]), nomes, afiliacao, elem["doi"]]
        l.append(nl)
    return l

def gravar(artigos,fnome): 
    f = open(fnome,"w",encoding="utf-8") 
    json.dump(artigos,f) 
    return


#Cria a publicação- PONTO 2
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
    return artigo


# Cria a data para a criação da publicação
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

#Atualiza os artigos de acordo com os parametros definidos- PONTO 3

def atualiza_data(artigos, doi):
    datan = cria_data()
    for elem in artigos:
        if elem["doi"] == doi:
            elem["publish_date"] = datan
    return artigos

    
def atualiza_resumo(artigos, doi):
    resumon = str(input("Introduza um novo resumo"))
    for elem in artigos:
        if elem["doi"] == doi:
            elem["abstract"] = resumon
    return artigos


def atualiza_key(artigos, doi):
    chaven = str(input("Introduza novas palavras chave!"))
    for elem in artigos:
        if elem["doi"] == doi:
            elem["keywords"] == chaven
    return artigos


def atualiza_autores(artigos, doi):
    listaut = []
    a = int(input("Qual o número de autores que deseja introduzir?"))
    while a > 0:
        b = str(input("Nome do autor"))
        listaut.append(b)
        a = a - 1
    for elem in artigos:
        if elem["doi"] == doi:
            elem["authors"] == listaut
    return artigos

def atualiza_afiliacoes(artigos, doi):
    afi = []
    t = int(input("Introduz o número de afiliações"))
    while t > 0:
        c = str(input("Introduza a afiliação."))
        afi.append(c)
        t = t - 1
    for elem in artigos:
        if elem["doi"] == doi:
            elem["authors"]["affiliation"] = afi
    return artigos

# Consultar os artigos com filtros - PONTO 4

def consulta_artigo(artigos, titulo):
    for elem in artigos:
        if elem["title"] == titulo:
            print(elem)
    return

def ordena_artigos(artigos):
    pass




# GRAFICOS         
def grafico_publicacoes_por_ano(artigos):
    print(artigo for artigo in artigos)
    anos = [artigo['publish_date'][:4] for artigo in artigos]
    contagem = Counter(anos)
    plt.figure(figsize=(10, 6))
    plt.bar(contagem.keys(), contagem.values())
    plt.xlabel('Ano')
    plt.ylabel('Número de Publicações')
    plt.title('Distribuição de Publicações por Ano')
    plt.tight_layout()
    plt.show()
    return

def grafico_publicacoes_por_mes(artigos):
    ano_escolhido = sg.popup_get_text("Digite o ano para análise (YYYY):")
    meses = [artigo['publish_date'][5:7] for artigo in artigos if artigo['publish_date'][:4] == ano_escolhido]
    contagem = Counter(meses)
    plt.figure(figsize=(10, 6))
    plt.bar(contagem.keys(), contagem.values())
    plt.xlabel('Mês')
    plt.ylabel('Número de Publicações')
    plt.title(f'Distribuição de Publicações por Mês em {ano_escolhido}')
    plt.tight_layout()
    plt.show()
    return

def grafico_top_autores(artigos):
    autores = []
    for artigo in artigos:
        for autor in artigo['authors']:
            autores.append(autor['name'])
    contagem = Counter(autores)
    top_autores = contagem.most_common(20)
    nomes, contagens = zip(*top_autores)
    plt.figure(figsize=(10, 6))
    plt.barh(nomes, contagens)
    plt.xlabel('Número de Publicações')
    plt.title('Top 20 Autores com Mais Publicações')
    plt.tight_layout()
    plt.show()
    return

def grafico_publicacoes_por_autor(artigos):
    autor_escolhido = sg.popup_get_text("Digite o nome do autor:")
    anos = []
    for artigo in artigos:
        for autor in artigo['authors']:
            if autor['name'].lower() == autor_escolhido.lower():
                anos.append(artigo['publish_date'][:4])
    contagem = Counter(anos)
    plt.figure(figsize=(10, 6))
    plt.bar(contagem.keys(), contagem.values())
    plt.xlabel('Ano')
    plt.ylabel('Número de Publicações')
    plt.title(f'Distribuição de Publicações de {autor_escolhido} por Ano')
    plt.tight_layout()
    plt.show()
    return

def grafico_top_palavras_chave(artigos):
    palavras = []
    for artigo in artigos:
        palavras.extend(artigo['keywords'].lower().split(','))
    contagem = Counter([p.strip() for p in palavras])
    top_palavras = contagem.most_common(20)
    termos, contagens = zip(*top_palavras)
    plt.figure(figsize=(10, 6))
    plt.barh(termos, contagens)
    plt.xlabel('Frequência')
    plt.title('Top 20 Palavras-chave mais Frequentes')
    plt.tight_layout()
    plt.show()
    return

def grafico_palavras_chave_por_ano(artigos):
    ano_escolhido = sg.popup_get_text("Digite o ano para análise (YYYY):")
    palavras = []
    for artigo in artigos:
        if artigo['publish_date'][:4] == ano_escolhido:
            palavras.extend(artigo['keywords'].lower().split(','))
    contagem = Counter([p.strip() for p in palavras])
    top_palavras = contagem.most_common(10)
    termos, contagens = zip(*top_palavras)
    plt.figure(figsize=(10, 6))
    plt.barh(termos, contagens)
    plt.xlabel('Frequência')
    plt.title(f'Top 10 Palavras-chave mais Frequentes em {ano_escolhido}')
    plt.tight_layout()
    plt.show()
    return