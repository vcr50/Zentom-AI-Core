def calculate_risk(payload: dict) -> dict:
    technical_severity = 20
    business_impact = 20
    blast_radius = 15
    operational_context = 10

    if payload.get("environment") == "production":
        operational_context += 10
        business_impact += 10

    if payload.get("incidentType") in ["FLOW_FAILURE", "APEX_EXCEPTION", "INTEGRATION_FAILURE"]:
        technical_severity += 10

    total_score = technical_severity + business_impact + blast_radius + operational_context

    if total_score >= 80:
        risk_level = "CRITICAL"
    elif total_score >= 60:
        risk_level = "HIGH"
    elif total_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "technicalSeverity": technical_severity,
        "businessImpact": business_impact,
        "blastRadius": blast_radius,
        "operationalContext": operational_context,
        "totalScore": total_score,
        "riskLevel": risk_level,
    }
