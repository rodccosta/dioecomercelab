import os
from dotenv import load_dotenv
import time
import oci
import oracledb
from utils import *
import sys
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_CONSTRING =os.getenv('SQL_CONSTRING')



config = {
    "user": os.getenv('USER_OCID'),
    "fingerprint": os.getenv('FINGERPRINT'),
    "key_file": os.getenv('PRIVATE_KEY_PATH'),
    "tenancy": os.getenv('TENANCY_OCID'),
    "region": os.getenv('REGION')
}

# Cria o client do banco de dados
db_client = oci.database.DatabaseClient(config)

# OCID da instância do Autonomous Database
autonomous_db_ocid = os.getenv("SQL_SERVER")

# Iniciar o banco
response = db_client.get_autonomous_database(autonomous_db_ocid)
status = response.data.lifecycle_state
print(f"Status atual: {status}")
if status != "AVAILABLE":
    db_client.start_autonomous_database(autonomous_db_ocid)

meu_novo_ip = get_public_ip()
db_data = response.data

# Copia ACL atual e adiciona novo IP se não estiver já
#acl = db_data.access_control_list or []
acl = getattr(db_data, 'whitelisted_ips', None) or []
print(acl)
# Adiciona IP se ainda não estiver
if meu_novo_ip not in acl:
    raise Exception("ℹ️ IP já nao está na whitelist do OCI Autonomous Database. Abra o console e inclua o IP")

    

while True:
    response = db_client.get_autonomous_database(autonomous_db_ocid)
    status = response.data.lifecycle_state
    print(f"Status atual: {status}")
    
    if status == "AVAILABLE":
        print("✅ Banco de dados está disponível!")
        break

    time.sleep(10)  # espera 10 segundos antes de checar de novo

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

def remove_product_sql(nome):
    try:
        conn = oracledb.connect(user=SQL_USERNAME, password=SQL_PASSWORD,dsn=SQL_CONSTRING)#, dsn=dsn_tns, config_dir=wallet_location, wallet_location=wallet_location, wallet_password=SQL_PASSWORD)

        cursor = conn.cursor()

        
        # Insere os dados do produto
        
        insert_query = "DELETE FROM Produtos WHERE NOME=:nome"
        cursor.execute(insert_query, [nome])
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        raise e