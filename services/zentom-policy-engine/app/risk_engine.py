def score_risk(incident: dict) -> dict:
    severity = incident.get("severity", "medium")
    base_score = {"low": 25, "medium": 50, "high": 75, "critical": 90}.get(severity, 50)

    return {
        "total_score": base_score,
        "risk_level": "high" if base_score >= 75 else "medium" if base_score >= 50 else "low",
    }

