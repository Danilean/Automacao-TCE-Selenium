from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import TCE_LOGIN, TCE_PASSWORD


def login(driver):
    try:
        driver.get('https://virtual.tce.sc.gov.br/web/#/home')
        wait = WebDriverWait(driver, 15)

        wait.until(EC.presence_of_element_located((By.ID, 'codigo'))).send_keys(TCE_LOGIN)
        driver.find_element(By.ID, 'nova').send_keys(TCE_PASSWORD)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()
    except Exception as e:
        print(f"Login error: {e}")
        driver.quit()
        exit()
