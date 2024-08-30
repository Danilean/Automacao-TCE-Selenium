import logging
from datetime import datetime

def collate(iterable, n):
    from itertools import islice
    iterator = iter(iterable)
    while True:
        chunk = list(islice(iterator, n))
        if not chunk:
            break
        yield chunk

def setup_logging():
    logging.basicConfig(
        filename='automation.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def capture_screenshot(driver, name="screenshot"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename
