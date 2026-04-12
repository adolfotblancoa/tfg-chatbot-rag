import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings
from ingestion.load_documents import load_txt_files
from ingestion.chunking import chunk_text

CHROMA_PATH = "./chroma_db"

# usamos embeddings de OpenAI
embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small"
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="ceu_knowledge",
    embedding_function=embedding_function
)


def ingest():
    documents = load_txt_files("data/raw")

    all_chunks = []
    ids = []
    metadatas = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            ids.append(f"{doc['source']}_{i}")
            metadatas.append({"source": doc["source"]})

    collection.add(
        documents=all_chunks,
        ids=ids,
        metadatas=metadatas
    )

    print(f"Ingestados {len(all_chunks)} chunks")


if __name__ == "__main__":
    ingest()