# dioecomercelab
Laboratório do módulo Armazenando dados de um E-Commerce na Cloud

## Considerações Iniciais
Na aula do módulo, o professor já começa a fazer toda a codificação e não explica o setup inicial para desenvolver o projeto para resolução do problema, desta forma, neste repositório iremos descrever realizar de forma mais básica o desenvolvimento do projeto realizando a seguinte sequência de passos:
* [Setup do ambiente de desenvolvimento](#setup)
* [Desenvolvimento da interface para envio de produto](#stramlit)
* [Persistência em Arquivo](#json)

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

## Histórico de versões
* Versão 1: Persistência em Arquivo JSON com imagens armazenadas em JSON.
* Versão 2 [TODO]: Persistência em Arquivo JSON com imagens armazenadas em Bucket.
* Versão 3 [TODO]: Persistência em SQL com imagens armazenadas em Bucket.
