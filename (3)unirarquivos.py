import subprocess
import os

# Define o diretório onde os arquivos CSV estão localizados
diretorio = '/Users/ranecdonascimentont/Downloads/imoveis060424/'

# Muda o diretório corrente para onde estão os arquivos CSV
os.chdir(diretorio)

# Executa o comando 'cat' para concatenar todos os CSVs
subprocess.run('cat *.csv > unificado1.csv', shell=True)
