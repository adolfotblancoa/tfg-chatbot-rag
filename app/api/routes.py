from fastapi import APIRouter
from app.db.models import ChatRequest, ChatResponse
from app.services.chat_service import generate_dummy_response, save_chat_interaction

router = APIRouter()


@router.get("/")
def root():
    return {"message": "API funcionando 🚀"}


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_dummy_response(request.message)
    save_chat_interaction(request.message, reply)
    return ChatResponse(reply=reply)