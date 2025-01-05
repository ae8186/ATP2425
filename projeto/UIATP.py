from FuncATP import *
from Filtrarfunçao import *
import matplotlib.pyplot as plt
sg.theme('Dark Purple')
artigos = abre_ficheiro("ata_medica_papers.json")
dados = cria_dados(artigos)

# Tema e carregamento de dados
def criar_nova_janela(novos_dados):
    layout = [[sg.Text("Título:"),sg.Text(novos_dados["title"])],
              [sg.Multiline(novos_dados["abstract"], size=(400,10))],
              [sg.Text(novos_dados["url"])],
              [sg.Text(novos_dados["doi"])],
              [sg.Text(novos_dados["pdf"])],
              [sg.Text(novos_dados["authors"][0]["name"]), sg.Button('Eliminar')]
              ]
    return sg.Window('Artigo', layout, modal=True, size=(500,500))



def janela_criar_artigo():
    layout = [[sg.Text('Título:'), sg.Input(key='-NOVOTITULO-'),sg.Text('Data:'), sg.Input(key='-NOVODATA-')],
              [sg.Text('Resumo:'), sg.Input( key='-NOVORESUMO-')],
              [sg.Text('doi:'), sg.Input(key='-NOVODOI-')],
              [sg.Text('pdf:'), sg.Input(key='-NOVOPDF-')],
              [sg.Text('Autores:'), sg.Input(key='-NOVOAUTOR-')],
              [sg.Text('Afiliações:'), sg.Input(key='-NOVOAFILIACAO-')],
              [sg.Text('Url:'), sg.Input(key='-NOVOURL-')],
              [sg.Text('Palavras-chave:'), sg.Input(key='-NOVOKEYWORDS-')],
              [sg.Button("Criar", key='-CRIAARTIGO-')]
              ]
    return sg.Window('Criar', layout, modal=True, size=(500,500))

# Interface principal
layout = [
    [sg.Text("Pesquisa:"), sg.Input(key='-SEARCH-', size=(80, 1)), sg.Button('Procurar')],
    [sg.Listbox(values=dados, key='-TABELA-', size=(150, 30), enable_events=True)],
    [sg.ButtonMenu('Ordenar', ['Ordenar', ["Título", "Data", "Autor", "Afiliação"]], key='Ordenar'),
    sg.Button('Criar'), sg.Button('Filtrar'), sg.Button('Gráficos'), sg.Button('Gravar'), sg.Button('Sair')]
]

window = sg.Window('Artigos', layout, finalize=True)

# Função para pesquisa dinâmica
def pesquisa(artigos, query):
    query = query.lower().strip()
    return [a for a in artigos if (
        query in a['title'].lower() or
        any(query in aut['name'].lower() for aut in a['authors']) or
        query in a['keywords'].lower() or
        query in a['publish_date'])]

# Função de filtro com campos
def filtrar_artigos(artigos):
    filtro = sg.popup_get_text("Escolha o filtro: Título, Autor, Afiliação, Data ou Palavra-chave:").lower()
    busca = sg.popup_get_text("Digite o valor para filtro:").lower()
    resultados = []

    if filtro == 'título':
        resultados = [a for a in artigos if busca in a['title'].lower()]
    elif filtro == 'autor':
        resultados = [a for a in artigos if any(busca in aut['name'].lower() for aut in a['authors'])]
    elif filtro == 'afiliação':
        resultados = [a for a in artigos if any(busca in aut['affiliation'].lower() for aut in a['authors'])]
    elif filtro == 'data':
        resultados = [a for a in artigos if a['publish_date'] == busca]
    elif filtro == 'palavra-chave':
        resultados = [a for a in artigos if busca in [kw.strip().lower() for kw in a['keywords'].split(',')]]
    else:
        sg.popup("Filtro inválido!")
        return artigos

    return resultados

