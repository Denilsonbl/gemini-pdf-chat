import streamlit as st

# Configuração da página
st.set_page_config(page_title="Página com Sidebar", layout="wide")

# Título da página
st.title("Minha Página com Streamlit")

# Criação do sidebar
with st.sidebar:
    # Adiciona um container para centralizar o botão
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: red;
            color: white;
            display: block;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Botão centralizado
    if st.button("Clique Aqui"):
        st.write("Você clicou no botão!")

# Conteúdo principal da página
st.write("Este é o conteúdo principal da página.")