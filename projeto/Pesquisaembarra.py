import PySimpleGUI as sg
import json
from collections import Counter
from FuncATP import abre_ficheiro, cria_dados, gravar


# Tema e carregamento de dados
sg.theme('Dark Purple')
artigos = abre_ficheiro("ata_medica_papers.json")
dados = cria_dados(artigos)


# Criar nova janela para exibir detalhes do artigo
def criar_nova_janela(novos_dados):
    layout = [[sg.Text("Título:"), sg.Text(novos_dados["title"])],
              [sg.Multiline(novos_dados["abstract"], size=(50, 10))],
              [sg.Text(novos_dados["url"])],
              [sg.Text(novos_dados["doi"])],
              [sg.Text(novos_dados["pdf"])],
              [sg.Text(novos_dados["authors"][0]["name"]), sg.Button('Eliminar')]
              ]
    return sg.Window('Artigo', layout, modal=True, size=(500, 300))


# Função para encontrar artigo pelo DOI
def achar_artigo(id, artigos):
    for elem in artigos:
        if id == elem["doi"]:
            return elem


# Funções de Geração de Gráficos
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


# Interface principal com barra de pesquisa
layout = [
    [sg.Text("Pesquisa:"), sg.Input(key='-SEARCH-', size=(80, 1)), sg.Button('Procurar')],
    [sg.Listbox(values=dados, key='-TABELA-', size=(150, 30), enable_events=True)],
    [sg.ButtonMenu('Ordenar', ['Ordenar', ["Título", "Data", "Autor", "Afiliação"]], key='Ordenar'),
     sg.Button('Gráficos'), sg.Button('Gravar'), sg.Button('Sair')]
]

window = sg.Window('Artigos', layout, finalize=True)


# Loop principal
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break

    # Pesquisar
    if event == 'Procurar':
        query = values['-SEARCH-'].strip().lower()
        resultados = [
            a for a in artigos if
            query in a['title'].lower() or
            query in ','.join([aut['name'].lower() for aut in a['authors']]) or
            query in a['keywords'].lower() or
            query in a['publish_date']
        ]
        dados = cria_dados(resultados)
        window['-TABELA-'].update(values=dados)

    # Gráficos
    if event == 'Gráficos':
        grafico = sg.popup_get_text(
            'Escolha o gráfico: \n1. Por Ano\n2. Por Mês\n3. Top Autores\n4. Autor por Ano\n5. Top Palavras\n6. Palavras por Ano')
        if grafico == '1':
            grafico_publicacoes_por_ano(artigos)
        elif grafico == '2':
            grafico_publicacoes_por_mes(artigos)
        elif grafico == '3':
            grafico_top_autores(artigos)
        elif grafico == '4':
            grafico_publicacoes_por_autor(artigos)
        elif grafico == '5':
            grafico_top_palavras_chave(artigos)
        elif grafico == '6':
            grafico_palavras_chave_por_ano(artigos)

    # Gravação
    if event == 'Gravar':
        gravar(artigos, "ata_medica_papers.json")
        sg.popup("Dados salvos com sucesso!")

    window.refresh()

window.close()
