# Zentom Integration Engine

Salesforce, Agentforce, and Webhook integration clients for Zentom.

## Architecture

```
Zentom API → Integration Engine → Salesforce (Cases, Tasks, Incidents)
                               → Agentforce (Action Execution)
                               → Webhooks (Slack, Teams, PagerDuty)
```

## Modules

| Module | Description |
|--------|-------------|
| `salesforce_client.py` | SalesforceClient — Cases, Tasks, Sentinel_Incident__c, SOQL, Org Health |
| `agentforce_client.py` | AgentforceClient — Action lifecycle: submit → approve → execute → rollback |
| `webhook_client.py` | WebhookClient — Outbound webhooks with HMAC signing and delivery tracking |
| `main.py` | FastAPI service with REST endpoints |

## Salesforce Client

| Operation | Description |
|-----------|-------------|
| `create_case` | Create a Case from an incident |
| `create_task` | Create a Task linked to a parent record |
| `create_incident_record` | Create Sentinel_Incident__c custom object |
| `update_incident_status` | Update incident status + resolution notes |
| `query` | Execute SOQL queries |
| `get_org_health` | Get API usage, storage, active users, health score |

## Agentforce Client

| Action Type | Risk Level | Auto-Approve |
|-------------|-----------|--------------|
| send_notification | Low | ✅ |
| run_diagnostic | Low | ✅ |
| clear_cache | Low | ✅ |
| retry_integration | Low | ✅ |
| update_record | Medium | ⚠️ |
| create_record | Medium | ⚠️ |
| enable_flow | Medium | ⚠️ |
| delete_record | High | ❌ |
| disable_flow | High | ❌ |
| update_permission_set | High | ❌ |
| deploy_metadata | High | ❌ |

### Action Lifecycle

```
submit → pending_approval → approved → executing → completed
                                    ↓                ↓
                                 rejected        rolled_back
```

## Webhook Client

| Event | Description |
|-------|-------------|
| `incident.created` | New incident detected |
| `incident.classified` | AI classification complete |
| `incident.risk_scored` | Risk assessment complete |
| `incident.policy_decided` | Policy decision made |
| `incident.action_recommended` | AI recommendation ready |
| `incident.action_executed` | Action executed |
| `approval.required` | Human approval needed |
| `approval.completed` | Approval resolved |
| `escalation.triggered` | Incident escalated |

### Security

- HMAC-SHA256 signature on all payloads (`X-Zentom-Signature` header)
- Timestamp-based replay protection
- Configurable signing secret per environment

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `POST` | `/salesforce/case` | Create Case |
| `POST` | `/salesforce/task` | Create Task |
| `POST` | `/salesforce/incident` | Create Incident Record |
| `PATCH` | `/salesforce/incident/{id}/status` | Update Incident Status |
| `GET` | `/salesforce/org-health/{org_id}` | Get Org Health |
| `POST` | `/agentforce/submit` | Submit Action |
| `POST` | `/agentforce/approve` | Approve Action |
| `POST` | `/agentforce/execute/{id}` | Execute Action |
| `POST` | `/agentforce/reject/{id}` | Reject Action |
| `POST` | `/agentforce/rollback/{id}` | Rollback Action |
| `GET` | `/agentforce/actions` | List Actions |
| `GET` | `/agentforce/stats` | Action Statistics |
| `POST` | `/webhook/send` | Send Webhook |
| `GET` | `/webhook/deliveries` | List Deliveries |
| `GET` | `/webhook/stats` | Delivery Statistics |

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8005 --reload
# API docs: http://localhost:8005/docs
```

## Docker

```bash
docker build -t zentom-integration-engine .
docker run -p 8005:8005 zentom-integration-engine
```

## Source

🔗 [github.com/vcr50/salesforce-ops-monitoring-platform](https://github.com/vcr50/salesforce-ops-monitoring-platform)

