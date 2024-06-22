import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

# Configurar o WebDriver
driver = webdriver.Firefox()

# Aumentar timeout para esperar que os elementos da página carreguem
# driver.implicitly_wait()  # Ajuste conforme necessário

# Carregar dados do Excel
file_path = '/Users/ranecdonascimentont/Downloads/imoveis060424/unificado150424.xlsx'
data = pd.read_excel(file_path)

# Verificar se há uma coluna para armazenar os dados capturados
if 'financiamento' not in data.columns:
    data['financiamento'] = None  # Adiciona a coluna se ainda não existir

if 'area privativa' not in data.columns:
    data['area privativa'] = None  # Adiciona a coluna se ainda não existir

if 'area do terreno' not in data.columns:
    data['area do terreno'] = None  # Adiciona a coluna se ainda não existir

if 'leiloeiro' not in data.columns:
    data['leiloeiro'] = None  # Adiciona a coluna se ainda não existir

if 'data_leilao1' not in data.columns:
    data['data_leilao1'] = None  # Adiciona a coluna se ainda não existir

if 'data_leilao2' not in data.columns:
    data['data_leilao2'] = None  # Adiciona a coluna se ainda não existir

if 'data' not in data.columns:
    data['data'] = None  # Adiciona a coluna se ainda não existir

if 'hora' not in data.columns:
    data['hora'] = None  # Adiciona a coluna se ainda não existir

if 'erro' not in data.columns:
    data['erro'] = None  # Adiciona a coluna se ainda não existir



for index, row in data.iloc[30:].iterrows():


    try:
        print(index)
        driver.get(row['Link'])
        #driver.get('https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&hdnimovel=10171232')
        # Capturar os dados e incluir na coluna
        financiamento = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[1]/div/div[3]/p[3]')
        data.at[index, 'financiamento'] = financiamento.text
        print(financiamento.text)
    except:
        print("Dados de financiamento não localizados")

    try:
        area_privativa = driver.find_element(By.XPATH, "//span[contains(text(), 'Área privativa')]")
        data.at[index, 'area privativa'] = area_privativa.text
        print(area_privativa.text)
    except:
        print("Dados de area privativa não localizados")

    try:
        area_terreno = driver.find_element(By.XPATH, "//span[contains(text(), 'Área do Terreno')]")
        data.at[index, 'area do terreno'] = area_terreno.text
        print(area_terreno.text)
    except:
        print("Dados de area do terreno não localizados")

        # if row['Tipo'] in ["Venda Online" ]:

    try:
        leiloeiro = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[1]/div/div[3]/span[3]')
        data.at[index, 'leiloeiro'] = leiloeiro.text
        print(leiloeiro.text)
    except:
        print("Dados de leiloeiro não localizados")

    try:
        elemento_data1 = driver.find_element(By.XPATH, "//span[contains(text(), 'Data do 1º Leilão')]")
        texto_completo1 = elemento_data1.text
        data_leilao1 = re.search(r'\d{2}/\d{2}/\d{4} - \d{2}h\d{2}', texto_completo1)

        if data_leilao1:
            data_encontrada = data_leilao1.group()  # Extrai o texto da correspondência
            data.at[index, 'data_leilao1'] = data_encontrada
            print(data_encontrada)
        else:
            print("Data do 1º leilão não encontrada no texto fornecido.")

    except:
        print("Dados de data1 de leilão não localizados")

    try:
        elemento_data2 = driver.find_element(By.XPATH, "//span[contains(text(), 'Data do 2º Leilão')]")
        texto_completo2 = elemento_data2.text
        data_leilao2 = re.search(r'\d{2}/\d{2}/\d{4} - \d{2}h\d{2}', texto_completo2)

        if data_leilao2:
            data_encontrada = data_leilao2.group()  # Extrai o texto da correspondência
            data.at[index, 'data_leilao2'] = data_encontrada
            print(data_encontrada)
        else:
            print("Data do 2º leilão não encontrada no texto fornecido.")

    except:
        print("Dados de data2 de leilão não localizados")


# Salvar os dados de volta no mesmo arquivo
data.to_excel(file_path, index=False)

# Fechar o navegador
driver.quit()