"""
Zentom Approval Rules — Configurable approval workflows and request management.

Provides:
  - ApprovalRule: Configurable rule with conditions, approver roles, and timeout
  - ApprovalRequest: Tracks individual approval requests through their lifecycle
  - ApprovalManager: Orchestrates rule evaluation, request creation, and escalation
  - Default approval rules for common scenarios
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from .policy_engine import ApprovalStatus


class ApprovalRule:
    """Represents a configurable approval rule."""

    def __init__(
        self,
        rule_id: str,
        name: str,
        condition: dict,
        approver_roles: list[str],
        timeout_minutes: int = 60,
        auto_escalate: bool = True,
        enabled: bool = True,
    ):
        self.rule_id = rule_id
        self.name = name
        self.condition = condition
        self.approver_roles = approver_roles
        self.timeout_minutes = timeout_minutes
        self.auto_escalate = auto_escalate
        self.enabled = enabled

    def evaluate(self, incident: dict, risk_score: dict) -> bool:
        """Check if this rule applies to the given incident + risk score."""
        if not self.enabled:
            return False

        cond = self.condition

        if "severity_in" in cond:
            if incident.get("severity", "").lower() not in cond["severity_in"]:
                return False

        if "min_risk_score" in cond:
            if risk_score.get("total_score", 0) < cond["min_risk_score"]:
                return False

        if "action_type_in" in cond:
            if incident.get("action_type", "") not in cond["action_type_in"]:
                return False

        if "environment_in" in cond:
            if incident.get("environment", "").lower() not in cond["environment_in"]:
                return False

        if "incident_type_in" in cond:
            if incident.get("incident_type", "").lower() not in cond["incident_type_in"]:
                return False

        return True


class ApprovalRequest:
    """Tracks an individual approval request through its lifecycle."""

    def __init__(
        self,
        request_id: str,
        incident_id: int,
        rule_id: str,
        action_type: str,
        approver_roles: list[str],
        timeout_minutes: int = 60,
        auto_escalate: bool = True,
    ):
        self.request_id = request_id
        self.incident_id = incident_id
        self.rule_id = rule_id
        self.action_type = action_type
        self.approver_roles = approver_roles
        self.timeout_minutes = timeout_minutes
        self.auto_escalate = auto_escalate
        self.status = ApprovalStatus.PENDING.value
        self.created_at = datetime.utcnow()
        self.resolved_at: Optional[datetime] = None
        self.approver: Optional[str] = None
        self.reason: Optional[str] = None
        self.escalation_count = 0

    @property
    def is_expired(self) -> bool:
        """Check if the request has exceeded its timeout."""
        if self.status != ApprovalStatus.PENDING.value:
            return False
        elapsed = datetime.utcnow() - self.created_at
        return elapsed > timedelta(minutes=self.timeout_minutes)

    def approve(self, approver: str, reason: str = "") -> None:
        """Mark the request as approved."""
        self.status = ApprovalStatus.APPROVED.value
        self.approver = approver
        self.reason = reason
        self.resolved_at = datetime.utcnow()

    def reject(self, approver: str, reason: str = "") -> None:
        """Mark the request as rejected."""
        self.status = ApprovalStatus.REJECTED.value
        self.approver = approver
        self.reason = reason
        self.resolved_at = datetime.utcnow()

    def escalate(self) -> None:
        """Escalate the request (e.g., to higher-level approvers)."""
        self.status = ApprovalStatus.ESCALATED.value
        self.escalation_count += 1

    def expire(self) -> None:
        """Mark the request as expired due to timeout."""
        self.status = ApprovalStatus.EXPIRED.value
        self.resolved_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Serialize the request to a dictionary."""
        return {
            "request_id": self.request_id,
            "incident_id": self.incident_id,
            "rule_id": self.rule_id,
            "action_type": self.action_type,
            "approver_roles": self.approver_roles,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "approver": self.approver,
            "reason": self.reason,
            "escalation_count": self.escalation_count,
            "timeout_minutes": self.timeout_minutes,
        }


