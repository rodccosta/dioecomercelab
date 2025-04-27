import streamlit as st

st.markdown("# Cadastrar novo produto ➕")
st.sidebar.markdown("# Novo Produto ➕")

# Formulário para cadastro do produto
product_name = st.text_input("Nome do Produto")
description = st.text_area("Descrição do Produto")
price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
#filetype = st.select_slider("Escolha a fonte da imagem", options=["URL","Selecionar Arquivo",])
filetype = st.pills(
    "Envio de Arquivos",
    ["URL","Selecionar Arquivo",],
        selection_mode="single")
if filetype == "URL":
    uploaded_file = st.text_input("Link da Imagem do Produto")
else:
    uploaded_file = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])




def load_json_file():
    import json
    with open('products.json') as f:
        products = json.load(f)
    return products

def write_json_file(products):
    import json    
    # the json file where the output must be stored
    out_file = open("products.json", "w")
    json.dump(products, out_file, indent = 6)
    out_file.close()

if st.button("Cadastrar Produto"):

    products = load_json_file()
    if not product_name or not description or price is None:
        st.warning("Preencha todos os campos obrigatórios!")
    else:
        # Anexa a lista do arquivo.
        image_url = ""
        if uploaded_file is not None:
            print(uploaded_file)
        
        # Dados do produto
        product_data = {
            "nome": product_name,
            "descricao": description,
            "preco": price,
            "imagem_url": image_url
        }
        products.append(product_data)
        write_json_file(products)