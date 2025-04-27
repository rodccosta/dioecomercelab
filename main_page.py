import streamlit as st
from myjson import *

# Main page content
st.markdown("# Produtos Disponíveis - E-Commerce na Cloud🍔")
st.sidebar.markdown("# Página Principal 🍔")


def loaddummydata():
    product_data=[]
    product = {
            "nome": "Coca cola KS",
            "descricao": "Coca Cola 290ml",
            "preco": 4.00,
            "imagem_url": "https://media.istockphoto.com/id/499208007/pt/foto/cl%C3%A1ssico-coca-cola-em-um-frasco-de-vidro.jpg?s=612x612&w=0&k=20&c=UQdnP3aWXzItGUt-wECZwA3_zzTA5_XhMZ1-d4UQSZ8="
        }
    product_data.append(product)
    product = {
            "nome": "Lata Guaraná",
            "descricao": "Lata de 300ml do Guaraná Antártica",
            "preco":  5.00,
            "imagem_url": "https://mercantilnovaera.vtexassets.com/arquivos/ids/195393-800-450?v=637793382780370000&width=800&height=450&aspect=true"
        }
    product_data.append(product)
    return product_data


# Função para exibir a lista de produtos na tela   
def list_produtos_screen():
        products = load_json_file()#loaddummydata()#list_products_sql()
        if products:
        # Define o número de cards por linha
            cards_por_linha = 3
            # Cria as colunas iniciais
            cols = st.columns(cards_por_linha)
            for i, product in enumerate(products):
                col = cols[i % cards_por_linha]
                with col:
                    st.markdown(f"### {product['nome']}")
                    st.write(f"**Descrição:** {product['descricao']}")
                    st.write(f"**Preço:** R$ {product['preco']:.2f}")
                    if product["imagem_url"]:
                        st.image(product["imagem_url"],use_container_width=False)
                    st.markdown("---")
                # A cada 'cards_por_linha' produtos, se ainda houver produtos, cria novas colunas
                if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                    cols = st.columns(cards_por_linha)
        else:
            st.info("Nenhum produto encontrado.")

list_produtos_screen()