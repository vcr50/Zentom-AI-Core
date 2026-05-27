import logging

from app.config import settings
from app.services.ai_recommendation_service import generate_recommendation
from app.services.memory_service import (
    build_memory_context,
    search_memory_entries,
    search_similar_memories,
)
from app.services.policy_service import evaluate_policy
from app.services.risk_service import calculate_risk


BRAIN_VERSION = "zentom-brain-v1"
SAFETY_MODE = "POLICY_CONTROLLED"

logger = logging.getLogger(__name__)


def analyze_incident(payload: dict, db=None) -> dict:
    risk = calculate_risk(payload)
    policy = evaluate_policy(payload, risk)

    # --- Memory injection ---
    memory_context = "No memory context available."
    memory_metadata = {
        "enabled": False,
        "matchCount": 0,
        "contextInjected": False,
    }

    if db is not None:
        try:
            error_message = payload.get("errorMessage", "")
            search_method = "none"

            # Try vector similarity search first
            if error_message:
                similar_result = search_similar_memories(
                    db=db,
                    query_text=error_message,
                    limit=3,
                )
                memories = similar_result["memories"]
                search_method = similar_result["searchMethod"]

            # Fall back to keyword/filter search
            if not memories:
                memories = search_memory_entries(
                    db=db,
                    incident_type=payload.get("incidentType"),
                    query_text=error_message or None,
                    limit=3,
                )
                if memories:
                    search_method = "keyword"

            memory_context = build_memory_context(memories)

            memory_metadata = {
                "enabled": True,
                "matchCount": len(memories),
                "contextInjected": len(memories) > 0,
                "searchMethod": search_method,
            }
        except Exception as exc:
            logger.warning("Memory search failed: %s", exc)
            memory_context = (
                "Memory search unavailable. "
                "Continue with current incident only."
            )
            memory_metadata = {
                "enabled": False,
                "matchCount": 0,
                "contextInjected": False,
                "searchMethod": "none",
                "reason": str(exc),
            }

    recommendation = generate_recommendation(
        payload=payload,
        risk=risk,
        policy=policy,
        memory_context=memory_context,
    )

    ai_reasoning_status = "ACTIVE"
    if recommendation.get("modelName") == "zentom-rule-v1":
        ai_reasoning_status = "RULE_ONLY"
    elif "fallback" in recommendation.get("modelName", ""):
        ai_reasoning_status = "FALLBACK"

    orchestration_mode = settings.AI_MODE or "RULE"

    env = payload.get("environment", "sandbox")
    inc_type = payload.get("incidentType", "issue").replace("_", " ").lower()
    risk_level_fmt = risk.get("riskLevel", "UNKNOWN").lower().capitalize()
    risk_reason = f"{risk_level_fmt} risk because the incident indicates a {env} {inc_type} with business process impact."

    ai_trace = {
        "aiReasoningStatus": ai_reasoning_status,
        "aiConfidenceScore": recommendation.get("confidenceScore", 0),
        "aiExplanation": recommendation.get("aiExplanation", "AI explanation not available."),
        "riskReason": risk_reason,
        "policyReason": policy.get("reason", "Policy reason not available."),
        "runbookReason": recommendation.get("runbookReason", "Runbook reason not available."),
        "memoryUsed": memory_metadata.get("contextInjected", False),
        "orchestrationMode": orchestration_mode,
        "brainVersion": BRAIN_VERSION,
    }

    return {
        "risk": risk,
        "policy": policy,
        "recommendation": recommendation,
        "runbook": {
            "runbookKey": recommendation.get("runbookKey"),
            "recommendationStatus": recommendation.get("recommendationStatus"),
        },
        "aiTrace": ai_trace,
        "brain": get_brain_metadata(),
        "memory": memory_metadata,
    }


def get_brain_metadata() -> dict:
    return {
        "brainVersion": BRAIN_VERSION,
        "aiMode": settings.AI_MODE,
        "aiProvider": settings.AI_PROVIDER,
        "localModel": settings.LOCAL_LLM_MODEL,
        "safetyMode": SAFETY_MODE,
    }
