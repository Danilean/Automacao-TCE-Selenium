from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import util


def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Abre o Chrome no modo anônimo

    # Configura o diretório de download padrão
    download_dir = r"C:\Users\danilo.formanski\Downloads"  # Substitua pelo caminho do diretório desejado
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,  # Desativa o prompt de download
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver


def fazer_login(driver):
    driver.get('https://virtual.tce.sc.gov.br/web/#/home')
    wait = WebDriverWait(driver, 15)

    nome = wait.until(EC.presence_of_element_located((By.ID, 'codigo')))
    nome.send_keys('05388407900')

    senha = driver.find_element(By.ID, 'nova')
    senha.send_keys('Campeao1')

    botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    botao_enviar.click()


def navegar_para_extrato(driver):
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]')))
    menu_tce_virtual = driver.find_element(By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]')
    menu_tce_virtual.click()

    paineis_controle_interno = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//h3[text()="Painéis Controle Interno"]')))
    paineis_controle_interno.click()

    extrato = wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()="E-SFINGE ONLINE – EXTRATO"]')))
    extrato.click()


def alternar_para_nova_aba(driver):
    # Captura a aba original
    aba_antiga = driver.current_window_handle

    # Aguarda até que uma nova aba seja aberta
    novas_abas = WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

    # Alterna para a nova aba
    for aba in driver.window_handles:
        if aba != aba_antiga:
            driver.switch_to.window(aba)
            break

    # Fecha a aba original e assegura o foco na nova aba
    driver.switch_to.window(aba_antiga)
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


def realizar_downloads(driver):
    wait = WebDriverWait(driver, 50)

    sleep(5)
    # Clica no botão "Extrato Geral"
    extrato_geral_botao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-light')))
    extrato_geral_botao.click()
    sleep(7)

    # Clica no botão "Ente"
    botao_ente = wait.until(EC.element_to_be_clickable((By.XPATH, '//h6[text()="Ente"]')))
    botao_ente.click()

    botao_limpar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
    botao_limpar.click()
    sleep(2)

    second_item = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
    for sublist in util.collate(second_item, 10):
        for element in sublist:
            element.click()
            sleep(2)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.MuiBackdrop-root'))).click()
        botao_download = wait.until(EC.element_to_be_clickable((By.ID, 'GRA_1_Dow')))
        botao_download.click()
        print("xD")
        sleep(15)
        botao_ente.click()
        botao_limpar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
        botao_limpar.click()
        sleep(15)

    driver.save_screenshot('screenshot.png')


def main():
    driver = iniciar_driver()
    try:
        fazer_login(driver)
        navegar_para_extrato(driver)
        alternar_para_nova_aba(driver)
        realizar_downloads(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
