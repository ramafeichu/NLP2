import os
from typing import List
from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings
import pinecone

# Mapa target → índice
INDEX_MAP = {
    "ana": "ana-index",
    "juan": "juan-index"
}

# Setup embeddings (usando modelo del .env)
embedding_model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

# Inicializar Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_REGION"))

def retrieve_context(target: str, query: str, k: int = 3) -> List[str]:
    index_name = INDEX_MAP.get(target)
    if not index_name:
        return []

    vectorstore = Pinecone.from_existing_index(index_name, embeddings)
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