class ApprovalManager:
    """Orchestrates approval rule evaluation, request creation, and escalation."""

    def __init__(self, rules: list[ApprovalRule] | None = None):
        self.rules: list[ApprovalRule] = rules or []
        self.pending_requests: dict[str, ApprovalRequest] = {}
        self._request_counter = 0

    def add_rule(self, rule: ApprovalRule) -> None:
        self.rules.append(rule)

    def remove_rule(self, rule_id: str) -> None:
        self.rules = [r for r in self.rules if r.rule_id != rule_id]

    def _next_request_id(self) -> str:
        self._request_counter += 1
        return f"apr-{self._request_counter:06d}"

    def evaluate(
        self, incident: dict, risk_score: dict, action_type: str
    ) -> list[ApprovalRule]:
        """Return all rules that match the given incident context."""
        return [
            rule for rule in self.rules
            if rule.evaluate(incident, risk_score)
        ]

    def create_request(
        self,
        incident_id: int,
        rule: ApprovalRule,
        action_type: str,
    ) -> ApprovalRequest:
        """Create a new approval request from a matched rule."""
        request = ApprovalRequest(
            request_id=self._next_request_id(),
            incident_id=incident_id,
            rule_id=rule.rule_id,
            action_type=action_type,
            approver_roles=rule.approver_roles,
            timeout_minutes=rule.timeout_minutes,
            auto_escalate=rule.auto_escalate,
        )
        self.pending_requests[request.request_id] = request
        return request

    def process_approval(
        self, request_id: str, approver: str, approved: bool, reason: str = ""
    ) -> ApprovalRequest | None:
        """Process an approval or rejection for a pending request."""
        request = self.pending_requests.get(request_id)
        if not request or request.status != ApprovalStatus.PENDING.value:
            return None

        if approved:
            request.approve(approver, reason)
        else:
            request.reject(approver, reason)

        return request

    def check_timeouts(self) -> list[ApprovalRequest]:
        """Find and handle expired requests. Auto-escalate if configured."""
        expired = []
        for request in self.pending_requests.values():
            if request.is_expired:
                if request.auto_escalate and request.escalation_count < 3:
                    request.escalate()
                else:
                    request.expire()
                expired.append(request)
        return expired

    def get_pending(self) -> list[ApprovalRequest]:
        """Return all currently pending requests."""
        return [
            r for r in self.pending_requests.values()
            if r.status == ApprovalStatus.PENDING.value
        ]

    def get_by_incident(self, incident_id: int) -> list[ApprovalRequest]:
        """Return all requests for a specific incident."""
        return [
            r for r in self.pending_requests.values()
            if r.incident_id == incident_id
        ]


# ---------------------------------------------------------------------------
# Default Approval Rules
# ---------------------------------------------------------------------------

DEFAULT_APPROVAL_RULES: list[ApprovalRule] = [
    ApprovalRule(
        rule_id="rule_critical_prod",
        name="Critical incidents in production require admin approval",
        condition={"severity_in": ["critical"], "environment_in": ["production"]},
        approver_roles=["admin", "cto"],
        timeout_minutes=30,
        auto_escalate=True,
    ),
    ApprovalRule(
        rule_id="rule_high_risk",
        name="High risk score requires manager approval",
        condition={"min_risk_score": 70},
        approver_roles=["manager", "admin"],
        timeout_minutes=60,
        auto_escalate=True,
    ),
    ApprovalRule(
        rule_id="rule_destructive_action",
        name="Destructive actions require admin approval",
        condition={"action_type_in": ["delete_record", "disable_flow", "update_permission_set"]},
        approver_roles=["admin"],
        timeout_minutes=120,
        auto_escalate=False,
    ),
    ApprovalRule(
        rule_id="rule_agentforce",
        name="Agentforce actions require operator approval",
        condition={"action_type_in": ["execute_agentforce_action"]},
        approver_roles=["operator", "admin"],
        timeout_minutes=45,
        auto_escalate=True,
    ),
    ApprovalRule(
        rule_id="rule_payment_prod",
        name="Payment failures in production require finance approval",
        condition={
            "incident_type_in": ["payment_failure"],
            "environment_in": ["production"],
        },
        approver_roles=["finance", "admin"],
        timeout_minutes=20,
        auto_escalate=True,
    ),
]


def create_default_manager() -> ApprovalManager:
    """Create an ApprovalManager pre-loaded with default rules."""
    manager = ApprovalManager()
    for rule in DEFAULT_APPROVAL_RULES:
        manager.add_rule(rule)
    return manager


# Keep backward-compatible constant
APPROVAL_REQUIRED_ACTIONS = {
    "delete_record",
    "disable_flow",
    "update_permission_set",
    "execute_agentforce_action",
    "modify_security_settings",
    "bulk_data_update",
    "deploy_to_production",
}

