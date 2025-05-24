import base64

def gerar_data_uri(imagem_bytes, mime_type='image/jpeg'):
    # Codifica os bytes para base64
    imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')
    # Monta a data URI
    data_uri = f'data:{mime_type};base64,{imagem_base64}'
    return data_uri

import os
from dotenv import load_dotenv
import oci

# Carrega variáveis do arquivo .env
load_dotenv()

# Monta o config manualmente
config = {
    "user": os.getenv('USER_OCID'),
    "fingerprint": os.getenv('FINGERPRINT'),
    "key_file": os.getenv('PRIVATE_KEY_PATH'),
    "tenancy": os.getenv('TENANCY_OCID'),
    "region": os.getenv('REGION')
}

# Cria o cliente
object_storage_client = oci.object_storage.ObjectStorageClient(config)

# Usa normalmente
namespace = object_storage_client.get_namespace().data
print(f'Namespace: {namespace}')
bucketname = os.getenv('BUCKET_NAME')

def listar_objetos(bucket_name=bucketname):
    object_list = object_storage_client.list_objects(namespace, bucket_name,  fields="name,timeCreated,size")
    filelists=""
    for o in object_list.data.objects:
        print(o.name)
        filelists+=o.name+'\n'
    return filelists

def adicionar_objetos(filename,content,bucket_name=bucketname):
    object_storage_client.put_object(namespace,bucket_name,filename,content)
    return "https://objectstorage."+os.getenv('REGION')+".oraclecloud.com/n/"+namespace+"/b/"+bucket_name+"/o/"+filename

from urllib.parse import unquote
import re

def remover_objeto_por_url_simples(url):
    if "oraclecloud.com" not in url:
        print("❌ URL não parece ser do Oracle Object Storage.")
        return False

    try:
        # Extrai partes relevantes da URL
        partes = url.split("/o/")
        if len(partes) != 2:
            print("❌ URL malformada. Esperado '/o/<nome_do_arquivo>'.")
            return False

        filename = unquote(partes[1])
        match = re.search(r"/n/([^/]+)/b/([^/]+)/", url)
        if not match:
            print("❌ Não foi possível extrair namespace e bucket da URL.")
            return False

        namespace = match.group(1)
        bucket = match.group(2)

        object_storage_client.delete_object(namespace, bucket, filename)
        print(f"🗑️ Objeto '{filename}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover objeto: {e}")
        return False

import requests

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Erro ao obter IP público: {e}")
        return None

