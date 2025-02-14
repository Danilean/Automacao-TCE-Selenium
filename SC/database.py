import os
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text

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
