### Criando ChromaDB com Docker

```sh
docker run -p 8000:8000 -v C:\ai\chroma:/chroma/chroma chromadb/chroma



### creating chromaDb with docker

docker run -p 8000:8000 -v C:\ai\chroma:/chroma/chroma chromadb/chroma

### instalação

pip install chromadb openai pypdf fastapi uvicorn pymupdf python-dotenv

### Como Usar
Indexe o PDF (execute apenas uma vez para armazenar no ChromaDB):
python process_pdf.py

Inicie o chatbot como API:
uvicorn chatbot:app --reload

Faça perguntas ao chatbot via API usando o curl ou Postman:
curl -X POST "http://127.0.0.1:8000/perguntar" -H "Content-Type: application/json" -d '{"question": "Quais são as taxas para um anúncio de 30 segundos?"}'
Ou use o Postman e envie um POST para http://127.0.0.1:8000/perguntar com o JSON:

json

{
  "question": "Quais são as taxas para um anúncio de 30 segundos?"
}