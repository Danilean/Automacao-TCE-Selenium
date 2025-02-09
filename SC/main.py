from driver_setup import start_driver
from login import login
from navigation import navigate_to_extrato
from download import download_files
from utils import clean_folder
from config import DOWNLOAD_FOLDER


def main():
    driver = start_driver()
    login(driver)
    navigate_to_extrato(driver)
    download_files(driver)

    clean_folder(DOWNLOAD_FOLDER)
    driver.quit()


if __name__ == "__main__":
    main()
