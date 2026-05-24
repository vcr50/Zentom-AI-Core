def recommend_action(incident: dict) -> dict:
    return {
        "summary": "Review the incident context and confirm business impact.",
        "recommended_action": "Create investigation task for an approver.",
        "confidence_score": 50,
    }

