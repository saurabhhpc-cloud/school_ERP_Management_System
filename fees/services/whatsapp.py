import os
import requests

WHATSAPP_PROVIDER = os.getenv("WHATSAPP_PROVIDER", "mock")
API_URL = os.getenv("WHATSAPP_API_URL", "")
API_KEY = os.getenv("WHATSAPP_API_KEY", "")

def send_whatsapp(phone, message):
    """
    Provider-agnostic sender.
    Replace MOCK with your real provider later.
    """
    if WHATSAPP_PROVIDER == "mock":
        print(f"[MOCK WHATSAPP] To: {phone} | Msg: {message}")
        return True

    # Example generic POST (adapt to provider)
    payload = {
        "to": phone,
        "message": message,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    r = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    return r.status_code in (200, 201)
