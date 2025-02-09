from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_extrato(driver):
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h3[text()="Painéis Controle Interno"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()="E-SFINGE ONLINE – EXTRATO"]'))).click()
    except Exception as e:
        print(f"Navigation error: {e}")
        driver.quit()
        exit()
