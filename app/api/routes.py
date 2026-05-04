from fastapi import APIRouter
from app.db.models import ChatRequest, ChatResponse
from app.db.sessions import get_or_create_session
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
    session_id = get_or_create_session(
        user_identifier=request.user_identifier,
        channel=request.channel
    )

    reply = process_chat_message(
        session_id=session_id,
        message=request.message
    )

    return ChatResponse(
        reply=reply,
        session_id=session_id
    )