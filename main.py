import streamlit as st



# Configurando as páginas
main_page = st.Page("main_page.py", title="Página Principal", icon="🎉")
page_2 = st.Page("page_2.py", title="Cadastrar Novo Produto", icon="➕")

# Configurando a navegação
pg = st.navigation([main_page, page_2])

# Executar a página selecionada
pg.run()