import logging

from sqlalchemy.orm import Session

from app.models import AIRecommendation, Incident, PolicyDecision, RiskScore
from app.services.memory_service import create_incident_memory
from app.services.zentom_brain_engine import analyze_incident

logger = logging.getLogger(__name__)


def process_incident(payload: dict, db: Session) -> dict:
    brain_result = analyze_incident(payload, db=db)
    risk_result = brain_result["risk"]
    policy_result = brain_result["policy"]
    recommendation_result = brain_result["recommendation"]

    incident = Incident(
        org_id=payload.get("orgId"),
        incident_type=payload.get("incidentType"),
        source=payload.get("source"),
        environment=payload.get("environment", "sandbox"),
        error_message=payload.get("errorMessage"),
        confidence=payload.get("confidence", 0),
        action_type=payload.get("actionType", "CREATE_CASE"),
        raw_payload=payload,
    )
    db.add(incident)
    db.flush()

    db.add(
        RiskScore(
            incident_id=incident.id,
            technical_severity=risk_result["technicalSeverity"],
            business_impact=risk_result["businessImpact"],
            blast_radius=risk_result["blastRadius"],
            operational_context=risk_result["operationalContext"],
            total_score=risk_result["totalScore"],
            risk_level=risk_result["riskLevel"],
        )
    )

    db.add(
        PolicyDecision(
            incident_id=incident.id,
            decision=policy_result["decision"],
            requires_approval=policy_result["requiresApproval"],
            reason=policy_result["reason"],
        )
    )

    db.add(
        AIRecommendation(
            incident_id=incident.id,
            summary=recommendation_result["summary"],
            root_cause=recommendation_result["rootCause"],
            recommended_action=recommendation_result["recommendedAction"],
            confidence_score=recommendation_result["confidenceScore"],
            runbook_key=recommendation_result["runbookKey"],
            recommendation_status=recommendation_result["recommendationStatus"],
            model_name=recommendation_result["modelName"],
            raw_model_output=recommendation_result,
        )
    )

    db.commit()
    db.refresh(incident)

    try:
        create_incident_memory(
            db=db,
            incident_id=incident.id,
            payload=payload,
            risk=risk_result,
            policy=policy_result,
            recommendation=recommendation_result,
        )
    except Exception as exc:
        db.rollback()
        logger.warning("Memory creation failed for incident %s: %s", incident.id, exc)

    return {
        "message": "Incident received successfully",
        "incidentId": incident.id,
        "incident": payload,
        "risk": risk_result,
        "policy": policy_result,
        "recommendation": recommendation_result,
        "aiTrace": brain_result["aiTrace"],
        "brain": brain_result["brain"],
        "memory": brain_result.get("memory", {}),
    }
