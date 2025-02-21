
#print("Teste")
import os

from langchain_huggingface import ChatHuggingFace
from langchain_community.llms import HuggingFaceHub
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Exemplo com Hugging Face
llm = HuggingFaceHub(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    model_kwargs={
        "temperature": 0.9,
        "return_full_text": False,
        "max_new_tokens": 512,
        #"stop": ["<|eot_id|>"],
        # demais parâmetros que desejar
    }
)

#system_prompt = "Você é um assistente prestativo e está respondendo perguntas gerais."
system_prompt = "Você é um assistente juridico e vai se comportar como um advogado."
user_prompt = "{input}"

token_s, token_e = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>", "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

prompt = ChatPromptTemplate.from_messages([
    ("system", token_s + system_prompt),
    ("user", user_prompt + token_e)
])

chain = prompt | llm
os.system('cls')
PERGUNTA = input("Prompt: ")

#input = "Quais as caracteristicas das mulheres do signo de áries?"

res = chain.invoke({"input": PERGUNTA})
os.system('cls')
print('PERGUNTA PARA INTELIGÊNCIA ARTIFICIAL:', input)
print("----- RESPOSTA DA INTELIGÊNCIA ARTIFICIAL-----")
print(res)
print("----------------------------------------------")