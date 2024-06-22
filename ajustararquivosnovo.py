import pandas as pd
import os

# Caminho para a pasta contendo os arquivos CSV
diretorio = '/Users/ranecdonascimentont/Downloads/imoveis060424/'


# # Defina o cabeçalho único pré-definido
# cabecalho = ['Imóvel', 'Estado', 'Cidade', 'Bairro', 'Endereço', 'Preço', 'Avaliação', 'Desconto', 'Descrição', 'Modalidade', 'Link' ]

# Lista para armazenar os dataframes
dataframes = []

for arquivo in os.listdir(diretorio):
    if arquivo.endswith('.csv'):
        caminho_completo = os.path.join(diretorio, arquivo)
        print(caminho_completo)

        # Ler o CSV pulando as primeiras 4 linhas
        df = pd.read_csv(caminho_completo, skiprows=4, header=None, on_bad_lines='skip', encoding='latin-1')
        dataframes.append(df)
# Concatenar todos os dataframes em um único dataframe
resultado_final = pd.concat(dataframes, ignore_index=True)

# Salvar o dataframe concatenado em um novo arquivo CSV
resultado_final.to_csv('/Users/ranecdonascimentont/Downloads/imoveis060424/resultado_final.csv', index=False)

print('Processamento concluído. Todos os arquivos válidos foram combinados em "resultado_final.csv')

