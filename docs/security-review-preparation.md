# Security Review Preparation

## 1. Product Overview

SentinelFlow is a Salesforce incident intelligence and approval workflow app powered by the Zentom API.

Current beta flow:

```text
Salesforce
-> Hosted Zentom API
-> Risk scoring
-> Policy decision
-> Rule-based recommendation
-> Salesforce write-back
-> Human approval
-> Safe execution / Case creation
-> Replay timeline
```

Hosted API:

```text
https://zentom-api.onrender.com
```

Hosted beta AI mode:

```text
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_MODEL=zentom-rule-v1
```

The hosted beta does not expose or call Ollama. Local Ollama usage remains limited to developer and advanced demo environments.

## 2. Salesforce Objects Used

Stable beta package objects:

- `Sentinel_Incident__c`
- `Sentinel_Audit_Log__c`
- `Zentom_Policy_Decision__c`
- `Zentom_Setting__mdt`
- `Zentom_Runbook__mdt`

Standard object used:

- `Case`

Primary object purposes:

- `Sentinel_Incident__c`: stores incident summary, risk, policy, AI recommendation, approval, runbook, and execution state.
- `Sentinel_Audit_Log__c`: stores replay timeline events for incident intake, risk scoring, policy evaluation, recommendation, approval, execution, and case creation.
- `Zentom_Policy_Decision__c`: stores policy decision context for a SentinelFlow incident.
- `Zentom_Setting__mdt`: stores non-secret beta configuration such as hosted API base URL.
- `Zentom_Runbook__mdt`: stores stable recovery runbook metadata.
- `Case`: created only after approved action execution.

## 3. Apex Classes Used

Stable beta runtime Apex:

- `ZentomIncidentClient`
- `ZentomApprovalController`
- `ZentomExecutionController`
- `ZentomReplayController`
- `ZentomDashboardController`
- `ZentomRunbookService`

Stable beta tests:

- `ZentomIncidentClientTest`
- `ZentomApprovalControllerTest`
- `ZentomExecutionControllerTest`
- `ZentomReplayControllerTest`
- `ZentomDashboardControllerTest`

## 4. LWC Components Used

Stable beta Lightning Web Components:

- `zentomApprovalPanel`
- `zentomReplayTimeline`
- `zentomDashboard`

## 5. External Callouts

Current beta callout:

```text
POST https://zentom-api.onrender.com/api/incidents/receive
```

Current Salesforce configuration:

```text
Remote Site Setting: Zentom_API
URL: https://zentom-api.onrender.com
```

`Zentom_Setting__mdt.Default.Base_URL__c` stores:

```text
https://zentom-api.onrender.com
```

The Remote Site Setting contains only the base URL. Apex appends `/api/incidents/receive`.

## 6. Data Sent To Zentom API

The beta Apex client sends a minimal incident payload:

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

No Salesforce session token, user password, API secret, OAuth secret, or Named Credential secret is sent.

Administrators should avoid sending sensitive personal data in `errorMessage`.

## 7. Data Stored In Salesforce

Salesforce stores:

- Incident type
- Source
- Environment
- Error message
- Risk score and risk level
- Policy decision and reason
- Recommendation summary
- Root cause
- Recommended action
- Confidence score
- Runbook key, title, description, and steps
- Approval status, approver, approval timestamp, and rejection reason
- Execution status, action, result, timestamp, and created Case reference
- Audit/replay timeline records

Salesforce remains the system of record for package workflow state.

## 8. Data Stored In Hosted DB

The hosted Zentom API uses hosted PostgreSQL.

Required hosted tables:

- `incidents`
- `risk_scores`
- `policy_decisions`
- `ai_recommendations`
- `memory_entries`

`pgvector` is enabled in the hosted database, but the hosted beta remains in `AI_MODE=RULE`. Vector/RAG and local model workflows are not exposed as public model endpoints.

## 9. Permission Sets

Beta package permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

Permission model:

- Admin: full access to stable SentinelFlow beta objects, app tabs, runtime Apex, and approved Case creation path.
- Approver: can review incidents, approve or reject recommendations, execute approved actions, view replay timeline, and create Cases through the execution flow.
- Viewer: read-only access to stable incident, audit, policy, dashboard, and replay data.

Legacy broad operator metadata is excluded from the beta manifest.

## 10. Remote Site Setting / Future Named Credential Plan

Beta uses Remote Site Setting for stability.

Marketplace/security-review target:

```text
Named Credential
External Credential
Permission Set Mapping
```

Future target callout:

```text
callout:Zentom_API/api/incidents/receive
```

Migration plan is documented in:

```text
docs/salesforce-callout-security.md
```

## 11. Security Controls

Current security controls:

- Hosted beta runs in `AI_MODE=RULE`.
- No Ollama endpoint is publicly exposed.
- No direct LLM execution happens in hosted beta.
- Policy decisions control execution behavior.
- Production and high-risk actions require human approval.
- Autonomous execution remains blocked outside experimental metadata.
- Case creation runs only through the approved execution path.
- Replay timeline records incident intake, risk scoring, policy evaluation, recommendation, approval, execution, and Case creation.
- Permission sets separate admin, approver, and viewer roles.
- Remote Site Setting uses HTTPS hosted API base URL only.
- No API keys or secrets are stored in Custom Metadata for the beta package.

## 12. Known Beta Limitations

Known beta limitations:

- Hosted beta uses `AI_MODE=RULE`, not hosted LLM reasoning.
- Ollama is local only and is not exposed publicly.
- Remote Site Setting is used for beta callouts.
- Named Credential, External Credential, and Permission Set Mapping are planned before marketplace security review.
- Hosted authentication is minimal for beta and must be hardened before public marketplace release.
- Customers should avoid sending sensitive personal data inside free-form error messages.

## 19A Status

Milestone 19A status:

```text
Security Review Preparation: Started
```

This document is the initial security-review preparation baseline for the SentinelFlow beta package.
