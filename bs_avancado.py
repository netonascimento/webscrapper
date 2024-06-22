import requests
from bs4 import BeautifulSoup
import time

root = "https://subslikescript.com"
website = f'{root}/movies'

result = requests.get(website)

content = result.text

soup = BeautifulSoup(content, 'lxml')

box = soup.find("article", class_= "main-article")

links = []

for link in box.find_all("a", href = True):
    links.append(root + "/" + link['href'])

#pagination
pagination =

print(links)
n = 10
for link in links:
        time.sleep(1)
    # try:
        n = n - 1
        if n == 0:
            break

        result = requests.get(link)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('article', class_="main-article")
        title = article.find('h1').get_text()
        soup = BeautifulSoup(content, 'lxml')
        box = soup.find('article', class_ = "main-article")
        fullscript = box.find("div", class_ = "full-script").get_text(strip=True, separator=" ")
        with open(f'{title}.txt', 'w') as file:
            file.write(fullscript)


    # except:
    #     print("Não foi possível capturar")






