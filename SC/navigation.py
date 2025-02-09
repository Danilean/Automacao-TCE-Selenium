from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navegar_para_extrato(driver):
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h3[text()="Painéis Controle Interno"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()="E-SFINGE ONLINE – EXTRATO"]'))).click()
    except Exception as e:
        print(f"Erro na navegação: {e}")
        driver.quit()
        exit()

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
        driver.quit()

def realizar_scroll(driver, container_css, pixels_to_scroll):
    try:
        container = driver.find_element(By.CSS_SELECTOR, container_css)
        driver.execute_script(f"arguments[0].scrollTop += {pixels_to_scroll};", container)
        sleep(3)
    except Exception as e:
        driver.quit()

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
                if scroll_count == 37:
                    realizar_scroll(driver, "div.ListBox-styledScrollbars", 10730)
                    second_item = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
                    for element in second_item:
                        text = element.text
                        if text in ["XAVANTINA", "XAXIM", "ZORTÉA"]:
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
                botao_limpar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
                botao_limpar.click()
                sleep(5)
                base_scroll_value = 290
                increment_value = 290
                scroll_position = scroll_count * increment_value
                realizar_scroll(driver, "div.ListBox-styledScrollbars", scroll_position + base_scroll_value)
                realizar_scroll(driver, "div.ListBox-styledScrollbars", 60)
                scroll_count += 1
                print(scroll_count)
            except Exception as e:
                break
    except Exception as e:
        driver.quit()