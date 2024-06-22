import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Configurar o WebDriver
driver = webdriver.Firefox()  # Ajuste o caminho conforme necessário
driver.implicitly_wait(1)  # Ajuste conforme necessário

# Carregar dados do Excel
file_path = '/Users/ranecdonascimentont/Downloads/imoveis060424/unificado120424.xlsx'
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

if 'erro' not in data.columns:
    data['erro'] = None  # Adiciona a coluna se ainda não existir

if 'data' not in data.columns:
    data['data'] = None  # Adiciona a coluna se ainda não existir

if 'hora' not in data.columns:
    data['hora'] = None  # Adiciona a coluna se ainda não existir


# Iterar a partir do índice 650 até o final do DataFrame
for index, row in data.iloc[0:].iterrows():

    try:

        # # Tentativas de captura de cada elemento com tratamento de exceções específico
        # try:
        #     financiamento = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[1]/div/div[3]/p[3]')
        #     data.at[index, 'financiamento'] = financiamento.text
        #     print(financiamento.text)
        # except NoSuchElementException:
        #     print("Dados de financiamento não localizados")
        #     data.at[index, 'erro'] = 'Erro no financiamento'
        #
        # try:
        #     area_privativa = driver.find_element(By.XPATH, "//span[contains(text(), 'Área privativa')]")
        #     data.at[index, 'area privativa'] = area_privativa.text
        #     print(area_privativa.text)
        # except NoSuchElementException:
        #     print("Dados de área privativa não localizados")
        #     data.at[index, 'erro'] = 'Erro na área privativa'
        #
        # try:
        #     area_terreno = driver.find_element(By.XPATH, "//span[contains(text(), 'Área do Terreno')]")
        #     data.at[index, 'area do terreno'] = area_terreno.text
        #     print(area_terreno.text)
        # except NoSuchElementException:
        #     print("Dados de área do terreno não localizados")
        #     data.at[index, 'erro'] = 'Erro na área do terreno'

        if row['Tipo'] in ["Venda Online"]:

            print(index)
            driver.implicitly_wait(1)
            driver.get(row['Link'])
            driver.implicitly_wait(1)
            try:
                dias = driver.find_element(By.ID, 'dias0')
                data.at[index, 'dias'] = dias.text
                print(dias.text)
            except NoSuchElementException:
                print("Dados de dias não localizados")


            try:
                horas = driver.find_element(By.ID, 'horas0')
                data.at[index, 'horas'] = horas.text
                print(horas.text)
            except NoSuchElementException:
                print("Dados de horas não localizados")
        else:
            None



    except Exception as e:
        print(f"Erro geral ao processar {row['Link']}: {e}")
        data.at[index, 'erro'] = 'Erro geral'

# Salvar os dados de volta no mesmo arquivo
data.to_excel(file_path, index=False)

# Fechar o navegador
driver.quit()