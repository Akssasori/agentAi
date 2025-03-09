from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import openai
import os
from dotenv import load_dotenv
import openai

# Carregar API Key do OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Client openAI
client = openai.Client()

# Inicializar ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="regras_veiculacao")

# Inicializar FastAPI
app = FastAPI()

class QueryRequest(BaseModel):
    question: str

# Função para buscar no ChromaDB e gerar resposta
def retrieve_and_respond(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    retrieved_texts = [doc for doc in results["documents"][0]]

    if not retrieved_texts:
        return "Desculpe, não encontrei informações relevantes no documento."

    context = "\n".join(retrieved_texts)
    prompt = f"""
    Baseado nas regras de veiculação comercial abaixo, responda à pergunta com precisão:
    {context}

    Pergunta: {query}
    Resposta:
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente especializado em veiculação comercial."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# Endpoint da API
@app.post("/perguntar")
def perguntar(req: QueryRequest):
    answer = retrieve_and_respond(req.question)
    return {"resposta": answer}

# Rodar a API (comando no terminal)
# uvicorn chatbot:app --reload
