import time
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import google.generativeai as genai
from dotenv import load_dotenv
import os

st.markdown("<h3 style='color: black;'>Oi, eu sou o OceanBlue</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: black;'>Como posso ajudar você hoje?</p>", unsafe_allow_html=True)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Streamlit
#st.set_page_config(page_title="Seu assistente virtual 🤖", page_icon="🤖")
#st.title("Seu assistente virtual 🤖")

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

# Botão para iniciar um novo chat
if st.button("Novo Chat"):
    st.session_state.chat_history = []
    st.session_state.chat_history = [
        AIMessage(content="Olá, sou o seu assistente virtual! Como posso ajudar você?"),
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