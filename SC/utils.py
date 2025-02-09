import os
from time import sleep

def scroll_page(driver, container_css, pixels_to_scroll):
    """Scrolls inside a specific element."""
    try:
        container = driver.find_element(By.CSS_SELECTOR, container_css)
        driver.execute_script(f"arguments[0].scrollTop += {pixels_to_scroll};", container)
        sleep(3)
    except Exception as e:
        print(f"Scrolling error: {e}")

def clean_folder(folder):
    """Removes all files inside the given folder."""
    if os.path.exists(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
