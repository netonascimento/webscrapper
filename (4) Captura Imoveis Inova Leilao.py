import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from urllib.parse import urljoin
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image
import os

# URL do site de leilões
url = "https://www.inovaleilao.com.br/categorias/imoveis#resultados"

# Envie uma solicitação GET para a página inicial
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)


base_url = "https://www.inovaleilao.com.br/"

# Encontre todos os links para leilões de imóveis
leilao_links = soup.find_all('a', class_='btn btn-link rounded-lg btn-block bg-3 text-white')  # ajuste a classe conforme a estrutura do site

print(leilao_links)

# Lista para armazenar informações dos imóveis
imoveis_data = []

# Diretório para armazenar as imagens baixadas
images_dir = 'images'
os.makedirs(images_dir, exist_ok=True)

# Função para limpar o nome do arquivo
def sanitize_filename(filename):
    # Remove caracteres inválidos para nomes de arquivos
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Percorra todos os links de leilões de imóveis
for link in leilao_links:
    leilao_url = urljoin(base_url, link['href'])
    print(leilao_url)
    leilao_response = requests.get(leilao_url)
    leilao_soup = BeautifulSoup(leilao_response.text, 'html.parser')

    # Converta o conteúdo HTML em um objeto lxml
    dom = html.fromstring(str(leilao_soup))


    # Extraia as informações do imóvel usando XPath
    titulo = dom.xpath('/html/body/section/div[2]/div/div/div/div[2]/div[1]/div[1]/h2/text()')
    data_primeiro_leilao = dom.xpath('/html/body/main/div/div/div[2]/div[2]/div[3]/div/table/tbody/tr[1]/td[2]/text()')
    valor_primeiro_leilao = dom.xpath('/html/body/main/div/div/div[2]/div[2]/div[3]/div/table/tbody/tr[1]/td[3]/text()')
    data_segundo_leilao = dom.xpath('/html/body/main/div/div/div[2]/div[2]/div[3]/div/table/tbody/tr[2]/td[2]/text()')
    valor_segundo_leilao = dom.xpath('/html/body/main/div/div/div[2]/div[2]/div[3]/div/table/tbody/tr[2]/td[3]/text()')
    descricao = dom.xpath('/html/body/main/div/div/div[2]/div[1]/div[3]/div[1]/article/div/p/text()')

    # Encontre a primeira tag <img> com a classe 'w-100'
    img_tag = leilao_soup.find('img', class_='w-100')

    # Extraia o atributo 'src' da tag <img>
    imagem_url = img_tag['src'] if img_tag else 'N/A'

    # Imprima os resultados para depuração
    print(f"Título: {titulo}")
    print(f"Data do Primeiro Leilão: {data_primeiro_leilao}")
    print(f"Valor do Primeiro Leilão: {valor_primeiro_leilao}")
    print(f"Data do Segundo Leilão: {data_segundo_leilao}")
    print(f"Valor do Segundo Leilão: {valor_segundo_leilao}")
    print(f"Descrição: {descricao}")
    print(f"Link da Imgem: {img_tag}")


    # Se o XPath retornar uma lista, pegue o primeiro elemento; caso contrário, use 'N/A'
    titulo = titulo[0].strip() if titulo else 'N/A'
    data_primeiro_leilao = data_primeiro_leilao[0].strip() if data_primeiro_leilao else 'N/A'
    valor_primeiro_leilao = valor_primeiro_leilao[0].strip() if valor_primeiro_leilao else 'N/A'
    data_segundo_leilao = data_segundo_leilao[0].strip() if data_segundo_leilao else 'N/A'
    valor_segundo_leilao = valor_segundo_leilao[0].strip() if valor_segundo_leilao else 'N/A'
    descricao = descricao if descricao else 'N/A'

    # Baixar a imagem
    if imagem_url != 'N/A':
        imagem_path = os.path.join(images_dir, f"{sanitize_filename(titulo)}.jpg")
        imagem_response = requests.get(imagem_url)
        with open(imagem_path, 'wb') as file:
            file.write(imagem_response.content)



    # Limpeza dos dados extraídos
    def clean_text(text_list):
        # Junta a lista em uma única string e remove caracteres desnecessários
        return ' '.join([text.strip() for text in text_list if text.strip()])

    #titulo = clean_text(titulo)
    #data_primeiro_leilao = clean_text(data_primeiro_leilao)
    #valor_primeiro_leilao = clean_text(valor_primeiro_leilao)
    #data_segundo_leilao = clean_text(data_segundo_leilao)
    #valor_segundo_leilao = clean_text(valor_segundo_leilao)
    descricao = clean_text(descricao)
    imagem_url = urljoin(base_url, imagem_url) if imagem_url != 'N/A' else 'N/A'

    # Adicione as informações à lista de dados
    imoveis_data.append({
        'Título': titulo,
        'Data do Primeiro Leilão': data_primeiro_leilao,
        'Valor do Primeiro Leilão': valor_primeiro_leilao,
        'Data do Segundo Leilão': data_segundo_leilao,
        'Valor do Segundo Leilão': valor_segundo_leilao,
        'Descrição': descricao,
        'URL': leilao_url,
        'Imagem': imagem_path


    })
    print(link)

# Crie um DataFrame do pandas com os dados dos imóveis
df_imoveis = pd.DataFrame(imoveis_data)
print(df_imoveis)


# Salve o DataFrame em uma planilha Excel sem as imagens
excel_path = 'imoveis_Inova_leilao.xlsx'
df_imoveis.to_excel(excel_path, index=False)

# Reabra o arquivo Excel para adicionar as imagens
wb = Workbook()
ws = wb.active

# Adicione os dados à planilha
for row in dataframe_to_rows(df_imoveis, index=False, header=True):
    ws.append(row)

# Adicione as imagens à planilha
for index, row in df_imoveis.iterrows():
    if row['Imagem']:
        img = Image(row['Imagem'])
        ws.add_image(img, f"H{index + 2}")

# Salve o arquivo Excel final com as imagens
wb.save(excel_path)

print("Dados dos imóveis salvos em 'imoveis_inova_leilao.xlsx'")
