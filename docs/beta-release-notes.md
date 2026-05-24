# SentinelFlow Private Beta Release Notes

## Release Name

```text
SentinelFlow Private Beta v0.5.0
```

## Product Summary

SentinelFlow Private Beta v0.5.0 validates the hosted Salesforce-to-Zentom incident intelligence workflow. The beta includes Salesforce incident intake, hosted Zentom API analysis, risk scoring, policy evaluation, AI recommendation, runbook mapping, human approval, safe Case creation, dashboard visibility, Org Health Score, and replayable audit timeline.

## Included

- SentinelFlow Lightning App
- SentinelFlow Dashboard
- Sentinel Incident object
- Audit Log object
- Policy Decision object
- Hosted Zentom API integration
- Hosted PostgreSQL + pgvector backend
- RULE-mode AI recommendation
- Runbook Engine
- Human approval workflow
- Safe Case creation
- Replay Timeline
- Org Health Score
- Admin / Approver / Viewer permission sets

## Hosted Beta Configuration

Hosted API:

```text
https://zentom-api.onrender.com
```

Hosted AI mode:

```text
AI_MODE=RULE
```

Recommended Salesforce metadata:

```text
Zentom_Setting__mdt.Default.Base_URL__c = https://zentom-api.onrender.com
Remote Site Setting Zentom_API = https://zentom-api.onrender.com
```

## Validation Coverage

Private beta preparation includes:

- Fresh-org validation
- Stable SentinelFlow test validation
- Hosted API health verification
- Hosted PostgreSQL health verification
- Salesforce callout verification
- Incident write-back verification
- Approval and execution workflow verification
- Case Origin verification with `SentinelFlow`
- Replay timeline verification
- Dashboard verification
- Permission set hardening
- Security, privacy, install, support, feedback, and beta testing documentation

## Known Limitations

- Hosted beta uses `AI_MODE=RULE`.
- Local HYBRID Ollama mode is available only for advanced local demos.
- Render free tier may cold start.
- Named Credential migration is planned before marketplace security review.
- Full autonomous remediation is not enabled.
- Agentforce integration is planned later.

## Beta Testing References

- `docs/private-beta-plan.md`
- `docs/beta-testing-scenarios.md`
- `docs/beta-feedback-capture.md`
- `docs/beta-bug-fix-sprint.md`
- `docs/support-troubleshooting-guide.md`
- `docs/install-guide.md`

## Release Status

```text
SentinelFlow Private Beta v0.5.0 is ready for selected private beta validation.
```

Next phase:

```text
Milestone 21: Production v1.0 Preparation
```
