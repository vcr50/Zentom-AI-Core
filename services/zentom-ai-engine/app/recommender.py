"""
Zentom AI Engine — Action Recommender

Generates actionable recommendations for incidents based on:
  - Incident classification and risk level
  - Historical resolution patterns (runbook mapping)
  - Confidence scoring with reasoning
  - LLM-augmented analysis (when available)
"""

from enum import Enum
from typing import Optional


class ActionType(str, Enum):
    LOG_INCIDENT = "log_incident"
    SEND_NOTIFICATION = "send_notification"
    RETRY_FAILED_JOB = "retry_failed_job"
    CLEAR_CACHE = "clear_cache"
    RESTART_INTEGRATION = "restart_integration"
    UPDATE_DASHBOARD = "update_dashboard"
    CREATE_INVESTIGATION_TASK = "create_investigation_task"
    RUN_DIAGNOSTIC = "run_diagnostic"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    EXECUTE_AGENTFORCE_ACTION = "execute_agentforce_action"
    DELETE_RECORD = "delete_record"
    DISABLE_FLOW = "disable_flow"
    UPDATE_PERMISSION_SET = "update_permission_set"
    DEPLOY_TO_PRODUCTION = "deploy_to_production"
    BULK_DATA_UPDATE = "bulk_data_update"
    MODIFY_SECURITY_SETTINGS = "modify_security_settings"
    NO_ACTION = "no_action"


# Runbook mapping: incident_type → recommended actions
RUNBOOK_MAP: dict[str, dict] = {
    "payment_failure": {
        "primary_action": ActionType.RETRY_FAILED_JOB,
        "secondary_actions": [ActionType.SEND_NOTIFICATION, ActionType.UPDATE_DASHBOARD],
        "runbook_key": "rb-payment-failure",
        "summary_template": "Payment integration failure detected. Retry the failed transaction and notify the finance team.",
        "root_cause_template": "Payment gateway (Stripe/Razorpay) returned an error or timeout during transaction processing.",
        "base_confidence": 85,
    },
    "integration_error": {
        "primary_action": ActionType.RESTART_INTEGRATION,
        "secondary_actions": [ActionType.RUN_DIAGNOSTIC, ActionType.SEND_NOTIFICATION],
        "runbook_key": "rb-integration-error",
        "summary_template": "External integration sync failure. Restart the connector and run diagnostics.",
        "root_cause_template": "The integration connector lost connectivity or received an invalid response from the external service.",
        "base_confidence": 80,
    },
    "data_corruption": {
        "primary_action": ActionType.ESCALATE_TO_HUMAN,
        "secondary_actions": [ActionType.CREATE_INVESTIGATION_TASK, ActionType.RUN_DIAGNOSTIC],
        "runbook_key": "rb-data-corruption",
        "summary_template": "Data integrity issue detected. Escalate for manual review and investigation.",
        "root_cause_template": "Potential data corruption from failed sync, duplicate records, or orphaned data relationships.",
        "base_confidence": 75,
    },
    "security_breach": {
        "primary_action": ActionType.ESCALATE_TO_HUMAN,
        "secondary_actions": [ActionType.MODIFY_SECURITY_SETTINGS, ActionType.SEND_NOTIFICATION],
        "runbook_key": "rb-security-breach",
        "summary_template": "Security anomaly detected. Immediately escalate and lock down affected access.",
        "root_cause_template": "Unauthorized access attempt, permission escalation, or suspicious login pattern detected.",
        "base_confidence": 90,
    },
    "performance_degradation": {
        "primary_action": ActionType.CLEAR_CACHE,
        "secondary_actions": [ActionType.RUN_DIAGNOSTIC, ActionType.UPDATE_DASHBOARD],
        "runbook_key": "rb-performance",
        "summary_template": "Performance degradation detected. Clear caches and run system diagnostics.",
        "root_cause_template": "Resource exhaustion (CPU, memory, heap) or inefficient query patterns causing slowdowns.",
        "base_confidence": 72,
    },
    "apex_exception": {
        "primary_action": ActionType.CREATE_INVESTIGATION_TASK,
        "secondary_actions": [ActionType.RUN_DIAGNOSTIC, ActionType.SEND_NOTIFICATION],
        "runbook_key": "rb-apex-exception",
        "summary_template": "Apex exception detected. Create investigation task for developer review.",
        "root_cause_template": "Unhandled exception in Apex trigger or class execution (null pointer, governor limit, DML error).",
        "base_confidence": 82,
    },
    "flow_failure": {
        "primary_action": ActionType.DISABLE_FLOW,
        "secondary_actions": [ActionType.SEND_NOTIFICATION, ActionType.CREATE_INVESTIGATION_TASK],
        "runbook_key": "rb-flow-failure",
        "summary_template": "Flow execution failure. Disable the failing flow and notify the automation team.",
        "root_cause_template": "Flow encountered an error in decision element, assignment, or loop iteration.",
        "base_confidence": 78,
    },
    "api_limit_exceeded": {
        "primary_action": ActionType.SEND_NOTIFICATION,
        "secondary_actions": [ActionType.LOG_INCIDENT, ActionType.UPDATE_DASHBOARD],
        "runbook_key": "rb-api-limits",
        "summary_template": "API limit exceeded. Notify the team and log for capacity planning.",
        "root_cause_template": "Organization exceeded Salesforce API request limits due to bulk operations or integration volume.",
        "base_confidence": 88,
    },
    "configuration_change": {
        "primary_action": ActionType.RUN_DIAGNOSTIC,
        "secondary_actions": [ActionType.LOG_INCIDENT, ActionType.SEND_NOTIFICATION],
        "runbook_key": "rb-config-change",
        "summary_template": "Configuration change detected. Run diagnostics to verify system integrity.",
        "root_cause_template": "Metadata change, deployment, or manual configuration update altered system behavior.",
        "base_confidence": 70,
    },
    "user_reported": {
        "primary_action": ActionType.CREATE_INVESTIGATION_TASK,
        "secondary_actions": [ActionType.SEND_NOTIFICATION, ActionType.LOG_INCIDENT],
        "runbook_key": "rb-user-reported",
        "summary_template": "User-reported issue. Create investigation task and acknowledge to reporter.",
        "root_cause_template": "End user reported unexpected behavior; root cause pending investigation.",
        "base_confidence": 60,
    },
}

