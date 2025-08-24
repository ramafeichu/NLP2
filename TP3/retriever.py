import os
from typing import List
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

embedding_model_name = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
embedding_model = SentenceTransformer(embedding_model_name)

pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME", "cv-index")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)


def retrieve_context(target: str, query: str, k: int = 3) -> List[str]:
    if not target:
        return []

    print(f"Buscando en índice '{index_name}', namespace: '{target}', query: '{query}'")

    # Generar embedding del query
    vector = embedding_model.encode(query).astype("float32").tolist()

    # Realizar consulta en Pinecone
    res = index.query(
        vector=vector,
        top_k=k,
        include_metadata=True,
        namespace=target,
    )

    matches = res.get("matches", [])
    print(f"Resultados obtenidos: {len(matches)}")

    # Devolver texto de metadata si está presente
    return [match["metadata"].get("text", "") for match in matches]
