
import scrapy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class ImoveisSpider(scrapy.Spider):
    name = "imoveis"
    start_urls = [
        'https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?codigo=8019070007882'
    ]

    def __init__(self, *args, **kwargs):
        super(ImoveisSpider, self).__init__(*args, **kwargs)
        self.data = []
        print("Spider iniciado")

    def parse(self, response):
        print(f"Processando página: {response.url}")

        # Configuração do Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executar o Chrome em modo headless (sem GUI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(response.url)
        time.sleep(5)  # Esperar carregar a página completamente

        # Extrair dados usando Selenium
        titulo = driver.find_element(By.CSS_SELECTOR, 'div.control-item h5').text
        endereco = driver.find_element(By.CSS_SELECTOR, 'div.related-box p').text
        preco_avaliacao = driver.find_element(By.XPATH, '//p[contains(text(), "Valor de avaliação")]').text.split(":")[1].strip()
        preco_venda = driver.find_element(By.XPATH, '//p[contains(text(), "Valor mínimo de venda")]//b').text
        link = response.url

        item = {
            'titulo': titulo.strip() if titulo else 'N/A',
            'endereco': endereco.strip() if endereco else 'N/A',
            'preco_avaliacao': preco_avaliacao.strip() if preco_avaliacao else 'N/A',
            'preco_venda': preco_venda.strip() if preco_venda else 'N/A',
            'link': link.strip() if link else 'N/A',
        }
        print(f"Item extraído: {item}")
        self.data.append(item)
        driver.quit()
        yield item

    def closed(self, reason):
        print(f"Spider fechado: {reason}")
        if self.data:
            print("Salvando dados em imoveis.xlsx")
            df = pd.DataFrame(self.data)
            df.to_excel('imoveis.xlsx', index=False)
            print("Dados salvos com sucesso")
        else:
            print("Nenhum dado para salvar")

