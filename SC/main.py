import os

from acesso_tce import acessar_painel_tce
from database import unificar_arquivos_xlsx
from driver_setup import iniciar_driver
from login import fazer_login
from navigation import navegar_para_extrato, alternar_para_nova_aba, realizar_downloads
from utils import limpar_pasta

pasta_origem = os.getenv("PASTA_ORIGEM")
nome_arquivo_saida = os.getenv("NOME_ARQUIVO_SAIDA")

def main():
    driver = iniciar_driver()
    fazer_login(driver)
    acessar_painel_tce()
    navegar_para_extrato(driver)
    alternar_para_nova_aba(driver)
    realizar_downloads(driver)
    unificar_arquivos_xlsx(pasta_origem, nome_arquivo_saida)
    limpar_pasta(pasta_origem)
    driver.quit()

if __name__ == "__main__":
    main()