# Função de gráficos para palavras-chave
def grafico_top_palavras_chave(artigos):
    palavras = []
    for artigo in artigos:
        palavras.extend([p.strip().lower() for p in artigo['keywords'].split(',')])
    contagem = Counter(palavras)
    top_palavras = contagem.most_common(20)
    termos, contagens = zip(*top_palavras)
    plt.figure(figsize=(10, 6))
    plt.barh(termos, contagens)
    plt.xlabel('Frequência')
    plt.title('Top 20 Palavras-chave mais Frequentes')
    plt.tight_layout()
    plt.show()

def achar_artigo(id, artigos):
    for artigo in artigos:
        if id == artigo["doi"]:
            a = artigo
    return a


# Loop principal
while True:

    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break

    if event == '-TABELA-':
        id = values['-TABELA-'][0]
        artigo_escolhido = achar_artigo(id[-1], artigos)
        janela_info = criar_nova_janela(artigo_escolhido)
        while True:
            nevent, nvalues = janela_info.read()
            if nevent in (sg.WINDOW_CLOSED, 'Close'):
                janela_info.close()
                break
            
                    
            if nevent == 'Eliminar':
                artigos.remove(artigo_escolhido)
                janela_info.close()
                dados = cria_dados(artigos)
                window['-TABELA-'].update(values = dados)
                break
    
    if event == 'Ordenar':
        v = values['Ordenar']
        if v == "Título":
            artigos.sort(key=lambda x: x['title'])
            dados = cria_dados(artigos)
            window['-TABELA-'].update(values = dados)
        elif v == "Data":
            artigos.sort(key=lambda x: x['publish_date'])
            dados = cria_dados(artigos)
            window['-TABELA-'].update(values = dados)
        elif v == "Autor":
            artigos.sort(key=lambda x: x['authors'][0]['name'])
            dados = cria_dados(artigos)
            window['-TABELA-'].update(values = dados)
        elif v == "Afiliação":
            artigos.sort(key=lambda x: x['authors'][0]['affiliation'])
            dados = cria_dados(artigos)
            window['-TABELA-'].update(values = dados)
        
    if event == '-SEARCH-':
        query = values['-SEARCH-'].strip()
        resultados = pesquisa(artigos, query)
        dados = cria_dados(resultados)
        window['-TABELA-'].update(values=dados)
    
    if event == 'OK' and values['-RESULTADOS-']:
        resultado_selecionado = values['-RESULTADOS-'][0]
        sg.popup(f"Você selecionou: {resultado_selecionado}")
         

    if event == 'Criar':
        janela_criacao = janela_criar_artigo()
        while True:
            event, values = janela_criacao.read()
            if event == sg.WINDOW_CLOSED:
                janela_criacao.close()
                break
            if event == '-CRIAARTIGO-':
                novo_titulo = values['-NOVOTITULO-']
                novo_doi = values ['-NOVODOI-']
                novo_pdf = values['-NOVOPDF-']
                novo_resumo = values['-NOVORESUMO-']
                novo_data = values['-NOVODATA-']
                novo_url = values['-NOVOURL-']
                novo_keywords = values['-NOVOKEYWORDS-']
                autores = []
                novo_autor = values['-NOVOAUTOR-'].split(',')
                novo_afiliacao = values['-NOVOAFILIACAO-'].split(',')
                for i in range(0,len(novo_autor)):
                    autores.append({"name":novo_autor[i],"affiliation":novo_afiliacao[i]})
                novo_artigo = {
                    "title": novo_titulo,
                    "abstract": novo_resumo,
                    "doi": novo_doi,
                    "pdf": novo_pdf,
                    "publish_date": novo_data,
                    "url": novo_url,
                    "keywords": novo_keywords,
                    "authors": autores
                }
                artigos.append(novo_artigo)
                novos_dados = cria_dados(artigos)
                window["-TABELA-"].update(values = novos_dados)
                janela_criacao.close()
                break
            

        
    if event == 'Filtrar':
        resultados = filtrar_artigos(artigos)
        dados = cria_dados(resultados)
        window['-TABELA-'].update(values=dados)
    
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

    if event == 'Gravar':
        gravar(artigos, "ata_medica_papers.json")
        sg.popup("Dados salvos com sucesso!")

    window.refresh()

window.close()