"""
Zentom Integration Engine — FastAPI Service

REST API endpoints for:
  - Salesforce case/task/incident management
  - Agentforce action lifecycle
  - Webhook delivery and tracking
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .salesforce_client import SalesforceClient, get_client as get_sf_client
from .agentforce_client import AgentforceClient, get_client as get_af_client
from .webhook_client import WebhookClient, WebhookEvent, get_client as get_wh_client

app = FastAPI(
    title="Zentom Integration Engine",
    version="1.0.0",
    description="Salesforce, Agentforce, and Webhook integration clients",
)


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class CaseInput(BaseModel):
    subject: str = Field(description="Case subject")
    description: str = ""
    origin: str = "Zentom AI"
    priority: str = "Medium"
    org_id: Optional[str] = None


class TaskInput(BaseModel):
    what_id: str = Field(description="Parent record ID")
    subject: str = Field(description="Task subject")
    description: str = ""
    owner_id: Optional[str] = None
    priority: str = "Normal"


class IncidentRecordInput(BaseModel):
    incident_type: str
    severity: str = "Medium"
    error_message: str = ""
    org_id: Optional[str] = None
    environment: str = "sandbox"
    raw_payload: Optional[dict] = None


class IncidentStatusUpdate(BaseModel):
    status: str
    resolution_notes: str = ""


class ActionSubmitInput(BaseModel):
    action_type: str = Field(description="Action type")
    target_object: str = ""
    target_id: str = ""
    parameters: Optional[dict] = None
    org_id: Optional[str] = None
    incident_id: Optional[int] = None
    auto_approve: bool = False


class ActionApproveInput(BaseModel):
    action_id: str
    approver: str = "system"


class WebhookSendInput(BaseModel):
    url: Optional[str] = None
    event: str = "incident.created"
    data: Optional[dict] = None
    org_id: Optional[str] = None
    incident_id: Optional[int] = None


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "service": "zentom-integration-engine",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ---------------------------------------------------------------------------
# Salesforce Endpoints
# ---------------------------------------------------------------------------

@app.post("/salesforce/case")
async def create_case(input: CaseInput):
    """Create a Salesforce Case."""
    client = get_sf_client()
    return client.create_case(
        subject=input.subject,
        description=input.description,
        origin=input.origin,
        priority=input.priority,
        org_id=input.org_id,
    )


@app.post("/salesforce/task")
async def create_task(input: TaskInput):
    """Create a Salesforce Task."""
    client = get_sf_client()
    return client.create_task(
        what_id=input.what_id,
        subject=input.subject,
        description=input.description,
        owner_id=input.owner_id,
        priority=input.priority,
    )


@app.post("/salesforce/incident")
async def create_incident_record(input: IncidentRecordInput):
    """Create a Sentinel_Incident__c record."""
    client = get_sf_client()
    return client.create_incident_record(
        incident_type=input.incident_type,
        severity=input.severity,
        error_message=input.error_message,
        org_id=input.org_id,
        environment=input.environment,
        raw_payload=input.raw_payload,
    )


@app.patch("/salesforce/incident/{record_id}/status")
async def update_incident_status(record_id: str, input: IncidentStatusUpdate):
    """Update a Sentinel_Incident__c status."""
    client = get_sf_client()
    return client.update_incident_status(
        record_id=record_id,
        status=input.status,
        resolution_notes=input.resolution_notes,
    )


@app.get("/salesforce/org-health/{org_id}")
async def get_org_health(org_id: str):
    """Get organization health metrics."""
    client = get_sf_client()
    return client.get_org_health(org_id)


# ---------------------------------------------------------------------------
# Agentforce Endpoints
# ---------------------------------------------------------------------------

@app.post("/agentforce/submit")
async def submit_action(input: ActionSubmitInput):
    """Submit an Agentforce action."""
    client = get_af_client()
    return client.submit_action(
        action_type=input.action_type,
        target_object=input.target_object,
        target_id=input.target_id,
        parameters=input.parameters,
        org_id=input.org_id,
        incident_id=input.incident_id,
        auto_approve=input.auto_approve,
    )


@app.post("/agentforce/approve")
async def approve_action(input: ActionApproveInput):
    """Approve a pending Agentforce action."""
    client = get_af_client()
    result = client.approve_action(input.action_id, input.approver)
    if "error" in result.get("status", ""):
        raise HTTPException(status_code=400, detail=result.get("message", "Approval failed"))
    return result


@app.post("/agentforce/execute/{action_id}")
async def execute_action(action_id: str):
    """Execute an approved Agentforce action."""
    client = get_af_client()
    result = client.execute_action(action_id)
    if "error" in result.get("status", ""):
        raise HTTPException(status_code=400, detail=result.get("message", "Execution failed"))
    return result


@app.post("/agentforce/reject/{action_id}")
async def reject_action(action_id: str, reason: str = ""):
    """Reject a pending Agentforce action."""
    client = get_af_client()
    return client.reject_action(action_id, reason)


@app.post("/agentforce/rollback/{action_id}")
async def rollback_action(action_id: str):
    """Rollback a completed Agentforce action."""
    client = get_af_client()
    return client.rollback_action(action_id)


@app.get("/agentforce/actions")
async def list_actions(
    status: Optional[str] = None,
    action_type: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
):
    """List Agentforce actions."""
    client = get_af_client()
    return {"actions": client.list_actions(status=status, action_type=action_type, limit=limit)}


@app.get("/agentforce/stats")
async def agentforce_stats():
    """Get Agentforce action statistics."""
    client = get_af_client()
    return client.get_stats()


# ---------------------------------------------------------------------------
# Webhook Endpoints
# ---------------------------------------------------------------------------

@app.post("/webhook/send")
async def send_webhook(input: WebhookSendInput):
    """Send a webhook notification."""
    client = get_wh_client()
    return client.send(
        url=input.url,
        event=input.event,
        data=input.data or {},
        org_id=input.org_id,
        incident_id=input.incident_id,
    )


@app.get("/webhook/deliveries")
async def list_deliveries(
    event: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
):
    """List webhook delivery records."""
    client = get_wh_client()
    return {"deliveries": client.list_deliveries(event=event, status=status, limit=limit)}


@app.get("/webhook/stats")
async def webhook_stats():
    """Get webhook delivery statistics."""
    client = get_wh_client()
    return client.get_stats()
