import os
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def insert_dataframe_to_postgres(df: DataFrame, user: str, password: str, host: str, port: int, database: str, table_name: str) -> None:
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    with engine.begin() as conn:
        try:
            table_exists_query = f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table_name}'
                );
            """
            table_exists = conn.execute(text(table_exists_query)).scalar()

            if not table_exists:
                create_table_query = f"""
                    CREATE TABLE {table_name} (
                    id SERIAL PRIMARY KEY,
                    entidade VARCHAR(244) COLLATE "und-x-icu",
                    uniao_gestora VARCHAR(244) COLLATE "und-x-icu",
                    tipo VARCHAR(244) COLLATE "und-x-icu",
                    valor DOUBLE PRECISION,
                    periodo VARCHAR(244) COLLATE "und-x-icu" 
                    );
                """
                conn.execute(text(create_table_query))
                print(f"Tabela {table_name} criada.")

            for _, row in df.iterrows():
                delete_query = text(f'''
                    DELETE FROM {table_name}
                    WHERE entidade = :entidade AND tipo = :tipo AND periodo = :periodo
                ''')
                conn.execute(delete_query, {
                    'entidade': row['entidade'],
                    'tipo': row['tipo'],
                    'periodo': row['periodo']
                })

            df.drop(columns=["id"], errors="ignore").to_sql(table_name, conn, if_exists='append', index=False)
            print("Dados inseridos/atualizados com sucesso.")

        except Exception as e:
            print(f"Erro ao inserir dados: {e}")

def limpar_valores(valor):
    if pd.isna(valor) or valor == "-" or str(valor).strip() == "":
        return None
    try:
        return float(valor)
    except Exception:
        return None

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

                entidade_ug_df = df.iloc[2:, [0, 1]].copy()
                entidade_ug_df.columns = ['entidade', 'uniao_gestora']

                tipos_nomes = df.iloc[1, 2:].tolist()
                datas_meses = df.iloc[0, 2:].tolist()

                for j in range(len(entidade_ug_df)):
                    for idx, tipo in enumerate(tipos_nomes):
                        temp_df = entidade_ug_df.iloc[[j]].copy()
                        temp_df['tipo'] = tipo
                        coluna_tipo = 2 + idx

                        valor = df.iloc[j + 2, coluna_tipo] if coluna_tipo < df.shape[1] else None
                        temp_df['valor'] = valor

                        data_raw = datas_meses[idx]
                        temp_df['periodo'] = str(data_raw)

                        df_list.append(temp_df)

                print(f"Arquivo processado: {file_name}")
            except Exception as e:
                print(f"Erro ao processar {file_name}: {e}")

    if df_list:
        df_concatenado = pd.concat(df_list, ignore_index=True)
        df_concatenado["valor"] = df_concatenado["valor"].apply(limpar_valores)

        df_concatenado = df_concatenado.sort_values(by=["entidade", "periodo"], ascending=[True, True])

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
