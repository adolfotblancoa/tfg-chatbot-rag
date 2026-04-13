from app.rag.retriever import retrieve_context_with_metadata

query = "¿Donde esta el campus?"

results = retrieve_context_with_metadata(query, n_results=3)

print("\nRESULTADOS:\n")

documents = results["documents"][0]
metadatas = results["metadatas"][0]

for i, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
    print(f"Resultado {i}")
    print(f"Fuente: {meta.get('source')}")
    print(f"Chunk: {meta.get('chunk_index')}")
    print(doc)
    print("-" * 60)