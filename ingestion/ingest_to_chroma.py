import chromadb
from chromadb.utils import embedding_functions

from app.core.config import settings
from ingestion.load_documents import load_documents
from ingestion.chunking import chunk_text

COLLECTION_NAME = "ceu_knowledge"

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small"
)

client = chromadb.PersistentClient(path=settings.chroma_db_path)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


def infer_faculty(source: str) -> str:
    source_lower = source.lower()

    if "farmacia" in source_lower:
        return "farmacia"
    if "medicina" in source_lower:
        return "medicina"
    if "derecho" in source_lower:
        return "derecho"
    if "eps" in source_lower or "politecnica" in source_lower:
        return "eps"
    if "hum" in source_lower or "com" in source_lower:
        return "humanidades_comunicacion"

    return "general"


def ingest(reset_collection: bool = False):
    global collection

    if reset_collection:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_function
        )

    documents = load_documents("data/raw")

    all_chunks = []
    ids = []
    metadatas = []

    for doc in documents:
        chunks = chunk_text(doc["content"], chunk_size=1200, overlap=200)

        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            ids.append(f"{doc['source']}_p{doc['page']}_{i}")
            metadatas.append({
                "source": doc["source"],
                "doc_type": doc["type"],
                "page": doc["page"],
                "chunk_index": i,
                "faculty": infer_faculty(doc["source"])
            })

    if all_chunks:
        collection.add(
            documents=all_chunks,
            ids=ids,
            metadatas=metadatas
        )

    print(f"Ingestados {len(all_chunks)} chunks de {len(documents)} unidades documentales")


if __name__ == "__main__":
    ingest(reset_collection=True)