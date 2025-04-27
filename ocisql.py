import os
from dotenv import load_dotenv
import pymssql

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_CONSTRING =os.getenv('SQL_CONSTRING')

#import cx_Oracle
import oracledb
# Defina o caminho para o wallet
#dsn_tns = oracledb.makedsn("hostname", "port", service_name="service_name")
oracledb.init_oracle_client()

# Conecte-se ao banco de dados


def insert_product_sql(product_data):
    try:
        conn = oracledb.connect(user=SQL_USERNAME, password=SQL_PASSWORD,dsn=SQL_CONSTRING)#, dsn=dsn_tns, config_dir=wallet_location, wallet_location=wallet_location, wallet_password=SQL_PASSWORD)

        cursor = conn.cursor()

        
        # Insere os dados do produto
        insert_query = """
        INSERT INTO Produtos (nome, descricao, preco, imagem_url)
        VALUES (%s, %s, %s, %s)
        """
        insert_query = "INSERT INTO Produtos(NOME,DESCRICAO,PRECO,IMAGEM_URL) values (:nome,:descricao,:preco,:IMAGEM_URL)"
        nome = product_data["nome"]
        descricao=product_data["descricao"]
        preco=product_data["preco"]
        url=product_data["imagem_url"]
        cursor.execute(insert_query, [nome,descricao,preco,url])
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        raise e

# Função para listar os produtos do Azure SQL Server
def list_products_sql():
    try:
        conn = oracledb.connect(user=SQL_USERNAME, password=SQL_PASSWORD,dsn=SQL_CONSTRING)#, config_dir=wallet_location, wallet_location=wallet_location, wallet_password=SQL_PASSWORD)
        # Usamos cursor com dict=True para facilitar a conversão para DataFrame
        cursor = conn.cursor()
        query = "SELECT id, nome, descricao, preco, imagem_url FROM Produtos"
        cursor.execute(query)
        desc = cursor.description
        column_names = ["id","nome","descricao","preco","imagem_url"]
        data = [dict(zip(column_names, row))  
            for row in cursor.fetchall()]
        print(data)
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise e