import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

client = chromadb.PersistentClient(path=settings.chroma_db_path)

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="ceu_knowledge",
    embedding_function=embedding_function
)


def retrieve_context(query: str, n_results: int = 2) -> list[str]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    return documents