import csv
import io

estados = [
    'AC',
    'AL',
    'AP',
    'AM',
    'BA',
    'CE',
    'DF',
    'ES',
    'GO',
    'MA',
    'MT',
    'MS',
    'MG',
    'PA',
    'PB',
    'PR',
    'PE',
    'PI',
    'RJ',
    'RN',
    'RS',
    'RO',
    'RR',
    'SC',
    'SP',
    'SE',
    'TO'
]

# Lê um CSV com o cabeçalho

try:
    for estado in estados:
        with io.open('/Users/ranecdonascimentont/Downloads/imoveis060424/Lista_imoveis_'+estado+'.csv', encoding='latin-1') as f:
            reader = csv.reader(f)
            #next(reader) # skip header
            data = [r for r in reader]
            print(estado)
            header = data[0]
            data = data[4:]
            with open("/Users/ranecdonascimentont/Downloads/imoveis060424/arquivo_modificado"+estado+".csv", 'w', encoding="latin-1") as file:
                writer = csv.writer(file)
                writer.writerows(data)
except FileNotFoundError:
    print("Erro: O arquivo "+estado+" não foi encontrado.")

