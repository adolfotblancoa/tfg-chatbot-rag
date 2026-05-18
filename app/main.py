from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.core.config import settings
from app.db.sqlite import init_db
from app.api.whatsapp import router as whatsapp_router

app = FastAPI(
    title=settings.app_name,
    description="API del asistente conversacional basado en RAG",
    version="0.4.0"
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(router)
app.include_router(whatsapp_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")