import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

# conectar a la misma DB
client = chromadb.PersistentClient(path=settings.chroma_db_path)

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="ceu_knowledge",
    embedding_function=embedding_function
)

# consulta de prueba
query = "¿Dónde está el campus?"

results = collection.query(
    query_texts=[query],
    n_results=2
)

print("\nRESULTADOS:")
for i, doc in enumerate(results["documents"][0]):
    print(f"\nChunk {i+1}:")
    print(doc)