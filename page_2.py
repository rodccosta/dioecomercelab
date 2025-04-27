import streamlit as st
from myjson import *
from utils import *
from ocisql import *
import uuid
st.markdown("# Cadastrar novo produto ➕")
st.sidebar.markdown("# Novo Produto ➕")

# Formulário para cadastro do produto
product_name = st.text_input("Nome do Produto")
description = st.text_area("Descrição do Produto")
price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
#filetype = st.select_slider("Escolha a fonte da imagem", options=["URL","Selecionar Arquivo",])
filetype = st.pills(
    "Selecione o tipo de Envio de Imagem",
    ["URL","Selecionar Arquivo",],
        selection_mode="single")
if filetype == "URL":
    uploaded_file = st.text_input("Link da Imagem do Produto")
elif filetype == "Selecionar Arquivo":
    uploaded_file = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"],accept_multiple_files =False)


if st.button("Cadastrar Produto"):

    products = load_json_file()
    if not product_name or not description or price is None:
        st.warning("Preencha todos os campos obrigatórios!")
    else:
        # Anexa a lista do arquivo.
        image_url = ""
        if filetype == "URL":
            image_url = uploaded_file 
        elif uploaded_file is not None:
            object_name = f"{uuid.uuid4()}.jpg" #gera um nome único
            image_url = adicionar_objetos(object_name,uploaded_file)
            
            #image_url = str(gerar_data_uri(uploaded_file.getvalue(),mime_type=uploaded_file.type))

        
        # Dados do produto
        product_data = {
            "nome": product_name,
            "descricao": description,
            "preco": price,
            "imagem_url": image_url
        }
        try:
            insert_product_sql(product_data)
            st.success("Produto cadastrado com sucesso no OCI SQL!")
        except Exception as e:
            st.error(f"Erro ao inserir no OCI SQL: {e}")

        #products.append(product_data)
        #product_data_ordenado = sorted(products, key=lambda x: x['nome'])
        #write_json_file(product_data_ordenado)