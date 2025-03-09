# import fitz  # PyMuPDF para extração de texto
# import chromadb
# import os

# # Função para extrair texto do PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with fitz.open(pdf_path) as doc:
#         for page in doc:
#             text += page.get_text("text") + "\n"
#     return text

# # Função para dividir texto em chunks
# def split_text_into_chunks(text, max_chars=1000):
#     sentences = text.split(". ")
#     chunks = []
#     chunk = ""

#     for sentence in sentences:
#         if len(chunk) + len(sentence) > max_chars:
#             chunks.append(chunk)
#             chunk = ""
#         chunk += sentence + ". "
    
#     if chunk:
#         chunks.append(chunk)

#     return chunks

# # Função para indexar no ChromaDB
# def index_pdf(pdf_path, collection_name="regras_veiculacao"):
#     # Verifica se o arquivo PDF existe
#     if not os.path.exists(pdf_path):
#         print(f"O arquivo {pdf_path} não foi encontrado.")
#         return

#     # Extrai o texto do PDF
#     text = extract_text_from_pdf(pdf_path)
    
#     # Verifica se há texto no PDF
#     if not text.strip():
#         print("O PDF não contém texto extraível.")
#         return
    
#     chunks = split_text_into_chunks(text)
#     print(f"Texto extraído e dividido em {len(chunks)} chunks.")

#     # Inicializa o cliente ChromaDB
#     try:
#         chroma_client = chromadb.PersistentClient(path="C:/ai/chroma") #path="./chroma_db"
#         print("Cliente ChromaDB inicializado com sucesso.")
        
#         # Lista as coleções existentes antes de criar uma nova
#         existing_collections = chroma_client.list_collections()
#         print(f"Coleções existentes: {[col.name for col in existing_collections]}")
        
#         # Cria ou obtém a coleção
#         collection = chroma_client.get_or_create_collection(name=collection_name)
#         print(f"Coleção '{collection_name}' obtida ou criada.")
        
#         # Adiciona os chunks à coleção
#         for i, chunk in enumerate(chunks):
#             collection.add(
#                 ids=[f"doc_{i}"],
#                 documents=[chunk],
#                 metadatas=[{"source": pdf_path, "index": i}]
#             )
        
#         # Verifica se os documentos foram adicionados
#         count = collection.count()
#         print(f"A coleção tem {count} documentos.")
        
#         # Lista as coleções novamente para confirmar
#         final_collections = chroma_client.list_collections()
#         print(f"Coleções após indexação: {final_collections}")
        
#     except Exception as e:
#         print(f"Erro ao trabalhar com ChromaDB: {e}")

# if __name__ == "__main__":
#     pdf_path = "202502_lista-precos_fev25.pdf"  # Substitua pelo seu arquivo PDF
    
#     if os.path.exists(pdf_path):
#         print(f"Arquivo encontrado: {pdf_path}")
#         index_pdf(pdf_path)
#     else:
#         print(f"Arquivo não encontrado: {pdf_path}")

import fitz  # PyMuPDF para extração de texto
import chromadb
import os

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

# Função para dividir texto em chunks
def split_text_into_chunks(text, max_chars=1000):
    sentences = text.split(". ")
    chunks = []
    chunk = ""

    for sentence in sentences:
        if len(chunk) + len(sentence) > max_chars:
            chunks.append(chunk)
            chunk = ""
        chunk += sentence + ". "
    
    if chunk:
        chunks.append(chunk)

    return chunks

# Função para indexar no ChromaDB
def index_pdf(pdf_path, collection_name="regras_veiculacao"):
    # Verifica se o arquivo PDF existe
    if not os.path.exists(pdf_path):
        print(f"O arquivo {pdf_path} não foi encontrado.")
        return

    # Extrai o texto do PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Verifica se há texto no PDF
    if not text.strip():
        print("O PDF não contém texto extraível.")
        return
    
    chunks = split_text_into_chunks(text)
    print(f"Texto extraído e dividido em {len(chunks)} chunks.")

    # Inicializa o cliente ChromaDB
    try:
        # Use o cliente HTTP em vez do cliente persistente
        chroma_client = chromadb.HttpClient(host="localhost", port=8000)
        print("Cliente ChromaDB HTTP inicializado com sucesso.")
        
        # Lista as coleções existentes antes de criar uma nova
        existing_collections = chroma_client.list_collections()
        print(f"Coleções existentes: {existing_collections}")
        
        # Cria ou obtém a coleção
        collection = chroma_client.get_or_create_collection(name=collection_name)
        print(f"Coleção '{collection_name}' obtida ou criada.")
        
        # Adiciona os chunks à coleção
        for i, chunk in enumerate(chunks):
            collection.add(
                ids=[f"doc_{i}"],
                documents=[chunk],
                metadatas=[{"source": pdf_path, "index": i}]
            )
        
        # Verifica se os documentos foram adicionados
        count = collection.count()
        print(f"A coleção tem {count} documentos.")
        
        # Lista as coleções novamente para confirmar
        final_collections = chroma_client.list_collections()
        print(f"Coleções após indexação: {final_collections}")
        
    except Exception as e:
        print(f"Erro ao trabalhar com ChromaDB: {e}")

if __name__ == "__main__":
    pdf_path = "202502_lista-precos_fev25.pdf"  # Substitua pelo seu arquivo PDF
    
    if os.path.exists(pdf_path):
        print(f"Arquivo encontrado: {pdf_path}")
        index_pdf(pdf_path)
    else:
        print(f"Arquivo não encontrado: {pdf_path}")