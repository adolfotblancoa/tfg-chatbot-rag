import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

COLLECTION_NAME = "ceu_knowledge"

client = chromadb.PersistentClient(path=settings.chroma_db_path)

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


def retrieve_context(query: str, n_results: int = 3) -> list[str]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    return documents


def retrieve_context_with_metadata(query: str, n_results: int = 3) -> dict:
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )