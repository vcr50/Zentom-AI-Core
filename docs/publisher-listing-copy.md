# SentinelFlow Publisher Listing Copy

## 1. Product Name

Recommended listing name:

```text
SentinelFlow by Tomcodex
```

Alternative listing name:

```text
SentinelFlow - Powered by Zentom AI
```

## 2. Short Description

SentinelFlow is a Salesforce-native incident intelligence and governed automation app powered by Zentom AI. It detects operational issues, calculates risk, recommends safe runbooks, requires human approval for high-risk actions, executes approved Case creation, and records every decision in a replayable audit timeline.

## 3. Long Description

SentinelFlow helps Salesforce teams detect, understand, and respond to operational incidents with governed AI assistance.

Powered by Zentom AI, SentinelFlow receives incident signals from Salesforce, analyzes risk and business impact, applies policy controls, recommends safe recovery runbooks, and writes the result back into Salesforce. Admins can approve or reject recommendations, execute safe actions such as Case creation, and review a full Replay Timeline showing what happened, why it happened, who approved it, and what action was taken.

The hosted beta runs in RULE mode for stability. Advanced local demos support Zentom Brain Engine with Ollama, pgvector memory, and RAG-based recommendations.

## 4. Key Features

- Salesforce incident intake
- Risk scoring
- Policy-based governance
- AI recommendation engine
- Runbook mapping
- Human approval workflow
- Safe Case creation
- Replay timeline
- SentinelFlow dashboard
- Org Health Score
- Hosted Zentom API integration

## 5. Business Value

SentinelFlow gives Salesforce operations teams a governed response layer for incidents that would otherwise be tracked manually across debug logs, Slack messages, tickets, and tribal knowledge.

Business benefits:

- Faster incident triage with structured risk scoring.
- Safer response workflows through policy evaluation and human approval.
- Better operational visibility through dashboards and replayable audit history.
- Reduced manual coordination for common Salesforce operational failures.
- A foundation for future AI-assisted remediation without allowing direct autonomous execution.

## 6. Target Users

- Salesforce Admins
- Salesforce Developers
- Sales Operations Teams
- RevOps Teams
- Support Operations Teams
- Enterprise Platform Teams

## 7. Use Cases

- Salesforce Flow failure triage
- Missing owner or assignment issue detection
- High-risk operational incident review
- Governed recommendation approval
- Safe Case creation for follow-up work
- Incident replay and audit review
- Salesforce operations dashboarding
- Beta validation of governed AI workflows

## 8. Security & Governance Summary

SentinelFlow does not allow AI to directly execute high-risk actions. Risk scoring, policy evaluation, human approval, and audit replay are built into the workflow.

The hosted beta uses RULE mode and does not expose local Ollama or LLM services publicly. High-risk or production-impacting actions require policy evaluation and human approval before execution.

Current beta security model:

- Hosted Zentom API runs in `AI_MODE=RULE`.
- No public Ollama endpoint is exposed.
- No direct LLM execution is used in the hosted beta.
- Production and high-risk actions are gated by policy decisions.
- Human approval is required before approved actions are executed.
- Replay timeline records incident intake, risk scoring, policy evaluation, recommendations, approvals, and execution events.

Future marketplace readiness work includes migration from Remote Site Setting to Named Credential, External Credential, and Permission Set Mapping.

## 9. Setup Summary

Typical beta setup:

1. Deploy the SentinelFlow beta package metadata.
2. Assign one of the included permission sets:
   - `SentinelFlow_Admin`
   - `SentinelFlow_Approver`
   - `SentinelFlow_Viewer`
3. Confirm `Zentom_Setting__mdt.Default.Base_URL__c` points to:

```text
https://zentom-api.onrender.com
```

4. Confirm Remote Site Setting `Zentom_API` points to:

```text
https://zentom-api.onrender.com
```

5. Open the SentinelFlow app.
6. Send a test incident.
7. Review the created incident, approval panel, replay timeline, and dashboard.

## 10. Support Contact / Placeholder

Support contact:

```text
support@tomcodex.example
```

Publisher:

```text
Tomcodex
```

Support documentation:

- `docs/install-guide.md`
- `docs/security-review-preparation.md`
- `docs/data-privacy-retention.md`
- `docs/salesforce-callout-security.md`

Note: Replace the placeholder support email before public marketplace submission.

## 11. Beta Limitations

- Hosted beta uses RULE mode only.
- Named Credential migration is planned before marketplace security review.
- Full autonomous remediation is not enabled.
- Local Ollama HYBRID mode is available only for advanced local demos.
- Hosted beta behavior is focused on Salesforce incident intake, risk scoring, policy evaluation, recommendation generation, human approval, Case creation, dashboarding, and replay timeline validation.