# Default runbook for unknown incident types
DEFAULT_RUNBOOK: dict = {
    "primary_action": ActionType.CREATE_INVESTIGATION_TASK,
    "secondary_actions": [ActionType.SEND_NOTIFICATION, ActionType.LOG_INCIDENT],
    "runbook_key": "rb-unknown",
    "summary_template": "Unrecognized incident pattern. Create investigation task for manual review.",
    "root_cause_template": "Unable to determine root cause automatically. Manual investigation required.",
    "base_confidence": 40,
}


def recommend_action(incident: dict, classification: dict | None = None, risk_score: dict | None = None) -> dict:
    """
    Generate an actionable recommendation for an incident.

    Args:
        incident: Raw incident data
        classification: Output from classifier (optional)
        risk_score: Output from risk engine (optional)

    Returns:
        dict with summary, root_cause, recommended_action, confidence_score,
        runbook_key, secondary_actions, rationale
    """
    # Determine incident type
    if classification and classification.get("incident_type"):
        incident_type = classification["incident_type"]
    else:
        incident_type = incident.get("incident_type", "unknown")

    # Get runbook
    runbook = RUNBOOK_MAP.get(incident_type, DEFAULT_RUNBOOK)

    # Base confidence from runbook
    confidence = runbook["base_confidence"]

    # Adjust confidence based on classification quality
    if classification:
        class_confidence = classification.get("confidence_score", 50)
        # Blend: 60% runbook confidence + 40% classification confidence
        confidence = int(confidence * 0.6 + class_confidence * 0.4)

    # Adjust confidence based on risk score
    if risk_score:
        total_score = risk_score.get("total_score", 50)
        # High risk with high confidence = trust the recommendation
        # High risk with low confidence = reduce confidence, needs human review
        if total_score >= 80 and confidence < 70:
            confidence = max(confidence - 10, 30)
        elif total_score <= 30:
            confidence = min(confidence + 5, 95)

    # Determine primary action
    primary_action = runbook["primary_action"].value

    # Escalate if risk is very high regardless of runbook
    if risk_score and risk_score.get("total_score", 0) >= 90:
        primary_action = ActionType.ESCALATE_TO_HUMAN.value
        confidence = min(confidence + 5, 95)

    # Build rationale
    risk_level = risk_score.get("risk_level", "medium") if risk_score else "unknown"
    urgency = classification.get("urgency", "medium") if classification else "medium"

    rationale_parts = []
    rationale_parts.append(f"Incident classified as '{incident_type}' with {urgency} urgency.")
    if risk_score:
        rationale_parts.append(f"Risk assessment: {risk_level} (score: {risk_score.get('total_score', 'N/A')}).")
    rationale_parts.append(f"Runbook '{runbook['runbook_key']}' suggests {primary_action}.")
    if confidence < 60:
        rationale_parts.append("Low confidence — human review recommended.")

    return {
        "summary": runbook["summary_template"],
        "root_cause": runbook["root_cause_template"],
        "recommended_action": primary_action,
        "confidence_score": confidence,
        "runbook_key": runbook["runbook_key"],
        "secondary_actions": [a.value for a in runbook["secondary_actions"]],
        "rationale": " ".join(rationale_parts),
        "model_name": "zentom-recommender-v1",
    }

