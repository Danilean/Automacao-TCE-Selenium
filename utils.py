from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_driver():
    chrome_options = Options()
    download_dir = r"C:\Users\danilo.formanski\Downloads\Arquivos-TCE"
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver

def fazer_login(driver):
    try:
        driver.get('https://virtual.tce.sc.gov.br/web/#/home')
        wait = WebDriverWait(driver, 15)
        nome = wait.until(EC.presence_of_element_located((By.ID, 'codigo')))
        nome.send_keys('05388407900')
        senha = driver.find_element(By.ID, 'nova')
        senha.send_keys('Campeao1')
        botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
        botao_enviar.click()
    except Exception as e:
        print(f"Erro durante o login: {e}")
        driver.quit()

def navegar_para_extrato(driver):
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]')))
        menu_tce_virtual = driver.find_element(By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]')
        menu_tce_virtual.click()
        paineis_controle_interno = wait.until(EC.element_to_be_clickable((By.XPATH, '//h3[text()="Painéis Controle Interno"]')))
        paineis_controle_interno.click()
        extrato = wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()="E-SFINGE ONLINE – EXTRATO"]')))
        extrato.click()
    except Exception as e:
        print(f"Erro durante a navegação para o extrato: {e}")
        driver.quit()

def alternar_para_nova_aba(driver):
    try:
        aba_antiga = driver.current_window_handle
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        for aba in driver.window_handles:
            if aba != aba_antiga:
                driver.switch_to.window(aba)
                break
        driver.switch_to.window(aba_antiga)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    except Exception as e:
        print(f"Erro ao alternar para a nova aba: {e}")
        driver.quit()
