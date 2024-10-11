import os
import pandas as pd
from sqlalchemy import create_engine
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def insert_dataframe_to_postgres(df, user, password, host, port, database, table_name):
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    try:
        with engine.connect() as connection:
            connection.execute(f"DELETE FROM {table_name};")
            print(f"Tabela {table_name} limpa com sucesso.")

        df.to_sql(table_name, engine, if_exists='append', index=False)
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

def unificar_arquivos_xlsx(pasta_origem, nome_arquivo_saida):
    df_list = []

    if not os.path.exists(pasta_origem):
        print(f"Pasta {pasta_origem} não encontrada.")
        return

    for file_name in os.listdir(pasta_origem):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(pasta_origem, file_name)

            try:
                df = pd.read_excel(file_path, header=None)

                if df.shape[0] < 3:
                    print(f"Arquivo {file_name} não possui linhas suficientes.")
                    continue

                ente_ug_df = df.iloc[2:, [0, 1]].copy()
                ente_ug_df.columns = ['Ente', 'UG']

                tipos_nomes = df.iloc[1, 2:].tolist()
                tipos_nomes = [tipo for tipo in tipos_nomes if tipo != 'Assunto']

                datas = df.iloc[0, 2:].tolist()
                datas = [data for data in datas if data != "Ano/Mês Referência Informação"]

                for j in range(len(ente_ug_df)):
                    if j >= len(ente_ug_df):
                        break

                    temp_df = ente_ug_df.iloc[[j]].copy()
                    tipo_atual = tipos_nomes[j % len(tipos_nomes)]
                    temp_df['Tipo'] = tipo_atual

                    coluna_tipo = 2 + tipos_nomes.index(tipo_atual)
                    if coluna_tipo < df.shape[1]:
                        valor = df.iloc[j + 2, coluna_tipo]
                        temp_df['Valores'] = valor
                    else:
                        temp_df['Valores'] = None

                    if coluna_tipo < len(datas):
                        data_raw = datas[coluna_tipo - 2]
                        try:
                            temp_df['Data'] = pd.to_datetime(data_raw).strftime('%d/%m/%Y')
                        except Exception as e:
                            temp_df['Data'] = None
                    else:
                        temp_df['Data'] = None

                    df_list.append(temp_df)

                print(f"Arquivo processado: {file_name}")
            except Exception as e:
                print(f"Erro ao processar {file_name}: {e}")

    if df_list:
        df_concatenado = pd.concat(df_list, ignore_index=True)

        output_path = os.path.join(pasta_origem, nome_arquivo_saida)
        df_concatenado.to_excel(output_path, index=False)

        print(f"Arquivo XLSX unificado salvo em: {output_path}")

        # Inserir o DataFrame unificado no PostgreSQL
        insert_dataframe_to_postgres(df_concatenado, "postgres", "postgress", "localhost", 8080, "postgres", "DadosTCE")
    else:
        print("Nenhum arquivo XLSX foi processado.")

pasta_origem = r'C:\Users\danilo.formanski\Downloads\Arquivos-TCE'
nome_arquivo_saida = 'TABELA_TCE.xlsx'

def limpar_pasta(pasta):
    for arquivo in os.listdir(pasta):
        file_path = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
        except Exception as e:
            print(f"Erro ao remover {file_path}: {e}")

def iniciar_driver():
    chrome_options = Options()
    download_dir = r"C:\Users\danilo.formanski\Downloads\Arquivos-TCE"
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver

def fazer_login(driver):
    try:
        driver.get('https://virtual.tce.sc.gov.br/web/#/home')
        wait = WebDriverWait(driver, 15)
        nome = wait.until(EC.presence_of_element_located((By.ID, 'codigo')))
        nome.send_keys('05388407900')
        senha = driver.find_element(By.ID, 'nova')
        senha.send_keys('Campeao1')
        botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
        botao_enviar.click()
    except Exception as e:
        driver.quit()
        main()

def navegar_para_extrato(driver):
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]')))
        menu_tce_virtual = driver.find_element(By.XPATH, '//span[@class="glyphicon glyphicon-menu-hamburger"]')
        menu_tce_virtual.click()
        paineis_controle_interno = wait.until(EC.element_to_be_clickable((By.XPATH, '//h3[text()="Painéis Controle Interno"]')))
        paineis_controle_interno.click()
        extrato = wait.until(EC.element_to_be_clickable((By.XPATH, '//p[text()="E-SFINGE ONLINE – EXTRATO"]')))
        extrato.click()
    except Exception as e:
        driver.quit()
        main()

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
        main()

def realizar_scroll(driver, container_css, pixels_to_scroll):
    try:
        container = driver.find_element(By.CSS_SELECTOR, container_css)
        driver.execute_script(f"arguments[0].scrollTop += {pixels_to_scroll};", container)
        sleep(3)
    except Exception as e:
        driver.quit()
        main()

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
        main()

def main():
    driver = iniciar_driver()
    fazer_login(driver)
    navegar_para_extrato(driver)
    alternar_para_nova_aba(driver)
    realizar_downloads(driver)
    unificar_arquivos_xlsx(pasta_origem, nome_arquivo_saida)
    limpar_pasta(pasta_origem)
    driver.quit()

if __name__ == "__main__":
    main()