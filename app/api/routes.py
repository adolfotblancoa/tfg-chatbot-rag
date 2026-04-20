from fastapi import APIRouter
from app.db.models import ChatRequest, ChatResponse
from app.services.chat_service import process_chat_message

router = APIRouter()


@router.get("/")
def root():
    return {"message": "API funcionando 🚀"}


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = process_chat_message(
        session_id=request.session_id,
        message=request.message
    )
    return ChatResponse(reply=reply)