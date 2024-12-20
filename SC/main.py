import os
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from acesso_tce import acessar_painel_tce

load_dotenv()

def insert_dataframe_to_postgres(df: DataFrame, user: str, password: str, host: str, port: int, database: str, table_name: str) -> None:
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
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
                datas_meses = df.iloc[0, 2:].tolist()

                for j in range(len(ente_ug_df)):
                    for idx, tipo in enumerate(tipos_nomes):
                        temp_df = ente_ug_df.iloc[[j]].copy()
                        temp_df['Tipo'] = tipo
                        coluna_tipo = 2 + idx

                        valor = df.iloc[j + 2, coluna_tipo] if coluna_tipo < df.shape[1] else None
                        temp_df['Valores'] = valor

                        data_raw = datas_meses[idx]
                        try:
                            temp_df['Data'] = pd.to_datetime(data_raw).strftime('%m/%Y')
                        except Exception as e:
                            temp_df['Data'] = None

                        df_list.append(temp_df)

                print(f"Arquivo processado: {file_name}")
            except Exception as e:
                print(f"Erro ao processar {file_name}: {e}")

    if df_list:
        df_concatenado = pd.concat(df_list, ignore_index=True)

        municipios_betha = [
            'ABDON BATISTA', 'AGROLÂNDIA', 'ÁGUA DOCE', 'ÁGUAS DE CHAPECÓ', 'ÁGUAS MORNAS', 'ALFREDO WAGNER',
            'ANCHIETA', 'ANGELINA', 'ANITA GARIBALDI', 'ANITÁPOLIS', 'ANTÔNIO CARLOS', 'ARMAZÉM', 'ATALANTA',
            'BALNEÁRIO ARROIO DO SILVA', 'BALNEÁRIO GAIVOTA', 'BALNEÁRIO RINCÃO', 'BANDEIRANTE', 'BELA VISTA DO TOLDO',
            'BELMONTE', 'BOCAINA DO SUL', 'BOM JARDIM DA SERRA', 'BOM JESUS', 'BRAÇO DO NORTE', 'BRAÇO DO TROMBUDO',
            'BRUNÓPOLIS', 'CAMPO ALEGRE', 'CAMPO BELO DO SUL', 'CAMPO ERÊ', 'CAMPOS NOVOS', 'CANELINHA', 'CAPINZAL',
            'CAPIVARI DE BAIXO', 'CATANDUVAS', 'CELSO RAMOS', 'CERRO NEGRO', 'CHAPECÓ', 'CIM - GRANDE FLORIANÓPOLIS',
            'CIS - GRANFPOLIS', 'COCAL DO SUL', 'CONCÓRDIA',
            'CONS. INTERM. SAÚDE DA MICRO REGIÃO DA AMURES (CISAMURES)',
            'CONSÓRCIO CIDAUC', 'CONSÓRCIO CIM AMAI', 'CONSÓRCIO INTERMUNICIPAL ABRIGO CASA LAR - CIALAR',
            'CONSÓRCIO INTERMUNICIPAL DE GERENCIAMENTO AMBIENTAL - IBERE', 'CORDILHEIRA ALTA', 'CORONEL FREITAS',
            'CORONEL MARTINS', 'CORREIA PINTO', 'CRICIÚMA', 'CRICIÚMA', 'CUNHATAÍ', 'CURITIBANOS', 'CURITIBANOS',
            'DESCANSO', 'DIONÍSIO CERQUEIRA', 'DONA EMMA', 'ENTRE RIOS', 'ERMO', 'ERVAL VELHO', 'FAXINAL DOS GUEDES',
            'FLORIANÓPOLIS', 'FORMOSA DO SUL', 'FORQUILHINHA', 'FREI ROGÉRIO', 'GALVÃO', 'GOVERNADOR CELSO RAMOS',
            'GRÃO PARÁ', 'HERVAL DOESTE', 'IBIAM', 'IBICARÉ', 'IÇARA', 'IMARUÍ', 'IMBITUBA', 'IMBUIA', 'IOMERÊ',
            'IPIRA', 'IPUAÇU', 'IPUMIRIM', 'IRACEMINHA', 'IRATI', 'ITAIÓPOLIS', 'ITAJAÍ', 'ITAPEMA', 'JABORÁ',
            'JACINTO MACHADO', 'JARAGUÁ DO SUL', 'JOAÇABA', 'JUPIÁ', 'LACERDÓPOLIS', 'LAGES', 'LAGUNA',
            'LAJEADO GRANDE',
            'LAURO MÜLLER', 'LEOBERTO LEAL', 'LINDÓIA DO SUL', 'LUZERNA', 'MACIEIRA', 'MAJOR GERCINO', 'MAJOR VIEIRA',
            'MARACAJÁ', 'MARAVILHA', 'MAREMA', 'MATOS COSTA', 'MELEIRO', 'MONDAÍ', 'MONTE CARLO', 'MONTE CASTELO',
            'MORRO DA FUMAÇA', 'MORRO GRANDE', 'NAVEGANTES', 'NOVA ERECHIM', 'NOVA TRENTO', 'NOVA TRENTO',
            'NOVA VENEZA',
            'NOVA VENEZA', 'NOVO HORIZONTE', 'ORLEANS', 'OTACÍLIO COSTA', 'PAINEL', 'PALMITOS', 'PAPANDUVA',
            'PASSO DE TORRES', 'PASSOS MAIA', 'PAULO LOPES', 'PEDRAS GRANDES', 'PESCARIA BRAVA', 'PETROLÂNDIA',
            'PIRATUBA', 'PONTE ALTA', 'PONTE ALTA DO NORTE', 'PONTE SERRADA', 'PORTO UNIÃO', 'POUSO REDONDO',
            'PRAIA GRANDE', 'PRESIDENTE CASTELLO BRANCO', 'QUILOMBO', 'RANCHO QUEIMADO', 'RIO DO SUL', 'RIO FORTUNA',
            'RIO RUFINO', 'SALTINHO', 'SALTO VELOSO', 'SANGÃO', 'SANTA CECÍLIA', 'SANTA ROSA DE LIMA',
            'SANTA TEREZINHA', 'SANTA TEREZINHA DO PROGRESSO', 'SANTO AMARO DA IMPERATRIZ', 'SANTO AMARO DA IMPERATRIZ',
            'SÃO BERNARDINO', 'SÃO BONIFÁCIO', 'SÃO CRISTÓVÃO DO SUL', 'SÃO DOMINGOS', 'SÃO FRANCISCO DO SUL',
            'SÃO JOÃO BATISTA', 'SÃO JOÃO DO OESTE', 'SÃO JOAQUIM', 'SÃO JOSÉ DO CERRITO', 'SÃO LOURENÇO DO OESTE',
            'SÃO LUDGERO', 'SÃO MARTINHO', 'SÃO MIGUEL DA BOA VISTA', 'SÃO MIGUEL DO OESTE', 'SÃO PEDRO DE ALCÂNTARA',
            'SCHROEDER', 'SEARA', 'SIDERÓPOLIS', 'SOMBRIO', 'TANGARÁ', 'TIGRINHOS', 'TREZE DE MAIO', 'TROMBUDO CENTRAL',
            'TUBARÃO', 'TUBARÃO', 'TUNÁPOLIS', 'TURVO', 'UNIÃO DO OESTE', 'URUBICI', 'URUSSANGA', 'VARGEÃO',
            'VARGEM', 'VARGEM BONITA', 'VIDAL RAMOS', 'XANXERÊ', 'XAVANTINA', 'XAXIM'
        ]

        df_concatenado['Clientes'] = df_concatenado['Ente'].apply(
            lambda x: "Betha Sistemas" if x in municipios_betha else "Concorrente")

        df_concatenado = df_concatenado.sort_values(by=["Ente", "Data"], ascending=[True, True])

        output_path = os.path.join(pasta_origem, nome_arquivo_saida)
        df_concatenado.to_excel(output_path, index=False)
        print(f"Arquivo XLSX unificado salvo em: {output_path}")

        conexao_db = {
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "database": os.getenv("POSTGRES_DB"),
            "table_name": os.getenv("POSTGRES_TABLE")
        }

        if all(conexao_db.values()):
            insert_dataframe_to_postgres(df_concatenado, **conexao_db)
        else:
            print("Erro: Configurações de conexão com o banco de dados estão incompletas.")
    else:
        print("Nenhum arquivo XLSX foi processado.")

pasta_origem = os.getenv("PASTA_ORIGEM")
nome_arquivo_saida = os.getenv("NOME_ARQUIVO_SAIDA")

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
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')

    download_dir = os.getenv("PASTA_ORIGEM")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service(os.getenv("CHROME_DRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver

def fazer_login(driver):
    try:
        driver.get('https://virtual.tce.sc.gov.br/web/#/home')
        wait = WebDriverWait(driver, 15)
        nome = wait.until(EC.presence_of_element_located((By.ID, 'codigo')))
        nome.send_keys(os.getenv("TCE_LOGIN"))
        senha = driver.find_element(By.ID, 'nova')
        senha.send_keys(os.getenv("TCE_PASSWORD"))
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
    acessar_painel_tce()
    navegar_para_extrato(driver)
    alternar_para_nova_aba(driver)
    realizar_downloads(driver)
    unificar_arquivos_xlsx(pasta_origem, nome_arquivo_saida)
    limpar_pasta(pasta_origem)
    driver.quit()

if __name__ == "__main__":
    main()