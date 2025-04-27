# dioecomercelab
Laboratório do módulo Armazenando dados de um E-Commerce na Cloud

![E-comerce](https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grgdg0txqvhh/b/bucket-test-rod-sp1/o/snaps/github-ecomerce-1resultado1.png)
![Upload](https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grgdg0txqvhh/b/bucket-test-rod-sp1/o/snaps/github-ecomerce-1resultado2.png)


## Considerações Iniciais
Na aula do módulo, o professor já começa a fazer toda a codificação e não explica o setup inicial para desenvolver o projeto para resolução do problema, desta forma, neste repositório iremos descrever realizar de forma mais básica o desenvolvimento do projeto realizando a seguinte sequência de passos:
* [Setup do ambiente de desenvolvimento](#setup)
* [Desenvolvimento da interface para envio de produto](#stramlit)
* [Persistência em Arquivo](#json)
* [Carregamento de credenciais em arquivo .env](#dotenv)
* [Troca de Azure Blobs por OCI Bucket Objects](#oci)

Além disto, a DIO não oferece contas de usuário para realizar o laboratório com conexão da azure. Como possuo conta na ([Oracle Cloud Infrastructure - OCI](https://cloud.oracle.com/) e minha conta é always free, então vou utilizar esta nuvem para este laboratório.

### Setup do ambiente de desenvolvimento
O projeto é desenvolvido em Python utilizando o vscode, além disso, o projeto utiliza algumas dependências, apresentadas no arquivo requeriments.txt. Para simplificação da instalação utilizamos a ferramenta [Chocolatey](https://chocolatey.org) no windows utilizando o comando:
```sh
choco install python3 vscode
pip install -r requirements.txt
```
Após a instalação, abrimos o vscode e realizamos a instalação dos plugins de python e stremalit
![Extensão Python](https://us-east-2-prod-datasource-bucket.s3.us-east-2.amazonaws.com/uploads/302d3364e0134f43e909c34b77ef948b.png)
Após a instalação das extensões, podemos executar o main.py criado no projeto clicando com o botão direito no arquivo main.py
![Extensão Streamlit](https://global.discourse-cdn.com/streamlit/original/3X/2/5/25dabc428d925c445c6c6384744208a1c6b96284.png)

### Desenvolvimento da interface para envio de produto
Na aula, como o desenvolvimento é feito para explicar como fazer a interação com a nuvem, todo desenvolvimento é feito um único arquivo main.py. O streamlit é muito poderoso e permite a criação de sites de forma bem interessante. E resolvemos fazer o desenvolvimento utilzando duas páginas
* Página Principal que contem a listagem dos produtos cadastrados (main_page.py)
* Página para cadastro de novos produtos (page_2.py)

Por causa disto, utilizamos o streamlit utilizando a estrutura de páginas, por isso que nosso main.py possui a estrutura da página com site de navegação lateral (sidebar)
```python
# Configurando as páginas
main_page = st.Page("main_page.py", title="Página Principal", icon="🎉")
page_2 = st.Page("page_2.py", title="Cadastrar Novo Produto", icon="➕")

# Configurando a navegação
pg = st.navigation([main_page, page_2])

# Executar a página selecionada
pg.run()
```

### Persistência em Arquivo
Para simplificar a compreensão do código da interface de envio de arquivos, implementamos a persistência de arquivo utilizando o dump de arquivo json. Para isso, criamos um arquivo myjson.py onde colocamos duas funções
* load_json_file(): para carregar os produtos do arquivo
* write_json_file(products): para salvar os produtos no arquivo json.

Além disto, para permitir a depuração da persistência, foi colocado um widget de pílulas para permitir escolher se cadastramos uma imagem por url digitada ou selecionamos o arquivo.

Ao clicar no botão cadastrar produto, o produto é inserido no .json e os produtos são organizados por nome em ordem alfabética.

Para persistência das imagens, foi feita a conversão da imagem para data_uri utilizando a função criada no arquivo utils.py
```python
gerar_data_uri(uploaded_file.getvalue(),mime_type=uploaded_file.type))
```
### Carregamento de credenciais em arquivo .env
O código criado deixa hard coded informações de credenciais de acessso a nuvem. Desta forma, foi utilizado o arquivo .env para deixar as credenciais criadas. Para usar este repositório você deve criar um arquivo.env com o seguinte conteúdo:
```sh
TENANCY_OCID=ocid1.tenancy.oc1...
USER_OCID=ocid1.user.oc1...
BUCKET_OCID=ocid1.bucket.oc1...
FINGERPRINT=XX:XX:XX:XX:XX:XX:XX:XX:XX::XX:XX:XX:XX:XX:XX
PRIVATE_KEY_PATH=./filekey.pem
REGION=......
BUCKET_NAME=....
```
No arquivo utils.py essas informçaões são carregadas e são colocadas no formato de configuração solicitado pela OCI.

### Interagindo com a OCI
A interação com os buckets OCI é mais simples que a Azure Blob, para isto, devemos carregar as informações de conexão usando os comandos:
```python
from dotenv import load_dotenv
# Carrega variáveis do arquivo .env
load_dotenv()

config = {
    "user": os.getenv('USER_OCID'),
    "fingerprint": os.getenv('FINGERPRINT'),
    "key_file": os.getenv('PRIVATE_KEY_PATH'),
    "tenancy": os.getenv('TENANCY_OCID'),
    "region": os.getenv('REGION')
}
import oci
# Cria o cliente de objetos
object_storage_client = oci.object_storage.ObjectStorageClient(config)
```
A partir deste cliente, usamos os comandos para interagir com o bucket:
* object_storage_client.list_objects(namespace, bucket_name,  fields="name,timeCreated,size") : lista os arquivos presentes no bucket
* object_storage_client.put_object(namespace,bucket_name,filename,content): envia o arquivo para o bucket.

### Banco na OCI - Autonomous
Na OCI A criação SQL é um pouco diferente:
```
CREATE TABLE Produtos (
            id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
            nome VARCHAR(255),
            descricao VARCHAR(2000),
            preco FLOAT,
            imagem_url VARCHAR(2083)
        )
```
Similarmente ao serviço de bucket, o AUTONOMOUS DATABASE SERVICE da OCI precisa de variáveis de ambiente a serem configuradas no .env
```
SQL_USERNAME=....
SQL_PASSWORD=....
SQL_CONSTRING=(description= ....
```
As funções para interação com o banco de dados estão disponíveis no arquivo ocisql.py. Foi necessário ir nas configurações do banco de dados e incluir o IP público que estamos acessando para poder permitir as conexões no banco de dados. Além disto, foi desabilitado o mTSL para facilitar o processo de carregamento das informações pela biblioteca oracledb.

```Python
import oracledb
import os
from dotenv import load_dotenv
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_CONSTRING =os.getenv('SQL_CONSTRING')
oracledb.init_oracle_client()
conn = oracledb.connect(user=SQL_USERNAME, password=SQL_PASSWORD,dsn=SQL_CONSTRING)#, dsn=dsn_tns, config_dir=wallet_location, wallet_location=wallet_location, wallet_password=SQL_PASSWORD)
cursor = conn.cursor()
```
A partir destas informações, foram criadas duas funções
* `insert_product_sql(product_data)`: inserir produto no banco de dados da nuvem
* `list_products_sql()`: listar produtos no banco de dados da nuvem
## Histórico de versões
* Versão 1: Persistência em Arquivo JSON com imagens armazenadas em JSON.
* Versão 2: Persistência em Arquivo JSON com imagens armazenadas em Bucket.
* Versão 3: Persistência em SQL com imagens armazenadas em Bucket.
