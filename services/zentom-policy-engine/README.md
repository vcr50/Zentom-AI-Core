# Zentom Policy Engine

Risk scoring, policy decisions, and approval workflows for incident handling.

## Architecture

```
Incident → Risk Engine → Policy Engine → Approval Manager → Action
              ↓               ↓                ↓
         RiskScore       PolicyDecision    ApprovalRequest
         (0-100)         (allowed/          (pending/
                         blocked/           approved/
                         approval_required/ rejected/
                         auto_remediate)    escalated)
```

## Modules

| Module | Description |
|--------|-------------|
| `policy_engine.py` | Core policy decision logic, enums, thresholds, tenant overrides |
| `risk_engine.py` | Multi-factor risk scoring (severity, environment, type, blast radius, recurrence) |
| `approval_rules.py` | ApprovalRule, ApprovalRequest, ApprovalManager, default rules |
| `main.py` | FastAPI service with REST endpoints |

## Risk Scoring Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Technical Severity | Base (20-90) | low=20, medium=45, high=70, critical=90 |
| Environment Multiplier | ×1.3 / ×1.0 / ×0.7 / ×0.5 | production > staging > sandbox > dev |
| Incident Type Weight | ×1.0 - ×1.6 | security_breach=1.6, payment_failure=1.4, etc. |
| Blast Radius | +0-20 | Number of affected objects |
| Recurrence | +10 | Same incident type in last 24h |
| Business Hours | +5 | Incident outside business hours |
| Affected Users | +0-25 | Derived from user count + incident type |

## Policy Decision Logic

1. **APPROVAL_REQUIRED** — Action is in the always-approve list (delete_record, deploy_to_production, etc.)
2. **BLOCKED** — Risk score ≥ 90 (must escalate to human)
3. **APPROVAL_REQUIRED** — Risk score ≥ 60 (human review needed)
4. **AUTO_REMEDIATE** — Low-risk (≤35) + auto-remediable action (retry_failed_job, clear_cache, etc.)
5. **ALLOWED** — Below approval threshold (with optional auto-approve for tenants)

## Default Approval Rules

| Rule | Condition | Approvers | Timeout |
|------|-----------|-----------|---------|
| Critical Prod | severity=critical + env=production | admin, cto | 30 min |
| High Risk | risk_score ≥ 70 | manager, admin | 60 min |
| Destructive Action | delete_record, disable_flow, etc. | admin | 120 min |
| Agentforce | execute_agentforce_action | operator, admin | 45 min |
| Payment Prod | payment_failure + production | finance, admin | 20 min |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/thresholds` | Get policy thresholds |
| `POST` | `/thresholds` | Update tenant thresholds |
| `POST` | `/risk-score` | Compute risk score |
| `POST` | `/policy-decision` | Compute policy decision |
| `POST` | `/evaluate` | Full evaluation (risk + policy + rules) |
| `GET` | `/approvals/pending` | List pending approvals |
| `GET` | `/approvals/{incident_id}` | Get approvals for incident |
| `POST` | `/approvals/process` | Approve or reject a request |
| `POST` | `/approvals/check-timeouts` | Check expired requests |
| `GET` | `/rules` | List approval rules |
| `POST` | `/rules` | Add new rule |
| `DELETE` | `/rules/{rule_id}` | Remove a rule |

## Run

```bash
# Install dependencies
pip install -r requirements.txt

# Start the service
uvicorn app.main:app --port 8002 --reload

# API docs
open http://localhost:8002/docs
```

## Docker

```bash
docker build -t zentom-policy-engine .
docker run -p 8002:8002 zentom-policy-engine
```

## Source

🔗 [github.com/vcr50/salesforce-ops-monitoring-platform](https://github.com/vcr50/salesforce-ops-monitoring-platform)

