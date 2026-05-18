from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse

from app.core.config import settings
from app.db.sessions import get_or_create_session
from app.services.chat_service import process_chat_message
from app.services.whatsapp_service import send_whatsapp_message

router = APIRouter(prefix="/webhook/whatsapp", tags=["WhatsApp"])


@router.get("")
def verify_webhook(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.whatsapp_verify_token:
        return PlainTextResponse(challenge or "")

    raise HTTPException(status_code=403, detail="Invalid verification token")


@router.post("")
async def receive_message(request: Request):
    payload = await request.json()

    try:
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "ignored"}

        message = messages[0]
        from_number = message.get("from")
        text = message.get("text", {}).get("body", "")

        if not from_number or not text:
            return {"status": "ignored"}

        session_id = get_or_create_session(
            user_identifier=from_number,
            channel="whatsapp"
        )

        reply = process_chat_message(
            session_id=session_id,
            message=text
        )

        send_whatsapp_message(
            to=from_number,
            message=reply
        )

        return {"status": "ok"}

    except Exception as e:
        print("Error procesando webhook de WhatsApp:", e)
        return {"status": "error"}