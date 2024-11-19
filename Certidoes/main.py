import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "https://api.virtual.tce.sc.gov.br/certidao/rest/visualizador/getCertidaoPorAno/0"
DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB")
}

def fetch_data_from_api():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao acessar API: {response.status_code}")

def format_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%d/%m/%Y')

def process_data(data):
    processed_data = []
    for item in data:
        try:
            data1 = format_date(item.get('data1', 0))
            data2 = format_date(item.get('data2', 0))
            data3 = format_date(item.get('data3', 0))
            data4 = format_date(item.get('data4', 0))

            periodo1 = f"{data2} - {data1}"
            periodo2 = f"{data4} - {data3}"

            processed_data.append(
                (
                    item.get('nome', 'N/A'),
                    item.get('identificadorEnte', 'N/A'),
                    periodo1,
                    periodo2,
                    item.get('q1Lrf', 'N/A'),
                    item.get('q1Sef', 'N/A'),
                    item.get('q1Oci', 'N/A'),
                    item.get('q1Positiva', 'N/A'),
                    item.get('q2Lrf', 'N/A'),
                    item.get('q2Sef', 'N/A'),
                    item.get('q2Oci', 'N/A'),
                    item.get('q2Positiva', 'N/A'),
                    item.get('q3Lrf', 'N/A'),
                    item.get('q3Sef', 'N/A'),
                    item.get('q3Oci', 'N/A'),
                    item.get('q3Positiva', 'N/A')
                )
            )
        except KeyError as e:
            print(f"Chave ausente no item: {e}")
    return processed_data

def insert_data_to_postgres(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS certificados")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS certificados (
                nome VARCHAR(255),
                identificadorEnte INTEGER,
                periodo1 VARCHAR(50),
                periodo2 VARCHAR(50),
                q1Lrf VARCHAR(50),
                q1Sef VARCHAR(50),
                q1Oci VARCHAR(50),
                q1Positiva VARCHAR(50),
                q2Lrf VARCHAR(50),
                q2Sef VARCHAR(50),
                q2Oci VARCHAR(50),
                q2Positiva VARCHAR(50),
                q3Lrf VARCHAR(50),
                q3Sef VARCHAR(50),
                q3Oci VARCHAR(50),
                q3Positiva VARCHAR(50)
            );
        """)
        insert_query = sql.SQL("""
            INSERT INTO certificados (
                nome, identificadorEnte, periodo1, periodo2,
                q1Lrf, q1Sef, q1Oci, q1Positiva, 
                q2Lrf, q2Sef, q2Oci, q2Positiva, 
                q3Lrf, q3Sef, q3Oci, q3Positiva
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        cur.executemany(insert_query, data)
        conn.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def main():
    data = fetch_data_from_api()
    processed_data = process_data(data)
    insert_data_to_postgres(processed_data)

if __name__ == "__main__":
    main()
