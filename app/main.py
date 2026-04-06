from fastapi import FastAPI

app = FastAPI(
    title="TFG RAG CEU",
    description="API del asistente conversacional basado en RAG",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}