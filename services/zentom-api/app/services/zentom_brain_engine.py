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

    return {
        "risk": risk,
        "policy": policy,
        "recommendation": recommendation,
        "runbook": {
            "runbookKey": recommendation.get("runbookKey"),
            "recommendationStatus": recommendation.get("recommendationStatus"),
        },
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
