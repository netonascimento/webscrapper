import requests
from bs4 import BeautifulSoup
import pandas as pd


# Função para obter o conteúdo de uma página específica
def get_page_content(url):
    response = requests.get(url)
    return response.content


# Função para extrair o número total de páginas
def get_total_pages(content):
    soup = BeautifulSoup(content, 'html.parser')
    pagination = soup.find_all('li', class_='page-item')
    last_page_link = pagination[-1].find('a', class_='page-link') if pagination else None
    total_pages = int(last_page_link.text.strip()) if last_page_link else 1
    return total_pages


# Função para extrair os links dos imóveis de uma página
def extract_property_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    property_links = []
    property_items = soup.find_all('a', class_='btn btn-block btn-dark')
    for item in property_items:
        link = item['href']
        property_links.append(link)
    return property_links


# Função para extrair os detalhes de um imóvel
def extract_property_details(content):
    soup = BeautifulSoup(content, 'html.parser')
    property_info = {}

    titulo_tag = soup.find('h1')
    property_info['Título'] = titulo_tag.text.strip() if titulo_tag else 'N/A'

    detalhes = soup.find_all('h6', class_='text-center border-top p-2 m-0')

    property_info['Data do Primeiro Leilão'] = 'N/A'
    property_info['Valor do Primeiro Leilão'] = 'N/A'
    property_info['Data do Segundo Leilão'] = 'N/A'
    property_info['Valor do Segundo Leilão'] = 'N/A'

    for detalhe in detalhes:
        if 'Data 1º Leilão' in detalhe.text:
            property_info['Data do Primeiro Leilão'] = detalhe.text.replace('Data 1º Leilão:', '').strip()
        elif 'Lance Inicial' in detalhe.text and property_info['Valor do Primeiro Leilão'] == 'N/A':
            property_info['Valor do Primeiro Leilão'] = detalhe.text.replace('Lance Inicial:', '').strip()
        elif 'Data 2º Leilão' in detalhe.text:
            property_info['Data do Segundo Leilão'] = detalhe.text.replace('Data 2º Leilão:', '').strip()
        elif 'Lance Inicial' in detalhe.text and property_info['Valor do Primeiro Leilão'] != 'N/A':
            property_info['Valor do Segundo Leilão'] = detalhe.text.replace('Lance Inicial:', '').strip()

    descricao_tag = soup.find('div', class_='mb-3 p-2 border rounded text-justify')
    property_info['Descrição'] = descricao_tag.text.strip() if descricao_tag else 'N/A'

    url_tag = soup.find('meta', property='og:url')
    property_info['URL'] = url_tag['content'] if url_tag else 'N/A'

    imagem_tag = soup.find('meta', property='og:image')
    property_info['Imagem'] = imagem_tag['content'] if imagem_tag else 'N/A'

    # Extraindo cidade e estado
    descricao_texto = descricao_tag.get_text() if descricao_tag else ''
    cidade_estado = ''
    for line in descricao_texto.split('\n'):
        if 'Cidade:' in line:
            cidade_estado = line.replace('Cidade:', '').strip()
            break

    if '/' in cidade_estado:
        cidade, estado = cidade_estado.split('/')
        property_info['Cidade'] = cidade.strip()
        property_info['Estado'] = estado.strip()
    else:
        property_info['Cidade'] = cidade_estado
        property_info['Estado'] = 'N/A'

    return property_info


# URL base do site
base_url = 'https://www.leilaopernambuco.com.br/lotes/imovel?tipo=imovel&page=1'

# Obtendo o conteúdo da primeira página para determinar o número total de páginas
first_page_content = get_page_content(base_url)
total_pages = get_total_pages(first_page_content)
print(f'Total de páginas encontradas: {total_pages}')

# Coletando todos os links de imóveis de todas as páginas
all_property_links = []
for page_num in range(1, total_pages + 1):
    page_url = f'https://www.leilaopernambuco.com.br/lotes/imovel?tipo=imovel&page={page_num}'
    print(f'Extraindo imóveis da página: {page_url}')
    page_content = get_page_content(page_url)
    property_links = extract_property_links(page_content)
    print(f'Links de imóveis extraídos: {len(property_links)}')
    all_property_links.extend(property_links)

# Coletando detalhes de todos os imóveis
all_properties = []
for property_link in all_property_links:
    print(f'Extraindo detalhes do imóvel: {property_link}')
    property_content = get_page_content(property_link)
    property_details = extract_property_details(property_content)
    all_properties.append(property_details)

# Criando um DataFrame com os dados coletados
df = pd.DataFrame(all_properties)
print(f'Total de imóveis extraídos: {len(df)}')

# Salvando os resultados em um arquivo Excel
excel_file = 'leiloespernambuco.xlsx'
df.to_excel(excel_file, index=False)

print(f'Dados salvos em {excel_file}')
