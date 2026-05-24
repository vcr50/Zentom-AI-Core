def send_webhook(url: str, payload: dict) -> dict:
    return {
        "status": "not_sent",
        "url": url,
        "payload": payload,
    }

