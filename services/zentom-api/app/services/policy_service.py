def evaluate_policy(payload: dict, risk: dict) -> dict:
    confidence = payload.get("confidence", 0)
    environment = payload.get("environment", "sandbox")
    action_type = payload.get("actionType", "CREATE_CASE")

    if environment == "production":
        return {
            "decision": "HUMAN_APPROVAL_REQUIRED",
            "requiresApproval": True,
            "reason": "Production environment requires human approval",
        }

    if risk["totalScore"] >= 80:
        return {
            "decision": "BLOCK_AUTONOMOUS_ACTION",
            "requiresApproval": True,
            "reason": "Risk score is critical",
        }

    if confidence < 80:
        return {
            "decision": "HUMAN_APPROVAL_REQUIRED",
            "requiresApproval": True,
            "reason": "Confidence below 80%",
        }

    if action_type in ["CREATE_CASE", "SEND_NOTIFICATION", "CREATE_TASK"]:
        return {
            "decision": "APPROVED",
            "requiresApproval": False,
            "reason": "Low-risk allowed action",
        }

    return {
        "decision": "HUMAN_APPROVAL_REQUIRED",
        "requiresApproval": True,
        "reason": "Action type requires review",
    }
