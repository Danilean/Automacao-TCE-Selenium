import os
import pandas as pd
from sqlalchemy import create_engine

def rename_duplicate_columns(df):
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in
                                                         range(sum(cols == dup))]
    df.columns = cols
    return df

def insert_dataframe_to_postgres(df, user, password, host, port, database, table_name):
    df.rename(columns={'Execução Orçamentária': 'Nova_Execução_Orçamentária'}, inplace=True)

    df = rename_duplicate_columns(df)

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f'Dados inseridos com sucesso na tabela {table_name}.')
    except Exception as e:
        print(f'Erro ao inserir dados: {e}')


pasta_downloads = r"C:\Users\danilo.formanski\Downloads\Arquivos-TCE"
arquivos_xlsx = [os.path.join(pasta_downloads, f) for f in os.listdir(pasta_downloads) if f.endswith('.xlsx')]
lista_dataframes = []

linha_ente = None
linha_ano_mes = None

for arquivo in arquivos_xlsx:
    df = pd.read_excel(arquivo, header=None)
    filtro_ente = df[df.iloc[:, 0] == "Ente"]
    if not filtro_ente.empty and linha_ente is None:
        linha_ente = filtro_ente

    filtro_ano_mes = df[df.iloc[:, 2].str.contains("Ano/Mês", na=False)]
    if not filtro_ano_mes.empty and linha_ano_mes is None:
        linha_ano_mes = filtro_ano_mes.iloc[0, :]

    df = df[(df.iloc[:, 0] != "Ente") & (df.iloc[:, 2] != "Ano/Mês Referência Informação") &
            (~df.apply(lambda row: row.astype(str).str.contains("###").any(), axis=1))]

    lista_dataframes.append(df)

df_concatenado = pd.concat(lista_dataframes, ignore_index=True)

if linha_ente is not None:
    df_concatenado.columns = linha_ente.values[0]

if linha_ano_mes is not None:
    df_concatenado.loc[-1] = linha_ano_mes.values
    df_concatenado.index = df_concatenado.index + 1
    df_concatenado = df_concatenado.sort_index()

coluna_ano_mes = None
for col in df_concatenado.columns:
    if "Ano/Mês" in col:
        coluna_ano_mes = col
        break

if coluna_ano_mes:
    df_concatenado = df_concatenado.drop_duplicates(subset=[coluna_ano_mes], keep="first")
else:
    print("A coluna 'Ano/Mês' não foi encontrada. Verifique os dados.")

caminho_arquivo_unificado = os.path.join(pasta_downloads, 'CSV_UNIFICADO_TCE.xlsx')
df_concatenado.to_excel(caminho_arquivo_unificado, index=False)
print(f"Arquivo salvo com sucesso em {caminho_arquivo_unificado}")

insert_dataframe_to_postgres(df_concatenado, "postgres", "postgress", "localHost", 8080, "postgres", "DadosTCE")