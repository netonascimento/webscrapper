from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame

# result = requests.get("https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp")
#
# content = result.text
#
# soup = BeautifulSoup(content, "lxml")
#
# print(soup)

website = "https://subslikescript.com/movie/Titanic-120338"

result = requests.get(website)

content = result.text

soup = BeautifulSoup(content, 'lxml')

box = soup.find('article', class_ = "main-article")

title = box.find("h1").get_text()

# print (title)

plot = box.find("p", class_ = "plot").get_text(strip=True, separator="/")

# print(plot)

fullscript = box.find("div", class_ = "full-script").get_text(strip=True, separator=" ")

# print(fullscript)

dict_movies = {'TItle': title, 'Plot': plot, 'Fullscript': fullscript}

# print(dict_movies)


# print(df_movies)

with open(f"{title}.txt", "w") as file:
    file.write(fullscript)

