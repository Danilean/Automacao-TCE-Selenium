from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import scroll_page
from time import sleep


def download_files(driver):
    """Downloads files from the TCE portal."""
    try:
        wait = WebDriverWait(driver, 50)
        sleep(5)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-light'))).click()
        sleep(7)

        ente_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//h6[text()="Ente"]')))
        clear_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Limpar seleção"]')))
        download_button = wait.until(EC.element_to_be_clickable((By.ID, 'GRA_1_Dow')))

        processed_elements = set()
        scroll_count = 0

        while True:
            try:
                scroll_page(driver, "div.ListBox-styledScrollbars", scroll_count * 290)
                scroll_count += 1
                print(f"Scrolled: {scroll_count}")

                if scroll_count == 37:
                    break

            except Exception as e:
                break
    except Exception as e:
        print(f"Download error: {e}")
        driver.quit()
        exit()
