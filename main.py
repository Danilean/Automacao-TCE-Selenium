from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from excel import processar_e_inserir_dados_postgres
from utils import iniciar_driver, fazer_login, navegar_para_extrato, alternar_para_nova_aba
import subprocess

def abrir_powerbi():
    powerbi_path = r"C:\Caminho\Para\O\PowerBI.exe"
    arquivo_pbix = r"C:\Caminho\Para\O\Arquivo.pbix"

    try:
        subprocess.Popen([powerbi_path, arquivo_pbix])
        print("Power BI foi aberto com sucesso.")
    except Exception as e:
        print(f"Erro ao abrir Power BI: {e}")

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(executable_path=r'C:\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


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
        print(scroll_count)
        while True:
            try:
                if scroll_count == 36:
                    realizar_scroll(driver, "div.ListBox-styledScrollbars", 10730)
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

                    botao_download = wait.until(EC.element_to_be_clickable((By.ID, 'GRA_1_Dow')))
                    botao_download.click()
                    sleep(10)
                    break

                second_item = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
                sublist = second_item[:10]
                for element in sublist:
                    text = element.text
                    if text in processed_elements:
                        raise Exception("Elemento já processado")
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element))
                    sleep(1)
                    element.click()
                    processed_elements.add(text)
                    sleep(1)

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.MuiBackdrop-root'))).click()

                botao_download = wait.until(EC.element_to_be_clickable((By.ID, 'GRA_1_Dow')))
                botao_download.click()
                sleep(10)

                botao_ente.click()
                botao_limpar = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
                botao_limpar.click()
                sleep(5)

                realizar_scroll(driver, "div.ListBox-styledScrollbars", scroll_count * 290 + 290)
                realizar_scroll(driver, "div.ListBox-styledScrollbars", 60)

                scroll_count += 1

            except Exception as e:
                print(f"Erro durante o processamento: {e}")
                break

        processar_e_inserir_dados_postgres()

    except Exception as e:
        print(f"Erro geral no download: {e}")
        driver.quit()
        main()


def main():
    driver = iniciar_driver()
    try:
        fazer_login(driver)
        navegar_para_extrato(driver)
        alternar_para_nova_aba(driver)
        realizar_downloads(driver)
       # processar_e_inserir_dados_postgres()
       # abrir_powerbi()
    except Exception as e:
        print(f"Erro na execução principal: {e}")
        driver.quit()
        main()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

