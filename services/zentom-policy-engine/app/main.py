"""
Zentom Policy Engine — FastAPI Service

REST API endpoints for:
  - Risk scoring
  - Policy decisions
  - Approval workflow management
  - Rule configuration
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .policy_engine import decide_policy, get_thresholds, POLICY_THRESHOLDS
from .risk_engine import score_risk
from .approval_rules import (
    ApprovalManager,
    ApprovalRule,
    ApprovalRequest,
    DEFAULT_APPROVAL_RULES,
    create_default_manager,
)

app = FastAPI(
    title="Zentom Policy Engine",
    version="1.0.0",
    description="Risk scoring, policy decisions, and approval workflows",
)

# Initialize with default rules
manager = create_default_manager()


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class IncidentInput(BaseModel):
    severity: str = Field(default="medium", description="Incident severity: low, medium, high, critical")
    environment: str = Field(default="sandbox", description="Environment: production, staging, sandbox, dev")
    incident_type: str = Field(default="unknown", description="Type of incident")
    blast_radius: int = Field(default=0, description="Number of affected objects")
    is_recurring: bool = Field(default=False, description="Same incident type in last 24h")
    outside_business_hours: bool = Field(default=False, description="Outside business hours")
    affected_users: int = Field(default=0, description="Number of affected users")
    action_type: Optional[str] = Field(default=None, description="Proposed action type")
    org_id: Optional[str] = Field(default=None, description="Tenant organization ID")
    auto_approve_enabled: bool = Field(default=False, description="Tenant auto-approve setting")


class RiskScoreResponse(BaseModel):
    technical_severity: int
    business_impact: int
    blast_radius: int
    operational_context: int
    total_score: int
    risk_level: str


class PolicyDecisionResponse(BaseModel):
    decision: str
    requires_approval: bool
    reason: str
    auto_remediated: bool


class FullEvaluationResponse(BaseModel):
    risk_score: RiskScoreResponse
    policy_decision: PolicyDecisionResponse
    matching_rules: list[dict]
    timestamp: str


class ApprovalActionRequest(BaseModel):
    request_id: str
    approver: str
    approved: bool
    reason: str = ""


class RuleCreateRequest(BaseModel):
    rule_id: str
    name: str
    condition: dict
    approver_roles: list[str]
    timeout_minutes: int = 60
    auto_escalate: bool = True
    enabled: bool = True


class ThresholdUpdateRequest(BaseModel):
    org_id: str
    auto_remediate_max: Optional[int] = None
    approval_required_min: Optional[int] = None
    blocked_min: Optional[int] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "service": "zentom-policy-engine",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/thresholds")
async def get_current_thresholds(org_id: Optional[str] = None):
    """Get current policy thresholds, optionally for a specific tenant."""
    return get_thresholds(org_id)


@app.post("/thresholds")
async def update_tenant_thresholds(request: ThresholdUpdateRequest):
    """Update policy thresholds for a specific tenant."""
    from .policy_engine import TENANT_OVERRIDES

    overrides = {}
    if request.auto_remediate_max is not None:
        overrides["auto_remediate_max"] = request.auto_remediate_max
    if request.approval_required_min is not None:
        overrides["approval_required_min"] = request.approval_required_min
    if request.blocked_min is not None:
        overrides["blocked_min"] = request.blocked_min

    TENANT_OVERRIDES[request.org_id] = overrides
    return {"org_id": request.org_id, "overrides": overrides}


@app.post("/risk-score", response_model=RiskScoreResponse)
async def compute_risk_score(incident: IncidentInput):
    """Compute a multi-factor risk score for an incident."""
    result = score_risk(incident.model_dump())
    return RiskScoreResponse(**result)


@app.post("/policy-decision", response_model=PolicyDecisionResponse)
async def compute_policy_decision(incident: IncidentInput):
    """Compute a policy decision for an incident (requires risk score first)."""
    risk = score_risk(incident.model_dump())
    decision = decide_policy(
        risk_score=risk,
        action_type=incident.action_type,
        org_id=incident.org_id,
        auto_approve_enabled=incident.auto_approve_enabled,
    )
    return PolicyDecisionResponse(**decision)


@app.post("/evaluate", response_model=FullEvaluationResponse)
async def full_evaluation(incident: IncidentInput):
    """Full evaluation: risk score + policy decision + matching approval rules."""
    incident_dict = incident.model_dump()

    # 1. Risk score
    risk = score_risk(incident_dict)

    # 2. Policy decision
    decision = decide_policy(
        risk_score=risk,
        action_type=incident.action_type,
        org_id=incident.org_id,
        auto_approve_enabled=incident.auto_approve_enabled,
    )

    # 3. Matching approval rules
    matching = manager.evaluate(incident_dict, risk, incident.action_type or "")
    matching_rules = [
        {"rule_id": r.rule_id, "name": r.name, "approver_roles": r.approver_roles}
        for r in matching
    ]

    return FullEvaluationResponse(
        risk_score=RiskScoreResponse(**risk),
        policy_decision=PolicyDecisionResponse(**decision),
        matching_rules=matching_rules,
        timestamp=datetime.utcnow().isoformat(),
    )


# ---------------------------------------------------------------------------
# Approval Workflow Endpoints
# ---------------------------------------------------------------------------

@app.get("/approvals/pending")
async def list_pending_approvals():
    """List all pending approval requests."""
    pending = manager.get_pending()
    return {"count": len(pending), "requests": [r.to_dict() for r in pending]}


@app.get("/approvals/{incident_id}")
async def get_approvals_for_incident(incident_id: int):
    """Get all approval requests for a specific incident."""
    requests = manager.get_by_incident(incident_id)
    return {"incident_id": incident_id, "requests": [r.to_dict() for r in requests]}


@app.post("/approvals/process")
async def process_approval(request: ApprovalActionRequest):
    """Approve or reject a pending approval request."""
    result = manager.process_approval(
        request_id=request.request_id,
        approver=request.approver,
        approved=request.approved,
        reason=request.reason,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Request not found or not pending")
    return result.to_dict()


@app.post("/approvals/check-timeouts")
async def check_approval_timeouts():
    """Check for expired approval requests and handle them."""
    expired = manager.check_timeouts()
    return {"expired_count": len(expired), "expired": [r.to_dict() for r in expired]}


# ---------------------------------------------------------------------------
# Rule Management Endpoints
# ---------------------------------------------------------------------------

@app.get("/rules")
async def list_rules():
    """List all configured approval rules."""
    return {
        "count": len(manager.rules),
        "rules": [
            {
                "rule_id": r.rule_id,
                "name": r.name,
                "condition": r.condition,
                "approver_roles": r.approver_roles,
                "timeout_minutes": r.timeout_minutes,
                "auto_escalate": r.auto_escalate,
                "enabled": r.enabled,
            }
            for r in manager.rules
        ],
    }


@app.post("/rules")
async def add_rule(request: RuleCreateRequest):
    """Add a new approval rule."""
    # Check for duplicate rule_id
    if any(r.rule_id == request.rule_id for r in manager.rules):
        raise HTTPException(status_code=409, detail=f"Rule '{request.rule_id}' already exists")

    rule = ApprovalRule(
        rule_id=request.rule_id,
        name=request.name,
        condition=request.condition,
        approver_roles=request.approver_roles,
        timeout_minutes=request.timeout_minutes,
        auto_escalate=request.auto_escalate,
        enabled=request.enabled,
    )
    manager.add_rule(rule)
    return {"message": "Rule added", "rule_id": request.rule_id}


@app.delete("/rules/{rule_id}")
async def delete_rule(rule_id: str):
    """Remove an approval rule."""
    if not any(r.rule_id == rule_id for r in manager.rules):
        raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found")
    manager.remove_rule(rule_id)
    return {"message": "Rule removed", "rule_id": rule_id}
