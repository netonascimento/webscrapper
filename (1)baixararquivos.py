from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


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

driver = webdriver.Firefox()

for estado in estados:
    driver.get("https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp")
    driver.implicitly_wait(0.5)
    dropdown = Select(driver.find_element(By.NAME, "cmb_estado"))
    dropdown.select_by_visible_text(estado)
    driver.find_element(By.XPATH, '//*[@id="btn_next1"]').click()

driver.implicitly_wait(10)
driver.quit()