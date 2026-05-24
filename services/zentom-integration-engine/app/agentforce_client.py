def execute_agentforce_action(action: dict) -> dict:
    return {
        "status": "approval_required",
        "action": action,
    }

