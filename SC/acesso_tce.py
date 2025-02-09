from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def access_tce_panel():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://paineis.tce.sc.gov.br"

    try:
        driver.get(url)
        print("Acesso ao site realizado com sucesso.")

        time.sleep(5)


    except Exception as e:
        print(f"Ocorreu um erro ao acessar o site: {e}")
    finally:
        driver.quit()
        print("Navegador fechado.")


if __name__ == "__main__":
    access_tce_panel()
