# import chromadb

from chromadb import PersistentClient
from app.embedder import embed_text

client = PersistentClient(path=".chroma_store")

collection = client.get_or_create_collection(name="code_chunks")


def add_to_vector_store(chunks: list, metadata_list: list):
    ids = [f"{meta['path']}_chunk_{meta['chunk_index']}" for meta in metadata_list]
    collection.add(documents=chunks, metadatas=metadata_list, ids=ids)

def search_similar_chunks(question: str, top_k: int = 5) -> list:
    embedded_question = embed_text(question)
    results = collection.query(query_embeddings=[embedded_question], n_results=top_k)

    documents = results['documents'][0]
    metadatas = results['metadatas'][0]

    return list(zip(documents, metadatas))
