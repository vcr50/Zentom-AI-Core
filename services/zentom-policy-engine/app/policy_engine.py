def decide_policy(risk_score: dict) -> dict:
    total_score = risk_score.get("total_score", 0)

    return {
        "decision": "approval_required" if total_score >= 75 else "allowed",
        "requires_approval": total_score >= 75,
        "reason": "High-risk incident requires approval." if total_score >= 75 else "Risk is within allowed threshold.",
    }

