import json

import requests

from app.config import settings


class LLMClientError(Exception):
    pass


def is_llm_enabled() -> bool:
    if settings.AI_MODE not in ["LLM", "HYBRID"]:
        return False

    if settings.AI_PROVIDER == "LOCAL":
        return True

    if settings.AI_PROVIDER == "OPENAI":
        return bool(settings.AI_API_KEY)

    return False


def generate_llm_recommendation(prompt: str) -> dict:
    """
    LLM only recommends.
    LLM never executes.
    Policy Engine and Human Approval control execution.
    """

    if not is_llm_enabled():
        raise LLMClientError("LLM is not enabled or provider is not configured.")

    if settings.AI_PROVIDER == "LOCAL":
        return generate_local_recommendation(prompt)

    if settings.AI_PROVIDER == "OPENAI":
        raise LLMClientError("OpenAI provider disabled for cost-safe MVP.")

    raise LLMClientError(f"Unsupported AI provider: {settings.AI_PROVIDER}")


def generate_local_recommendation(prompt: str) -> dict:
    url = f"{settings.LOCAL_LLM_URL}/api/generate"

    safe_prompt = f"""
You are Zentom AI. You recommend safe Salesforce incident resolutions.

Rules:
- Return only valid JSON. Do not include Markdown, prose, or code fences.
- Only produce summary, rootCause, recommendedAction, confidenceScore, aiExplanation, and runbookReason.
- Do not output or alter policyDecision, riskScore, riskLevel, runbookKey, or execution instructions.
- If policy requires human approval, the recommendedAction must preserve human review.

{prompt}

## Required JSON Shape

{{
  "summary": "short business-friendly summary",
  "rootCause": "likely root cause, leveraging past memory if applicable",
  "recommendedAction": "detailed, safe recommendation based on past resolutions",
  "confidenceScore": 85,
  "aiExplanation": "safe logical explanation of why this incident occurred",
  "runbookReason": "explanation of why the provided runbook is relevant"
}}

All values except confidenceScore must be plain strings. Do not use nested objects or arrays.
""".strip()

    payload = {
        "model": settings.LOCAL_LLM_MODEL,
        "prompt": safe_prompt,
        "stream": False,
        "format": "json",
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        raw_text = data.get("response", "{}")
        parsed = json.loads(raw_text)

        return {
            "summary": safe_text(parsed.get("summary"), "Local LLM generated summary unavailable."),
            "rootCause": safe_text(parsed.get("rootCause"), "Local LLM root cause unavailable."),
            "recommendedAction": safe_text(parsed.get("recommendedAction"), "Review incident manually."),
            "confidenceScore": safe_confidence(parsed.get("confidenceScore")),
            "aiExplanation": safe_text(parsed.get("aiExplanation"), "AI explanation unavailable."),
            "runbookReason": safe_text(parsed.get("runbookReason"), "AI runbook reason unavailable."),
            "modelName": settings.LOCAL_LLM_MODEL,
            "rawModelOutput": {
                "provider": "LOCAL",
                "model": settings.LOCAL_LLM_MODEL,
                "raw": compact_ollama_response(data),
            },
        }

    except Exception as exc:
        raise LLMClientError(f"Local LLM call failed: {str(exc)}") from exc


def safe_text(value, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()

    if isinstance(value, dict):
        parts = [
            part.strip()
            for part in value.values()
            if isinstance(part, str) and part.strip()
        ]
        if parts:
            return " ".join(parts)

    if isinstance(value, list):
        parts = [
            part.strip()
            for part in value
            if isinstance(part, str) and part.strip()
        ]
        if parts:
            return " ".join(parts)

    return fallback


def safe_confidence(value) -> int:
    try:
        confidence = int(value)
    except (TypeError, ValueError):
        return 75
    return max(0, min(100, confidence))


def compact_ollama_response(data: dict) -> dict:
    return {
        "model": data.get("model"),
        "created_at": data.get("created_at"),
        "response": data.get("response"),
        "done": data.get("done"),
        "done_reason": data.get("done_reason"),
        "total_duration": data.get("total_duration"),
        "load_duration": data.get("load_duration"),
        "prompt_eval_count": data.get("prompt_eval_count"),
        "eval_count": data.get("eval_count"),
    }
