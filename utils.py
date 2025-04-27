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
