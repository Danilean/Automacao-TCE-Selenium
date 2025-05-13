from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def acessar_painel_tce(driver):
    url = "https://paineis.tce.sc.gov.br"
    try:
        driver.get(url)
        print("Tentando acessar:", url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Site carregado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao acessar o site: {e}")
        driver.quit()
        exit()
