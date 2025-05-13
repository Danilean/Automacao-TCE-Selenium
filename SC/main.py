from acesso_tce import acessar_painel_tce
from database import unificar_arquivos_xlsx
from driver_setup import iniciar_driver
from login import fazer_login
from navigation import navegar_para_extrato, alternar_para_nova_aba, realizar_downloads
from utils import limpar_pasta
import os
from config import PASTA_ORIGEM, NOME_ARQUIVO_SAIDA
import traceback

def executar_processo():
    driver = iniciar_driver()
    try:
        fazer_login(driver)
        acessar_painel_tce(driver)
        navegar_para_extrato(driver)
        alternar_para_nova_aba(driver)

        if realizar_downloads(driver):
            print("Download realizado com sucesso. Processando arquivos...")
            unificar_arquivos_xlsx(PASTA_ORIGEM, NOME_ARQUIVO_SAIDA)
            limpar_pasta(PASTA_ORIGEM)
            return True
        else:
            print("Falha ao realizar downloads.")
            return False
    except Exception as e:
        print("Erro durante o processo:", e)
        traceback.print_exc()
        return False
    finally:
        driver.quit()

def main():
    sucesso = executar_processo()
    if not sucesso:
        print("Reiniciando processo após limpar pasta...")
        limpar_pasta(PASTA_ORIGEM)
        executar_processo()

if __name__ == "__main__":
    main()
