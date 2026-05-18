import requests
from app.core.config import settings


def send_whatsapp_message(to: str, message: str) -> None:
    if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
        print("WhatsApp no configurado. Respuesta generada:", message)
        return

    url = (
        f"https://graph.facebook.com/"
        f"{settings.whatsapp_api_version}/"
        f"{settings.whatsapp_phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=15)
    response.raise_for_status()