def classify_incident(payload: dict) -> dict:
    return {
        "incident_type": payload.get("incident_type", "unknown"),
        "confidence_score": 50,
    }

