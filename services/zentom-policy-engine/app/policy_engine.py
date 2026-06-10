"""
Zentom Policy Engine — Risk scoring, policy decisions, and approval workflows.

This engine evaluates incidents and determines the appropriate policy action:
- Risk scoring with multi-factor analysis
- Policy rule evaluation with configurable thresholds
- Approval workflow management
- Compliance and audit logging
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PolicyDecisionType(str, Enum):
    ALLOWED = "allowed"
    APPROVAL_REQUIRED = "approval_required"
    AUTO_REMEDIATE = "auto_remediate"
    BLOCKED = "blocked"
    ESCALATED = "escalated"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ESCALATED = "escalated"


# ---------------------------------------------------------------------------
# Risk Engine
# ---------------------------------------------------------------------------

SEVERITY_BASE_SCORES: dict[str, int] = {
    "low": 20, "medium": 45, "high": 70, "critical": 90,
}

ENVIRONMENT_MULTIPLIERS: dict[str, float] = {
    "production": 1.3, "staging": 1.0, "sandbox": 0.7, "dev": 0.5,
}

INCIDENT_TYPE_WEIGHTS: dict[str, float] = {
    "payment_failure": 1.4, "integration_error": 1.3,
    "data_corruption": 1.5, "security_breach": 1.6,
    "performance_degradation": 1.1, "configuration_change": 1.0,
    "apex_exception": 1.2, "flow_failure": 1.1,
    "api_limit_exceeded": 1.0, "user_reported": 1.15,
}

# Actions that always require manual approval
APPROVAL_REQUIRED_ACTIONS: set[str] = {
    "delete_record", "disable_flow", "update_permission_set",
    "execute_agentforce_action", "modify_security_settings",
    "bulk_data_update", "deploy_to_production",
}

# Actions that can be auto-remediated for low/medium risk
AUTO_REMEDIABLE_ACTIONS: set[str] = {
    "restart_integration", "clear_cache", "retry_failed_job",
    "send_notification", "log_incident", "update_dashboard",
}

# Risk score thresholds
POLICY_THRESHOLDS = {
    "auto_remediate_max": 35,
    "approval_required_min": 60,
    "blocked_min": 90,
}

TENANT_OVERRIDES: dict[str, dict] = {}


def get_thresholds(org_id: str | None = None) -> dict:
    base = POLICY_THRESHOLDS.copy()
    if org_id and org_id in TENANT_OVERRIDES:
        base.update(TENANT_OVERRIDES[org_id])
    return base


def decide_policy(
    risk_score: dict,
    action_type: str | None = None,
    org_id: str | None = None,
    auto_approve_enabled: bool = False,
) -> dict:
    """Evaluate risk score and action type to produce a policy decision."""
    total_score = risk_score.get("total_score", 0)
    thresholds = get_thresholds(org_id)

    if action_type and action_type in APPROVAL_REQUIRED_ACTIONS:
        return {
            "decision": PolicyDecisionType.APPROVAL_REQUIRED.value,
            "requires_approval": True,
            "reason": f"Action '{action_type}' always requires manual approval per policy.",
            "auto_remediated": False,
        }

    if total_score >= thresholds["blocked_min"]:
        return {
            "decision": PolicyDecisionType.BLOCKED.value,
            "requires_approval": True,
            "reason": f"Risk score {total_score} exceeds blocked threshold. Escalation required.",
            "auto_remediated": False,
        }

    if total_score >= thresholds["approval_required_min"]:
        return {
            "decision": PolicyDecisionType.APPROVAL_REQUIRED.value,
            "requires_approval": True,
            "reason": f"Risk score {total_score} meets approval threshold. Human review needed.",
            "auto_remediated": False,
        }

    if (
        action_type
        and action_type in AUTO_REMEDIABLE_ACTIONS
        and total_score <= thresholds["auto_remediate_max"]
    ):
        return {
            "decision": PolicyDecisionType.AUTO_REMEDIATE.value,
            "requires_approval": False,
            "reason": f"Low-risk ({total_score}) auto-remediable action '{action_type}'.",
            "auto_remediated": True,
        }

    if auto_approve_enabled and total_score < thresholds["approval_required_min"]:
        return {
            "decision": PolicyDecisionType.ALLOWED.value,
            "requires_approval": False,
            "reason": f"Auto-approve enabled. Risk score {total_score} below threshold.",
            "auto_remediated": False,
        }

    return {
        "decision": PolicyDecisionType.ALLOWED.value,
        "requires_approval": False,
        "reason": f"Risk score {total_score} is within allowed threshold.",
        "auto_remediated": False,
    }

