"""
Zentom AI Engine — FastAPI Service

REST API endpoints for:
  - Incident classification
  - Action recommendation
  - Full AI orchestration (classify → score risk → recommend → decide policy)
  - LLM prompt generation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .classifier import classify_incident, IncidentCategory, Urgency
from .recommender import recommend_action, ActionType, RUNBOOK_MAP
from .prompts import (
    INCIDENT_RECOMMENDATION_PROMPT,
    INCIDENT_CLASSIFICATION_PROMPT,
    ROOT_CAUSE_ANALYSIS_PROMPT,
    format_prompt,
)

app = FastAPI(
    title="Zentom AI Engine",
    version="1.0.0",
    description="Intent classification, action recommendation, and LLM orchestration",
)


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class IncidentInput(BaseModel):
    error_message: Optional[str] = Field(default=None, description="Error message text")
    source: Optional[str] = Field(default="unknown", description="Incident source")
    severity: str = Field(default="medium", description="Incident severity")
    environment: str = Field(default="sandbox", description="Environment")
    incident_type: Optional[str] = Field(default=None, description="Pre-classified type (optional)")
    org_id: Optional[str] = Field(default=None, description="Tenant organization ID")
    raw_payload: Optional[dict] = Field(default=None, description="Raw incident payload")


class ClassificationResponse(BaseModel):
    incident_type: str
    category: str
    confidence_score: int
    urgency: str
    matched_keywords: list[str]
    classification_method: str


class RecommendationResponse(BaseModel):
    summary: str
    root_cause: str
    recommended_action: str
    confidence_score: int
    runbook_key: str
    secondary_actions: list[str]
    rationale: str
    model_name: str


class OrchestrateResponse(BaseModel):
    classification: ClassificationResponse
    recommendation: RecommendationResponse
    timestamp: str


class PromptRequest(BaseModel):
    prompt_type: str = Field(default="recommendation", description="Prompt type: recommendation, classification, rca")
    variables: dict = Field(default_factory=dict, description="Variables to fill in the prompt template")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "service": "zentom-ai-engine",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/categories")
async def list_categories():
    """List all supported incident categories."""
    return {
        "categories": [
            {"value": cat.value, "name": cat.name}
            for cat in IncidentCategory
        ]
    }


@app.get("/urgency-levels")
async def list_urgency_levels():
    """List all urgency levels."""
    return {
        "urgency_levels": [
            {"value": urg.value, "name": urg.name}
            for urg in Urgency
        ]
    }


@app.get("/actions")
async def list_actions():
    """List all supported action types."""
    return {
        "actions": [
            {"value": action.value, "name": action.name}
            for action in ActionType
        ]
    }


@app.get("/runbooks")
async def list_runbooks():
    """List all runbook mappings."""
    return {
        "runbooks": {
            key: {
                "primary_action": rb["primary_action"].value,
                "secondary_actions": [a.value for a in rb["secondary_actions"]],
                "runbook_key": rb["runbook_key"],
                "base_confidence": rb["base_confidence"],
            }
            for key, rb in RUNBOOK_MAP.items()
        }
    }


@app.post("/classify", response_model=ClassificationResponse)
async def classify(incident: IncidentInput):
    """Classify an incident by category and urgency."""
    result = classify_incident(incident.model_dump())
    return ClassificationResponse(**result)


@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(incident: IncidentInput):
    """Generate an action recommendation for an incident."""
    # First classify, then recommend
    classification = classify_incident(incident.model_dump())
    recommendation = recommend_action(
        incident=incident.model_dump(),
        classification=classification,
    )
    return RecommendationResponse(**recommendation)


@app.post("/orchestrate", response_model=OrchestrateResponse)
async def orchestrate(incident: IncidentInput):
    """Full AI orchestration: classify → recommend."""
    classification = classify_incident(incident.model_dump())
    recommendation = recommend_action(
        incident=incident.model_dump(),
        classification=classification,
    )
    return OrchestrateResponse(
        classification=ClassificationResponse(**classification),
        recommendation=RecommendationResponse(**recommendation),
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/prompt")
async def generate_prompt(request: PromptRequest):
    """Generate a formatted LLM prompt from a template."""
    templates = {
        "recommendation": INCIDENT_RECOMMENDATION_PROMPT,
        "classification": INCIDENT_CLASSIFICATION_PROMPT,
        "rca": ROOT_CAUSE_ANALYSIS_PROMPT,
    }

    template = templates.get(request.prompt_type)
    if not template:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown prompt type: {request.prompt_type}. Available: {list(templates.keys())}",
        )

    formatted = format_prompt(template, **request.variables)
    return {"prompt_type": request.prompt_type, "prompt": formatted}
