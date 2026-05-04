from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_identifier: str
    channel: str = "web"
    message: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str