import os
from dotenv import load_dotenv
load_dotenv()

DOWNLOAD_FOLDER = os.getenv("PASTA_ORIGEM", "")
OUTPUT_FILE_NAME = os.getenv("NOME_ARQUIVO_SAIDA", "")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "")

TCE_LOGIN = os.getenv("TCE_LOGIN", "")
TCE_PASSWORD = os.getenv("TCE_PASSWORD", "")

POSTGRES_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "database": os.getenv("POSTGRES_DB"),
    "table_name": os.getenv("POSTGRES_TABLE")
}
