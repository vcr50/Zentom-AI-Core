# Zentom AI Engine

Intent classification, action recommendation, and LLM orchestration for incidents.

## Architecture

```
Incident → Classifier → Recommender → Policy Engine → Action
              ↓              ↓
         Category +      Runbook +
         Urgency +       Confidence +
         Confidence      Rationale
```

## Modules

| Module | Description |
|--------|-------------|
| `classifier.py` | Intent classification with keyword matching, confidence scoring, urgency detection |
| `recommender.py` | Action recommendation with runbook mapping, confidence blending, risk escalation |
| `prompts.py` | LLM prompt templates for DeepSeek R1, DeepSeek Coder, Llama 3, Agentforce |
| `main.py` | FastAPI service with REST endpoints |

## Classification Categories

| Category | Keywords | Base Confidence |
|----------|----------|----------------|
| payment_failure | stripe, razorpay, billing, charge | 85% |
| integration_error | sync, connector, webhook | 80% |
| data_corruption | corrupt, missing record, duplicate | 82% |
| security_breach | unauthorized, breach, access | 88% |
| performance_degradation | slow, timeout, latency | 75% |
| configuration_change | config, metadata, deploy | 70% |
| apex_exception | apex, exception, trigger, gack | 83% |
| flow_failure | flow, workflow, process builder | 78% |
| api_limit_exceeded | limit, governor, quota | 80% |
| user_reported | (fallback) | 60% |

## Runbook Actions

| Incident Type | Primary Action | Secondary Actions |
|---------------|---------------|-------------------|
| payment_failure | retry_failed_job | send_notification, update_dashboard |
| integration_error | restart_integration | run_diagnostic, send_notification |
| data_corruption | escalate_to_human | create_investigation_task, run_diagnostic |
| security_breach | escalate_to_human | modify_security_settings, send_notification |
| apex_exception | create_investigation_task | run_diagnostic, send_notification |

## LLM Prompt Templates

| Template | Purpose | Target Model |
|----------|---------|-------------|
| INCIDENT_RECOMMENDATION_PROMPT | Full incident analysis | DeepSeek R1 |
| INCIDENT_CLASSIFICATION_PROMPT | Type classification | Llama 3 |
| ROOT_CAUSE_ANALYSIS_PROMPT | 5-Why RCA | DeepSeek R1 |
| PREDICTIVE_ANALYSIS_PROMPT | Future incident prediction | DeepSeek R1 |
| VERIFICATION_PROMPT | Remediation verification | Llama 3 |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/categories` | List incident categories |
| `GET` | `/urgency-levels` | List urgency levels |
| `GET` | `/actions` | List action types |
| `GET` | `/runbooks` | List runbook mappings |
| `POST` | `/classify` | Classify an incident |
| `POST` | `/recommend` | Get action recommendation |
| `POST` | `/orchestrate` | Full classify → recommend pipeline |
| `POST` | `/prompt` | Generate formatted LLM prompt |

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8003 --reload
# API docs: http://localhost:8003/docs
```

## Docker

```bash
docker build -t zentom-ai-engine .
docker run -p 8003:8003 zentom-ai-engine
```

## Source

🔗 [github.com/vcr50/salesforce-ops-monitoring-platform](https://github.com/vcr50/salesforce-ops-monitoring-platform)

