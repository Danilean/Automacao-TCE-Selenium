from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_driver():
    chrome_options = Options()
    download_dir = r"C:\Users\danilo.formanski\Downloads"
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
    paineis_controle_interno = wait.until(EC.element_to_be_clickable((By.XPATH, '//h3[text()="Painéis Controle Interno"]')))
    paineis_controle_interno.click()
    extrato = wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()="E-SFINGE ONLINE – EXTRATO"]')))
    extrato.click()

def alternar_para_nova_aba(driver):
    aba_antiga = driver.current_window_handle
    novas_abas = WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    for aba in driver.window_handles:
        if aba != aba_antiga:
            driver.switch_to.window(aba)
            break
    driver.switch_to.window(aba_antiga)
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])

def realizar_scroll(driver, container_css, pixels_to_scroll):
    try:
        container = driver.find_element(By.CSS_SELECTOR, container_css)
        driver.execute_script(f"arguments[0].scrollTop += {pixels_to_scroll};", container)
        sleep(3)  # Espera para o scroll completar e carregar elementos
    except Exception as e:
        print(f"Erro durante o scroll: {e}")


def realizar_downloads(driver):
    wait = WebDriverWait(driver, 50)
    sleep(5)
    extrato_geral_botao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-light')))
    extrato_geral_botao.click()
    sleep(7)

    botao_ente = wait.until(EC.element_to_be_clickable((By.XPATH, '//h6[text()="Ente"]')))
    botao_ente.click()

    botao_limpar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
    botao_limpar.click()
    sleep(2)

    items_per_batch = 10
    processed_count = 0

    while True:
        try:
            # Garante que há pelo menos 10 elementos disponíveis
            while True:
                second_item = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
                available_items = len(second_item) - processed_count
                if available_items >= items_per_batch:
                    break
                realizar_scroll(driver, "div.ListBox-styledScrollbars", 240)
                sleep(3)  # Aguarda o carregamento de novos elementos

            # Seleciona o batch de 10 itens
            second_item = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
            sublist = second_item[processed_count:processed_count + items_per_batch]

            # Se há menos de 10 itens disponíveis, ajusta a seleção
            if len(sublist) < items_per_batch:
                sublist = second_item[processed_count:]

            # Certifica que cada elemento da sublist é visível e clicável
            items_to_process = [element for element in sublist if element.is_displayed()]
            if len(items_to_process) == 0:
                print("Nenhum item visível encontrado para seleção.")
                break

            for element in items_to_process:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element))
                sleep(1)
                element.click()
                sleep(1)  # Tempo para garantir que o clique foi registrado

            # Verificar se o botão de backdrop está presente e clicá-lo
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.MuiBackdrop-root'))).click()

            botao_download = wait.until(EC.element_to_be_clickable((By.ID, 'GRA_1_Dow')))
            botao_download.click()
            sleep(10)

            botao_ente.click()
            botao_limpar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
            botao_limpar.click()
            sleep(5)

            # Atualiza o contador de elementos processados
            processed_count += len(items_to_process)

            # Verifica se há mais elementos para processar
            if processed_count >= len(driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')):
                break

        except Exception as e:
            print(f"Erro durante o processamento: {e}")
            break

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
