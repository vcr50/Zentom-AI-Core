# Data Privacy and Retention

## 1. Purpose

This document describes what data SentinelFlow collects, where it is stored, how it is retained, who can access it, and how customers can export or delete it during beta.

Current hosted beta mode:

```text
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_MODEL=zentom-rule-v1
```

The hosted beta does not use a paid third-party LLM and does not expose Ollama publicly.

## 2. Data Flow Overview

Current beta flow:

```text
Salesforce
-> Hosted Zentom API
-> Hosted PostgreSQL
-> Risk + policy + recommendation
-> Salesforce write-back
-> Human approval
-> Case creation / replay timeline
```

Salesforce remains the workflow system of record. The hosted Zentom API stores incident processing data needed for beta analysis, rule-based recommendations, memory, and future dataset export.

## 3. Data Sent From Salesforce To Zentom API

SentinelFlow sends a minimal incident payload to the hosted Zentom API:

- Org Id
- Incident type
- Source
- Environment
- Error message
- Confidence
- Action type

Example payload:

```json
{
  "orgId": "Salesforce organization id",
  "incidentType": "FLOW_FAILURE",
  "source": "Salesforce Flow",
  "environment": "production",
  "errorMessage": "Flow failed because owner field is null and missing account owner",
  "confidence": 85,
  "actionType": "CREATE_CASE"
}
```

No Salesforce password, session token, OAuth secret, API secret, or Named Credential secret is sent to Zentom API.

Customers should avoid sending sensitive personal data or regulated data in free-form error messages.

## 4. Data Stored In Salesforce

Salesforce stores SentinelFlow workflow records, including:

- Sentinel Incident records
- Audit logs
- Policy decisions
- Approval status
- Execution status
- Created Case reference
- Replay timeline
- Risk score and risk level
- Recommendation summary, root cause, and recommended action
- Runbook metadata used by the incident workflow

Primary Salesforce objects:

- `Sentinel_Incident__c`
- `Sentinel_Audit_Log__c`
- `Zentom_Policy_Decision__c`
- `Case`

## 5. Data Stored In Hosted PostgreSQL

The hosted Zentom API stores processing data in hosted PostgreSQL.

Stored hosted DB data includes:

- Incident payload
- Risk score
- Policy decision
- AI recommendation
- Runbook key
- Memory entries
- Dataset export entries

Primary hosted tables:

- `incidents`
- `risk_scores`
- `policy_decisions`
- `ai_recommendations`
- `memory_entries`

`pgvector` is enabled for the hosted database. Hosted beta still remains in `AI_MODE=RULE`.

## 6. AI / LLM Data Handling

Hosted beta:

- Uses `AI_MODE=RULE`.
- Does not call a paid third-party LLM.
- Does not expose Ollama publicly.
- Does not run direct hosted LLM reasoning.
- Does not allow the AI model to execute actions directly.

SentinelFlow does not allow the AI model to execute actions directly. All production/high-risk actions require policy evaluation and human approval before execution.

Local advanced demo mode may use Ollama locally with `phi3:mini` and `all-minilm`, but this is not exposed as a public hosted endpoint.

## 7. Memory And RAG Data Handling

SentinelFlow memory entries may store incident-derived operational knowledge, including:

- Incident type
- Summary
- Root cause
- Recommended action
- Runbook key
- Risk level
- Policy decision
- Execution status
- Outcome status
- Embedding text
- Embedding vector where available

Hosted beta memory exists to support future retrieval and dataset generation. Hosted beta does not expose a public Ollama endpoint and does not rely on hosted LLM execution.

Dataset exports are generated manually through API endpoints and are not shared externally by default.

## 8. Data Retention Policy

Beta retention:

- Incident records: retained until manually deleted by customer/admin.
- Hosted DB incident data: retained during beta unless deletion is requested.
- Audit/replay logs: retained for traceability.
- Dataset exports: generated manually and not shared externally by default.

Recommended future production policy:

- Define customer-configurable retention windows.
- Support retention controls per data type.
- Add scheduled purge jobs for hosted DB data.
- Document retention commitments in customer-facing terms.

## 9. Data Deletion Policy

Salesforce data deletion:

- Customer admins can delete Salesforce records using standard Salesforce data management tools.
- Deleting a SentinelFlow incident should be handled carefully because audit and policy records may be required for operational traceability.

Hosted DB deletion:

- During beta, hosted DB deletion is handled by request.
- Deletion requests should include the Salesforce org id and any known Zentom hosted incident ids.
- Deletion should cover related incident, risk, policy, recommendation, and memory records where applicable.

Future production deletion:

- Provide documented deletion request workflow.
- Add admin-accessible delete/export tooling where appropriate.
- Add tenant-scoped deletion safeguards.

## 10. Data Export Policy

Salesforce export:

- Customers can export Salesforce records through standard Salesforce reports, data export, APIs, or admin tooling.

Zentom dataset export:

- Dataset exports are generated manually.
- Supported training-oriented formats include Alpaca JSON and JSONL.
- Dataset exports are intended for customer-controlled future fine-tuning experiments.
- Dataset exports are not shared externally by default.

Customers should review exported data before using it for model training.

## 11. Access Control

Salesforce access is controlled by permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

Access model:

- Admin: full beta package access.
- Approver: approval and execution workflow access.
- Viewer: read-only dashboard, incident, audit, policy, and replay access.

Hosted DB access should be limited to authorized maintainers and operational support users during beta.

## 12. Security Controls

Current controls:

- Hosted beta uses `AI_MODE=RULE`.
- No paid third-party LLM is used in hosted beta.
- No public Ollama endpoint exists.
- AI does not directly execute actions.
- Policy evaluation gates all recommendations.
- Production/high-risk actions require human approval.
- Case creation occurs only after approved execution.
- Replay timeline records key workflow events.
- Permission sets separate admin, approver, and viewer responsibilities.
- Remote Site Setting uses HTTPS base URL only.
- Named Credential migration is planned before marketplace security review.

## 13. Beta Limitations

Known beta limitations:

- Hosted API uses rule-based recommendations, not hosted LLM reasoning.
- Remote Site Setting is used for beta callouts.
- Named Credential and External Credential migration is planned before marketplace readiness.
- Hosted DB deletion/export workflows are operational/manual during beta.
- Customers should avoid sending sensitive personal data in incident error messages.
- Retention periods are not yet customer-configurable.

## 14. Future Improvements

Planned improvements:

- Named Credential + External Credential + Permission Set Mapping.
- Customer-facing data deletion request workflow.
- Tenant-scoped hosted data export.
- Configurable retention windows.
- Data minimization controls for error payloads.
- PII detection or masking before hosted API submission.
- Admin setup wizard for endpoint and privacy configuration.
- Marketplace security review documentation package.
