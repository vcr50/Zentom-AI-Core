from app.config import settings
from app.services.llm_client import generate_llm_recommendation


def generate_rule_recommendation(payload: dict, risk: dict, policy: dict) -> dict:
    incident_type = payload.get("incidentType")
    error_message = payload.get("errorMessage", "")
    environment = payload.get("environment", "sandbox")

    if incident_type == "FLOW_FAILURE":
        if "missing account owner" in error_message.lower():
            return {
                "summary": "Salesforce Flow failed because Account Owner was missing.",
                "rootCause": "Required owner lookup was null during Flow execution.",
                "recommendedAction": "Create an admin case and review Flow input validation.",
                "confidenceScore": 87,
                "runbookKey": "FLOW_FAILURE_BASIC_RECOVERY",
                "recommendationStatus": "Generated",
                "modelName": "zentom-rule-v1",
            }

        return {
            "summary": f"A Salesforce Flow failure was detected in the {environment} environment.",
            "rootCause": f"The likely cause is related to this error: {error_message}",
            "recommendedAction": (
                "Create an admin case, review the failed Flow interview, validate required "
                "fields, and check recent Flow changes."
            ),
            "confidenceScore": 87,
            "runbookKey": "FLOW_FAILURE_BASIC_RECOVERY",
            "recommendationStatus": "Generated",
            "modelName": "zentom-rule-v1",
        }

    return {
        "summary": "An incident was detected and requires admin review.",
        "rootCause": "Root cause could not be confidently determined from the current payload.",
        "recommendedAction": "Create a Salesforce admin case for manual investigation.",
        "confidenceScore": 70,
        "runbookKey": "GENERAL_INCIDENT_REVIEW",
        "recommendationStatus": "Needs Review",
        "modelName": "zentom-rule-v1",
    }


def build_llm_prompt(
    payload: dict,
    risk: dict,
    policy: dict,
    rule_recommendation: dict,
    memory_context: str | None = None,
) -> str:
    memory_block = (
        "## Past Resolutions\n\n"
        "No relevant past memory was retrieved for this incident.\n"
    )
    if memory_context and "No similar memory entries found" not in memory_context:
        memory_block = (
            "## Past Resolutions\n\n"
            "Use these retrieved memories as context for summary, root cause, and recommended action. "
            "Prefer patterns that match the current incident, but do not copy blindly.\n\n"
            f"{memory_context}\n"
        )

    return f"""
You are Zentom AI, an incident recommendation assistant for Salesforce operations.

## Current Incident

- Incident Type: {payload.get('incidentType')}
- Source: {payload.get('source')}
- Environment: {payload.get('environment')}
- Error Message: {payload.get('errorMessage')}
- Requested Action: {payload.get('actionType')}
- Confidence: {payload.get('confidence')}

## Locked Safety Context

These fields are authoritative and must not be changed or contradicted.

- Risk Score: {risk.get('totalScore')}
- Risk Level: {risk.get('riskLevel')}
- Policy Decision: {policy.get('decision')}
- Requires Approval: {policy.get('requiresApproval')}
- Policy Reason: {policy.get('reason')}
- Runbook Key: {rule_recommendation.get('runbookKey')}
- Safe Baseline Action: {rule_recommendation.get('recommendedAction')}

{memory_block}

## Task

Generate a concise recommendation for the current incident.

- Use past resolutions to improve the root cause and recommended action when they are relevant.
- Keep the recommendation aligned with the locked policy, risk, and runbook context.
- Do not recommend autonomous execution when policy requires human approval.
- Do not change the runbook key, policy decision, risk score, or risk level.
- Return only the recommendation fields requested by the API wrapper.
""".strip()


def generate_recommendation(
    payload: dict,
    risk: dict,
    policy: dict,
    memory_context: str | None = None,
) -> dict:
    rule_result = generate_rule_recommendation(payload, risk, policy)
    mode = (settings.ai_mode or "RULE").upper()

    if mode == "RULE":
        return rule_result

    prompt = build_llm_prompt(payload, risk, policy, rule_result, memory_context)

    if mode == "LLM":
        try:
            llm_result = generate_llm_recommendation(prompt)
            return merge_llm_with_rule_safety(rule_result, llm_result)
        except Exception as exc:
            return with_fallback_model(rule_result, exc)

    if mode == "HYBRID":
        try:
            llm_result = generate_llm_recommendation(prompt)
            return merge_llm_with_rule_safety(rule_result, llm_result)
        except Exception as exc:
            return with_fallback_model(rule_result, exc)

    return rule_result


def merge_llm_with_rule_safety(rule_result: dict, llm_result: dict) -> dict:
    merged = dict(rule_result)
    for key in ["summary", "rootCause", "recommendedAction"]:
        if isinstance(llm_result.get(key), str) and llm_result[key].strip():
            merged[key] = llm_result[key]

    if isinstance(llm_result.get("confidenceScore"), int):
        merged["confidenceScore"] = llm_result["confidenceScore"]

    merged["modelName"] = llm_result.get("modelName") or settings.ai_model
    merged["rawModelOutput"] = {
        "mode": (settings.ai_mode or "RULE").upper(),
        "provider": settings.ai_provider,
        "llm": llm_result,
        "ruleSafety": {
            "runbookKey": rule_result["runbookKey"],
            "recommendationStatus": rule_result["recommendationStatus"],
        },
    }
    return merged


def with_fallback_model(rule_result: dict, error: Exception) -> dict:
    fallback = dict(rule_result)
    fallback["modelName"] = "zentom-rule-v1-fallback"
    fallback["rawModelOutput"] = {
        "mode": (settings.ai_mode or "RULE").upper(),
        "provider": settings.ai_provider,
        "fallback": True,
        "fallbackReason": str(error),
        "rule": rule_result,
    }
    return fallback
