# Zentom Maintenance Log

## Milestone 17C: Hosted PostgreSQL / Production DB Hardening

Status: Complete

Date: 2026-05-24

Hosted API:

```text
https://zentom-api.onrender.com
```

Verification summary:

- Hosted PostgreSQL connected through Render `DATABASE_URL`.
- `/api/health/db` passed.
- Database type verified as `postgresql`.
- Required tables verified:
  - `incidents`
  - `risk_scores`
  - `policy_decisions`
  - `ai_recommendations`
  - `memory_entries`
- `pgvector` verified as enabled.
- Hosted incident persistence passed.
- Direct Render incident test returned hosted DB incident id `4`.
- Salesforce anonymous Apex created `Sentinel_Incident__c` record `SI-000010`.
- Salesforce write-back used hosted DB incident id `5`.
- Salesforce audit logs verified:
  - `INCIDENT_RECEIVED`
  - `RISK_CALCULATED`
  - `ZENTOM_POLICY_EVALUATED`
  - `AI_RECOMMENDATION_GENERATED`
  - `RUNBOOK_SELECTED`

Production mode:

```text
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_MODEL=zentom-rule-v1
```

Hosted AI/Ollama remains disabled for the online beta. Vector/RAG memory remains available at the database layer, with model-hosting strategy deferred to Milestone 17D.

## Milestone 17D: Hosted AI / Local Model Strategy Decision

Status: Complete

Date: 2026-05-24

Decision summary:

- Hosted Render beta remains `AI_MODE=RULE`.
- Local advanced demo remains `AI_MODE=HYBRID` with Ollama `phi3:mini`, `all-minilm`, PostgreSQL, and pgvector.
- Ollama is not hosted online for beta.
- Ollama must never be exposed directly to the public internet.
- Production hosted AI provider decision is deferred until after beta workflow validation.

Decision document:

```text
docs/hosted-ai-strategy.md
```

## Milestone 18: Salesforce Package Hardening

Status: Started

Date: 2026-05-24

Hosted API:

```text
https://zentom-api.onrender.com
```

Known beta limitation:

```text
Hosted API uses RULE mode. Hosted Ollama/LLM serving is intentionally disabled.
```

18A package manifest:

```text
apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml
```

18A/18B validation:

- Beta manifest created with stable SentinelFlow Apex, LWC, object, custom metadata, app, tab, page, layout, permission set, and remote site metadata.
- Excluded experimental Agentforce metadata, old static resources, tmp files, and unstable package drift.
- Validation org: `astrosoft`.
- Deploy validation ID: `0AfdL00000ayMNVSA2`.
- Stable tests passed: 14.
- Stable tests failed: 0.

18C permission set hardening:

- `SentinelFlow_Admin` narrowed to stable beta components with full access to SentinelFlow incidents, audit logs, policy decisions, app tabs, and runtime Apex.
- `SentinelFlow_Approver` added for approve, reject, replay, dashboard, and execute workflows.
- `SentinelFlow_Viewer` narrowed to read-only incident, audit, policy, replay, and dashboard access.
- Legacy broad `SentinelFlow_Operator` remains in source but is excluded from the beta manifest.
- Hardened permission validation org: `astrosoft`.
- Hardened permission deploy validation ID: `0AfdL00000ayY5JSAU`.
- Stable tests passed: 14.
- Stable tests failed: 0.
