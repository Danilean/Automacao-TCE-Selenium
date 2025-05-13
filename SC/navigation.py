from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def esperar_elemento(driver, by, identifier, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, identifier)))

def navegar_para_extrato(driver):
    try:
        if not driver.current_window_handle:
            print("Driver perdeu o handle da janela.")
            driver.quit()
            exit()

        esperar_elemento(driver, By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]').click()
        esperar_elemento(driver, By.XPATH, '//h3[text()="Painéis Controle Interno"]').click()
        esperar_elemento(driver, By.XPATH, '//p[text()="E-SFINGE ONLINE – EXTRATO"]').click()

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
        print(f"Erro ao alternar aba: {e}")
        driver.quit()

def esperar_elemento(driver, by, seletor, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, seletor)))

def esperar_elementos_carregados(driver, by, selector, timeout=30):
    try:
        return WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(by, selector)) > 0
            and any(e.text.strip() for e in d.find_elements(by, selector))
        )
    except:
        return []

def realizar_scroll(driver, container_css, pixels_to_scroll):
    try:
        container = esperar_elemento(driver, By.CSS_SELECTOR, container_css)
        driver.execute_script(f"arguments[0].scrollTop += {pixels_to_scroll};", container)
        sleep(3)
    except Exception as e:
        print(f"Erro ao fazer scroll: {e}")
        driver.quit()

def realizar_downloads(driver):
    try:
        wait = WebDriverWait(driver, 50)
        sleep(5)

        esperar_elemento(driver, By.CSS_SELECTOR, 'button.btn.btn-light').click()
        sleep(7)

        botao_ente = esperar_elemento(driver, By.XPATH, '//h6[text()="Ente"]')
        botao_ente.click()

        botao_limpar = esperar_elemento(driver, By.CSS_SELECTOR, 'button[title="Limpar seleção"]')
        botao_limpar.click()
        sleep(2)

        processed_elements = set()
        scroll_count = 0

        while True:
            try:
                esperar_elementos_carregados(driver, By.CSS_SELECTOR, 'div.RowColumn-barContainer')

                if scroll_count == 37:
                    realizar_scroll(driver, "div.ListBox-styledScrollbars", 10730)
                    elements = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')
                    for element in elements:
                        text = element.text
                        if text in ["XAVANTINA", "XAXIM", "ZORTÉA"] and text not in processed_elements:
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()
                            processed_elements.add(text)
                            sleep(1)

                    if not processed_elements:
                        print("Nenhum item foi selecionado, download não será realizado.")
                        return False

                    esperar_elemento(driver, By.CSS_SELECTOR, '.MuiBackdrop-root').click()
                    esperar_elemento(driver, By.ID, 'GRA_1_Dow').click()
                    sleep(10)
                    return True

                elements = driver.find_elements(By.CSS_SELECTOR, 'div.RowColumn-barContainer')[:10]
                for element in elements:
                    text = element.text
                    if text and text not in processed_elements:
                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()
                        processed_elements.add(text)
                        sleep(1)

                if not processed_elements:
                    print("Nenhum item foi selecionado, download não será realizado.")
                    return False

                esperar_elemento(driver, By.CSS_SELECTOR, '.MuiBackdrop-root').click()
                esperar_elemento(driver, By.ID, 'GRA_1_Dow').click()
                sleep(10)

                botao_ente.click()
                botao_limpar = esperar_elemento(driver, By.CSS_SELECTOR, 'button[title="Limpar seleção"]')
                botao_limpar.click()
                sleep(5)

                scroll_count += 1
                realizar_scroll(driver, "div.ListBox-styledScrollbars", scroll_count * 290 + 60)
                print(f"Scroll #{scroll_count}")

            except Exception as e:
                print(f"Erro durante loop de download: {e}")
                return False

    except Exception as e:
        print(f"Erro geral no download: {e}")
        driver.quit()
        return False
