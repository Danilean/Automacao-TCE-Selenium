from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd

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
        main()

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
        main()

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
        main()

def realizar_scroll(driver, container_css, pixels_to_scroll):
    try:
        container = driver.find_element(By.CSS_SELECTOR, container_css)
        driver.execute_script(f"arguments[0].scrollTop += {pixels_to_scroll};", container)
        sleep(3)
    except Exception as e:
        print(f"Erro durante o scroll: {e}")
        driver.quit()
        main()

def realizar_downloads(driver):
    try:
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

        processed_elements = set()
        scroll_count = 0

        while True:
            try:
                # Verificação para o scroll_count 36
                if scroll_count == 36:
                    realizar_scroll(driver, "div.ListBox-styledScrollbars", 10730)

                    # Seleciona os itens "XAVANTINA", "XAXIM" e "Zortéa"
                    second_item = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
                    for element in second_item:
                        text = element.text
                        if text in ["XAVANTINA", "XAXIM", "Zortéa"]:
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element))
                            sleep(1)
                            element.click()
                            processed_elements.add(text)
                            sleep(1)
                            print("Acabou!!")

                    # Realiza o download dos itens selecionados
                    botao_download = wait.until(EC.element_to_be_clickable((By.ID, 'GRA_1_Dow')))
                    botao_download.click()
                    sleep(10)

                    break  # Interrompe o loop após processar os itens desejados

                # Seleciona até 10 itens
                second_item = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
                sublist = second_item[:10]

                for element in sublist:
                    text = element.text
                    if text in processed_elements:
                        print("Elemento já foi processado anteriormente. Interrompendo o loop.")
                        raise Exception("Elemento já processado")
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element))
                    sleep(1)
                    element.click()
                    processed_elements.add(text)
                    sleep(1)

                # Verificar se o botão de backdrop está presente e clicá-lo
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.MuiBackdrop-root'))).click()

                # Realiza o download dos itens selecionados
                botao_download = wait.until(EC.element_to_be_clickable((By.ID, 'GRA_1_Dow')))
                botao_download.click()
                sleep(10)

                # Volta para a seleção de 'Ente' para o próximo lote
                botao_ente.click()
                botao_limpar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
                botao_limpar.click()
                sleep(5)

                # Scroll dinâmico
                base_scroll_value = 290
                increment_value = 290
                scroll_position = scroll_count * increment_value

                realizar_scroll(driver, "div.ListBox-styledScrollbars", scroll_position + base_scroll_value)
                realizar_scroll(driver, "div.ListBox-styledScrollbars", 60)

                scroll_count += 1

            except Exception as e:
                print(f"Erro durante o processamento: {e}")
                break

        concatenar_arquivos_xls()
    except Exception as e:
        print(f"Erro geral no download: {e}")
        driver.quit()
        main()


def concatenar_arquivos_xls(driver):
    try:
        download_dir = r"C:\Users\danilo.formanski\Downloads\Arquivos-TCE"
        all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith('.xls')]

        if not all_files:
            print("Nenhum arquivo XLS encontrado para armazenar.")
            return

        dataframes = []
        for file in all_files:
            df = pd.read_excel(file)
            dataframes.append(df)

        if dataframes:
            df_concatenado = pd.concat(dataframes, ignore_index=True)
            df_concatenado.to_excel(os.path.join(download_dir, 'unificado_final.xlsx'), index=False)
            print("Arquivos concatenados e armazenados em 'unificado_final.xlsx'.")
        else:
            print("Nenhum dado foi concatenado.")
    except Exception as e:
        print(f"Erro ao concatenar arquivos XLS: {e}")
        driver.quit()
        main()

def main():
    driver = iniciar_driver()
    try:
        fazer_login(driver)
        navegar_para_extrato(driver)
        alternar_para_nova_aba(driver)
        realizar_downloads(driver)
    except Exception as e:
        print(f"Erro na execução principal: {e}")
        driver.quit()
        main()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
