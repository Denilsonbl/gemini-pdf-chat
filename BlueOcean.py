import time
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Texto personalizado com HTML e CSS
st.sidebar.markdown(
    """
    <style>
    .custom-text {
        all: unset;
        font-size: 24px;  /* Tamanho da fonte */
        font-family: 'Arial', sans-serif;  /* Tipo da fonte */
        color: #1E90FF;  /* Cor da fonte (azul OceanBlue) */
        font-weight: bold;  /* Negrito */
        font-style: italic;  /* Itálico */
        margin: 0;
        display: flex;  /* Usa Flexbox para centralizar */
        justify-content: center;  /* Centraliza horizontalmente */
        align-items: center;  /* Centraliza verticalmente */
    }
    </style>
    <div class="custom-text">BlueOcean</div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    # Adiciona o CSS personalizado
    st.markdown(
        """
        <style>
        /* Estilo padrão do botão */
        .stButton>button {
            background-color: #0092d4;  /* Cor de fundo */
            color: white !important;;               /* Cor do texto */
            display: block;             /* Centraliza o botão */
            margin: 0 auto;             /* Centraliza o botão */
            border: none;               /* Remove a borda padrão */
            border-radius: 5px;         /* Borda arredondada */
            padding: 10px 20px;         /* Espaçamento interno */
            font-size: 16px;            /* Tamanho da fonte */
            cursor: pointer;            /* Mostra o cursor de clique */
            transition: none;           /* Remove transições */
        }

        /* Mantém o mesmo estilo ao passar o mouse */
        .stButton>button:hover {
            background-color: #0092d4;  /* Mesma cor de fundo */
            color: white !important;;               /* Mesma cor do texto */
            cursor: pointer;            /* Mantém o cursor de clique */
        }

        /* Mantém o mesmo estilo ao clicar */
        .stButton>button:active {
            background-color: #0092d4;  /* Mesma cor de fundo */
            color: white !important;               /* Mesma cor do texto */
            cursor: pointer;            /* Mantém o cursor de clique */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Botão centralizado
    if st.button("Novo chat"):
        st.session_state.chat_history = []
       
# URL do ícone
icon_url = "https://s3u.tmimgcdn.com/u37752224/e5f815644715f8716617578c621cda39.gif"

st.markdown(
    """
    <style>
    .custom-text {
        font-size: 24px;  /* Tamanho da fonte */
        font-family: 'Century', sans-serif;  /* Tipo da fonte */
        color: black;  /* Cor da fonte (azul OceanBlue) */
        font-weight: bold;  /* Negrito */
        font-style: italic;  /* Itálico */
        text-align: center;
    }
    .custom-image {
        width: 15%;  /* Reduz o tamanho da imagem para 50% */
        height: auto;  /* Mantém a proporção da imagem */
    }
    .custom-help {
        text-align: center;
    }
    </style>

    <div class="custom-text">
        <img class="custom-image" src="https://s3u.tmimgcdn.com/u37752224/e5f815644715f8716617578c621cda39.gif"/>
        Oi, eu sou o BlueOcean
    </div> 
    <div class="custom-help">
        Como posso te ajudar hoje?
    </div> 
    
    """,
    unsafe_allow_html=True
)

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Adicione sua chave da API no .env

# Função para gerar respostas usando o Gemini
def model_response(user_query, chat_history):
    # Configuração do modelo Gemini
    model = genai.GenerativeModel('gemini-pro')

    # Formata o histórico de chat para o Gemini
    messages = []
    for message in chat_history:
        if isinstance(message, HumanMessage):
            messages.append({"role": "user", "parts": [message.content]})
        elif isinstance(message, AIMessage):
            messages.append({"role": "model", "parts": [message.content]})

    # Adiciona a nova mensagem do usuário
    messages.append({"role": "user", "parts": [user_query]})

    # Gera a resposta usando o Gemini
    response = model.generate_content(messages)
    return response.text

# Inicialização do histórico de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        #AIMessage(content="Olá, sou o seu assistente virtual! Como posso ajudar você?"),
    ]

# Exibição do histórico de chat
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# Entrada do usuário
user_query = st.chat_input("Digite sua mensagem aqui...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    # Cria um espaço reservado para o GIF
    gif_placeholder = st.empty()

    # Exibe o GIF enquanto processa a resposta
    with gif_placeholder:
        st.image("https://i.giphy.com/ckebyFUgKNQMYP7Q8S.webp", width=50)  # Exibe o GIF

    # Processa a resposta da IA
    resp = model_response(user_query, st.session_state.chat_history)

    gif_placeholder.empty()  # Limpa o espaço reservado (remove o GIF)
    with st.chat_message("AI"):
        st.write(resp)  # Exibe a resposta da IA

    st.session_state.chat_history.append(AIMessage(content=resp))