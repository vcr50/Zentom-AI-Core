"""
Zentom Risk Engine — Multi-factor risk scoring for incidents.

Scoring factors:
  1. Technical severity base score (0-100)
  2. Environment multiplier (production > staging > sandbox > dev)
  3. Incident type weight (payment_failure, security_breach, etc.)
  4. Blast radius (number of affected objects)
  5. Recurrence bonus (same incident type in last 24h)
  6. Business hour penalty (incidents outside business hours are riskier)
  7. Affected users impact
"""

from .policy_engine import (
    SEVERITY_BASE_SCORES,
    ENVIRONMENT_MULTIPLIERS,
    INCIDENT_TYPE_WEIGHTS,
    RiskLevel,
)


def score_risk(incident: dict) -> dict:
    """
    Compute a multi-factor risk score for an incident.

    Returns a dict matching the RiskScore SQLAlchemy model fields:
      - technical_severity: int (0-100)
      - business_impact: int (0-30)
      - blast_radius: int (0-20)
      - operational_context: int (0-25)
      - total_score: int (0-100)
      - risk_level: str (low/medium/high/critical)
    """
    severity = incident.get("severity", "medium").lower()
    environment = incident.get("environment", "sandbox").lower()
    incident_type = incident.get("incident_type", "unknown").lower()
    blast_radius = incident.get("blast_radius", 0)
    is_recurring = incident.get("is_recurring", False)
    outside_business_hours = incident.get("outside_business_hours", False)
    affected_users = incident.get("affected_users", 0)

    # 1. Technical severity base
    technical_severity = SEVERITY_BASE_SCORES.get(severity, 45)

    # 2. Business impact — derived from affected users and type
    business_impact = min(int(affected_users * 0.5), 25)
    if incident_type in ("payment_failure", "data_corruption", "security_breach"):
        business_impact = min(business_impact + 15, 30)

    # 3. Blast radius score
    blast_radius_score = min(int(blast_radius * 2), 20)

    # 4. Operational context score
    operational_context = 0
    env_mult = ENVIRONMENT_MULTIPLIERS.get(environment, 1.0)
    type_weight = INCIDENT_TYPE_WEIGHTS.get(incident_type, 1.0)
    if is_recurring:
        operational_context += 10
    if outside_business_hours:
        operational_context += 5
    operational_context = min(operational_context, 25)

    # Weighted total
    raw_total = (
        technical_severity * env_mult * type_weight
        + business_impact
        + blast_radius_score
        + operational_context
    )
    total_score = min(int(raw_total), 100)

    # Determine risk level
    if total_score >= 80:
        risk_level = RiskLevel.CRITICAL.value
    elif total_score >= 60:
        risk_level = RiskLevel.HIGH.value
    elif total_score >= 35:
        risk_level = RiskLevel.MEDIUM.value
    else:
        risk_level = RiskLevel.LOW.value

    return {
        "technical_severity": technical_severity,
        "business_impact": business_impact,
        "blast_radius": blast_radius_score,
        "operational_context": operational_context,
        "total_score": total_score,
        "risk_level": risk_level,
    }


def score_risk_simple(incident: dict) -> dict:
    """
    Simple risk scoring for backward compatibility.
    Uses only severity to compute a base score.
    """
    severity = incident.get("severity", "medium")
    base_score = {"low": 25, "medium": 50, "high": 75, "critical": 90}.get(severity, 50)

    return {
        "total_score": base_score,
        "risk_level": "high" if base_score >= 75 else "medium" if base_score >= 50 else "low",
    }

