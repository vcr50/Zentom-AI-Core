from pydantic import BaseModel, Field


class IncidentPayload(BaseModel):
    org_id: str | None = Field(default=None, alias="orgId")
    incident_type: str | None = Field(default=None, alias="incidentType")
    source: str | None = None
    environment: str = "sandbox"
    error_message: str | None = Field(default=None, alias="errorMessage")
    confidence: int = 0
    action_type: str = Field(default="CREATE_CASE", alias="actionType")

    model_config = {
        "populate_by_name": True,
        "extra": "allow",
    }


class RiskResult(BaseModel):
    technical_severity: int = Field(alias="technicalSeverity")
    business_impact: int = Field(alias="businessImpact")
    blast_radius: int = Field(alias="blastRadius")
    operational_context: int = Field(alias="operationalContext")
    total_score: int = Field(alias="totalScore")
    risk_level: str = Field(alias="riskLevel")


class PolicyResult(BaseModel):
    decision: str
    requires_approval: bool = Field(alias="requiresApproval")
    reason: str
