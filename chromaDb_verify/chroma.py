import chromadb

def list_collections():
    # Use o cliente HTTP
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    collections = chroma_client.list_collections()
    
    if collections:
        print(f"Foram encontradas {len(collections)} coleções:")
        for col_name in collections:
            # Obtém a coleção para acessar a contagem
            collection = chroma_client.get_collection(col_name)
            print(f"- Nome: {col_name}, Número de documentos: {collection.count()}")
    else:
        print("Nenhuma coleção encontrada no ChromaDB.")

if __name__ == "__main__":
    list_collections()