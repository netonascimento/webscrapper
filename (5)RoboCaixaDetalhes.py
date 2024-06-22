import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Configurar o WebDriver
driver = webdriver.Firefox()

# Aumentar timeout para esperar que os elementos da página carreguem
driver.implicitly_wait(1)  # Ajuste conforme necessário

# Carregar dados do Excel
file_path = '/Users/ranecdonascimentont/Downloads/imoveis060424/unificado120424.xlsx'
data = pd.read_excel(file_path)

# Verificar se há uma coluna para armazenar os dados capturados
if 'Dados Capturados1' not in data.columns:
    data['Dados Capturados'] = None  # Adiciona a coluna se ainda não existir

if 'Dados Capturados2' not in data.columns:
    data['Dados Capturados2'] = None  # Adiciona a coluna se ainda não existir

for index, row in data.iterrows():
    # Verificar se a célula já contém dados capturados
    if pd.isna(row['Dados Capturados']):
        try:
            driver.get(row['Link'])
            # Suponha que você queira capturar o título da página
            financiamento = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[1]/div/div[3]/p[3]')
            data.at[index, 'Dados Capturados1'] = financiamento.text

            if data.at[index, 'Tipo'] != "Venda Online" or data.at[index, 'Tipo'] != "Venda Direta Online" or data.at[
                index, 'Tipo'] != None:
                leiloeiro = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[1]/div/div[3]/span[3]')
                data.at[index, 'Dados Capturados2'] = leiloeiro.text
            else:
                None
    else:
        print("Dados já capturados")


        except Exception as e:
        print(f"Erro ao processar {row['Link']}: {e}")
        data.at[index, 'Dados Capturados'] = 'Erro ao capturar dados'

# Salvar os dados de volta no mesmo arquivo
data.to_excel(file_path, index=False)

# Fechar o navegador
driver.quit()

# Verificar se há uma coluna para armazenar os dados capturados
if 'Dados Capturados' not in data.columns:
    data['Dados Capturados'] = None  # Adiciona a coluna se ainda não existir

for index, row in data.iterrows():
    # Verificar se a célula já contém dados capturados
    if pd.isna(row['Dados Capturados']):
        try:
            driver.get(row['Link'])
            # Suponha que você queira capturar o título da página
            titulo = driver.title
            data.at[index, 'Dados Capturados'] = titulo
        except Exception as e:
            print(f"Erro ao processar {row['Link']}: {e}")
            data.at[index, 'Dados Capturados'] = 'Erro ao capturar dados'
    else:
        print(f"Dados já capturados para {row['Link']}")

# Salvar os dados de volta no mesmo arquivo
data.to_excel(file_path, index=False)

# Fechar o navegador
driver.quit()

