"""
Zentom AI Engine — Intent Classifier

Classifies incoming incidents by type, severity, and urgency.
Supports both rule-based and LLM-augmented classification.
"""

from enum import Enum
from typing import Optional


class IncidentCategory(str, Enum):
    INTEGRATION_ERROR = "integration_error"
    PAYMENT_FAILURE = "payment_failure"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_BREACH = "security_breach"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    CONFIGURATION_CHANGE = "configuration_change"
    APEX_EXCEPTION = "apex_exception"
    FLOW_FAILURE = "flow_failure"
    API_LIMIT_EXCEEDED = "api_limit_exceeded"
    USER_REPORTED = "user_reported"
    UNKNOWN = "unknown"


class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Keyword-based classification rules
CLASSIFICATION_RULES: list[dict] = [
    {
        "keywords": ["stripe", "razorpay", "payment", "billing", "charge", "invoice", "subscription"],
        "category": IncidentCategory.PAYMENT_FAILURE,
        "base_confidence": 85,
    },
    {
        "keywords": ["integration", "sync", "connector", "webhook", "callback", "endpoint"],
        "category": IncidentCategory.INTEGRATION_ERROR,
        "base_confidence": 80,
    },
    {
        "keywords": ["corrupt", "data loss", "missing record", "duplicate", "orphan"],
        "category": IncidentCategory.DATA_CORRUPTION,
        "base_confidence": 82,
    },
    {
        "keywords": ["security", "unauthorized", "breach", "access", "permission", "login"],
        "category": IncidentCategory.SECURITY_BREACH,
        "base_confidence": 88,
    },
    {
        "keywords": ["slow", "timeout", "latency", "performance", "cpu", "memory", "heap"],
        "category": IncidentCategory.PERFORMANCE_DEGRADATION,
        "base_confidence": 75,
    },
    {
        "keywords": ["config", "setting", "metadata", "deploy", "change set", "custom"],
        "category": IncidentCategory.CONFIGURATION_CHANGE,
        "base_confidence": 70,
    },
    {
        "keywords": ["apex", "exception", "trigger", "class", "gack", "null pointer"],
        "category": IncidentCategory.APEX_EXCEPTION,
        "base_confidence": 83,
    },
    {
        "keywords": ["flow", "workflow", "automation", "process builder"],
        "category": IncidentCategory.FLOW_FAILURE,
        "base_confidence": 78,
    },
    {
        "keywords": ["limit", "api limit", "governor", "quota", "rate limit", "too many"],
        "category": IncidentCategory.API_LIMIT_EXCEEDED,
        "base_confidence": 80,
    },
]

# Severity-to-urgency mapping
SEVERITY_URGENCY_MAP: dict[str, Urgency] = {
    "low": Urgency.LOW,
    "medium": Urgency.MEDIUM,
    "high": Urgency.HIGH,
    "critical": Urgency.CRITICAL,
}


def classify_incident(payload: dict) -> dict:
    """
    Classify an incident by category, urgency, and confidence.

    Uses keyword matching with confidence adjustment based on:
      - Number of matching keywords (more matches = higher confidence)
      - Source reliability (Salesforce native > external > user reported)
      - Error message specificity

    Returns:
        dict with incident_type, category, confidence_score, urgency, matched_keywords
    """
    error_message = (payload.get("error_message") or "").lower()
    source = (payload.get("source") or "unknown").lower()
    severity = (payload.get("severity") or "medium").lower()
    incident_type_hint = payload.get("incident_type", "")

    # If incident_type is already provided and is a known category, trust it
    if incident_type_hint:
        try:
            IncidentCategory(incident_type_hint.lower())
            # Known type — boost confidence
            return {
                "incident_type": incident_type_hint.lower(),
                "category": incident_type_hint.lower(),
                "confidence_score": 90,
                "urgency": SEVERITY_URGENCY_MAP.get(severity, Urgency.MEDIUM).value,
                "matched_keywords": [],
                "classification_method": "provided",
            }
        except ValueError:
            pass

    # Keyword matching
    best_match: Optional[dict] = None
    best_confidence = 0
    matched_keywords: list[str] = []

    for rule in CLASSIFICATION_RULES:
        keywords_found = [kw for kw in rule["keywords"] if kw in error_message]
        if keywords_found:
            # More keyword matches = higher confidence
            confidence_boost = len(keywords_found) * 5
            confidence = min(rule["base_confidence"] + confidence_boost, 98)

            if confidence > best_confidence:
                best_confidence = confidence
                best_match = rule
                matched_keywords = keywords_found

    if best_match:
        category = best_match["category"].value
        confidence = best_confidence
    else:
        category = IncidentCategory.UNKNOWN.value
        confidence = 30
        matched_keywords = []

    # Source reliability adjustment
    source_reliability = {
        "salesforce": 5,
        "apex": 5,
        "flow": 4,
        "integration": 3,
        "user": -5,
        "monitoring": 4,
    }
    for src_key, boost in source_reliability.items():
        if src_key in source:
            confidence = min(max(confidence + boost, 0), 99)
            break

    # Determine urgency
    urgency = SEVERITY_URGENCY_MAP.get(severity, Urgency.MEDIUM).value

    # Upgrade urgency if high-confidence critical category
    if category in ("security_breach", "data_corruption") and confidence >= 80:
        urgency = Urgency.CRITICAL.value

    return {
        "incident_type": category,
        "category": category,
        "confidence_score": confidence,
        "urgency": urgency,
        "matched_keywords": matched_keywords,
        "classification_method": "keyword_match" if best_match else "fallback",
    }

