# SentinelFlow Security Review Final Checklist

## 1. Purpose

This checklist defines the final security-review readiness checks for SentinelFlow v1.0 preparation.

The goal is to confirm that the Salesforce package, hosted Zentom API, hosted database, documentation, and AI governance controls are ready for a formal marketplace/security-review path or have clearly documented gaps before submission.

## 2. Package Readiness

Checklist:

- [ ] Beta manifest validates.
- [ ] Fresh scratch org deploy passed.
- [ ] Stable tests pass.
- [ ] No experimental metadata included.
- [ ] Package includes only stable SentinelFlow components.
- [ ] Permission sets are included and validated.
- [ ] Remote Site Setting is documented as beta-only.
- [ ] Named Credential migration plan exists.
- [ ] Install guide is current.
- [ ] Support/troubleshooting guide is current.

Known current state:

- Beta manifest has been validated.
- Fresh-org validation has passed.
- Stable tests have passed.
- Experimental Agentforce/old metadata is excluded from the beta manifest.

## 3. Apex Security Checklist

Checklist:

- [ ] Uses `with sharing` where appropriate.
- [ ] Tests cover callout behavior.
- [ ] No hardcoded secrets.
- [ ] No unsafe dynamic SOQL.
- [ ] No direct autonomous execution without approval.
- [ ] Callout errors are handled safely.
- [ ] JSON parsing handles missing/invalid fields safely.
- [ ] Approval and execution paths enforce allowed status transitions.
- [ ] Case creation requires approved incident state.
- [ ] Apex tests cover stable production workflows.

Key governance rule:

```text
SentinelFlow must not execute high-risk actions directly without policy evaluation and human approval.
```

## 4. LWC Security Checklist

Checklist:

- [ ] No secrets in client-side code.
- [ ] Components respect permission sets.
- [ ] Approval/execution buttons hidden unless allowed.
- [ ] LWC calls Apex controllers rather than external services directly.
- [ ] Error messages do not expose secrets or internal credentials.
- [ ] Viewer role remains read-only.
- [ ] Admin/Approver actions are scoped to intended workflows.
- [ ] Browser console does not expose sensitive payloads.

Relevant components:

- `zentomApprovalPanel`
- `zentomReplayTimeline`
- `zentomDashboard`

## 5. Salesforce Object/FLS/CRUD Checklist

Checklist:

- [ ] Object permissions are defined for SentinelFlow roles.
- [ ] Field access matches role expectations.
- [ ] Viewer permission set is read-only.
- [ ] Approver permission set can approve/reject and execute allowed actions.
- [ ] Admin permission set has full beta administration access.
- [ ] Sensitive fields are not exposed unnecessarily.
- [ ] Created Case references are accessible only to permitted users.
- [ ] Audit/replay records are readable by intended roles.

Objects:

- `Sentinel_Incident__c`
- `Sentinel_Audit_Log__c`
- `Zentom_Policy_Decision__c`
- `Case`

Permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

## 6. External Callout Checklist

Checklist:

- [ ] Remote Site is used for beta.
- [ ] Named Credential migration planned for production/security review.
- [ ] Hosted API URL is documented.
- [ ] Callout endpoint is HTTPS.
- [ ] No API keys are hardcoded in Apex.
- [ ] Callout timeout/failure behavior is documented.
- [ ] Hosted API health endpoint is documented.
- [ ] Hosted DB health endpoint is documented.

Current beta callout:

```text
https://zentom-api.onrender.com/api/incidents/receive
```

Current beta base URL:

```text
https://zentom-api.onrender.com
```

Target production callout:

```text
callout:Zentom_API/api/incidents/receive
```

## 7. Data Privacy Checklist

Checklist:

- [ ] Privacy documentation complete.
- [ ] Retention documentation complete.
- [ ] Hosted DB documented.
- [ ] Customer deletion/export process documented.
- [ ] Data sent to Zentom API documented.
- [ ] Data stored in Salesforce documented.
- [ ] Data stored in hosted PostgreSQL documented.
- [ ] AI/LLM data handling documented.
- [ ] Memory/RAG data handling documented.
- [ ] Dataset export behavior documented.

Relevant document:

```text
docs/data-privacy-retention.md
```

## 8. AI Governance Checklist

Checklist:

- [ ] Hosted beta uses `AI_MODE=RULE`.
- [ ] Local Ollama is not public.
- [ ] AI cannot directly execute high-risk actions.
- [ ] Risk, policy, approval, and replay are enforced.
- [ ] Human approval is required for production/high-risk actions.
- [ ] Runbook selection is visible to users.
- [ ] Replay timeline records decisions and actions.
- [ ] Advanced local HYBRID mode is documented as local demo only.

Governance posture:

```text
Hosted beta = RULE mode
Advanced local demo = HYBRID + Ollama + pgvector
Production high-risk execution = policy gated + human approved
```

## 9. Hosted API Security Checklist

Checklist:

- [ ] `/` endpoint works.
- [ ] `/api/health/db` works.
- [ ] `DATABASE_URL` is not committed.
- [ ] Environment variables are managed in Render.
- [ ] Hosted API uses HTTPS.
- [ ] Hosted API runs in `AI_MODE=RULE`.
- [ ] No public Ollama endpoint is exposed.
- [ ] Secrets are not stored in source control.
- [ ] Render deployment process is documented.
- [ ] Error responses do not expose secrets.

Required health endpoints:

```text
GET https://zentom-api.onrender.com/
GET https://zentom-api.onrender.com/api/health/db
```

## 10. Database Security Checklist

Checklist:

- [ ] Hosted database is PostgreSQL.
- [ ] `pgvector` availability is documented.
- [ ] `DATABASE_URL` is stored only as a hosted environment variable.
- [ ] Database backup plan exists.
- [ ] Restore plan exists.
- [ ] Data stored in hosted DB is documented.
- [ ] Deletion/export process is documented.
- [ ] Production access to hosted DB is limited.
- [ ] Backup/export does not expose unnecessary data.

Relevant document:

```text
docs/backup-recovery-plan.md
```

## 11. Documentation Checklist

Checklist:

- [ ] Security review preparation doc complete.
- [ ] Data privacy and retention doc complete.
- [ ] Install guide complete.
- [ ] Salesforce callout security doc complete.
- [ ] Hosted AI strategy doc complete.
- [ ] Support/troubleshooting guide complete.
- [ ] Marketplace readiness wrap-up complete.
- [ ] Private beta plan complete.
- [ ] Beta testing scenarios complete.
- [ ] Feedback capture plan complete.
- [ ] Bug fix sprint plan complete.
- [ ] Beta release notes complete.
- [ ] Production readiness plan complete.
- [ ] Monitoring/error alerts plan complete.
- [ ] Backup/recovery plan complete.
- [ ] Named Credential migration plan complete.

## 12. Known Gaps Before Submission

Known gaps:

- Named Credential not implemented yet.
- Render free tier cold start.
- Full security scan not yet submitted.

Additional v1.0 review items:

- Final CRUD/FLS review should be performed before formal submission.
- Final Apex security scan should be performed before formal submission.
- Named Credential implementation should be validated in a clean org.
- External Credential and Permission Set Mapping should be finalized.
- Support contact placeholder should be replaced before public listing.

## 13. Final Go/No-Go Criteria

Go criteria:

- [ ] No open P0 issues.
- [ ] No open P1 issues.
- [ ] P2 issues fixed or accepted with documented workaround.
- [ ] Beta manifest validates.
- [ ] Fresh-org deploy passes.
- [ ] Stable tests pass.
- [ ] Hosted API health passes.
- [ ] Hosted DB health passes.
- [ ] Salesforce incident workflow passes.
- [ ] Approval, rejection, Case creation, replay timeline, and dashboard pass.
- [ ] Security/privacy/install/support docs are complete.
- [ ] Known gaps are accepted or closed.

No-go criteria:

- [ ] Package does not deploy cleanly.
- [ ] Stable tests fail.
- [ ] Hosted API is unavailable.
- [ ] Hosted DB is unavailable.
- [ ] Incident write-back fails.
- [ ] Approval or execution bypasses required governance.
- [ ] Secrets are found in source control.
- [ ] Data privacy documentation is incomplete.
- [ ] Named Credential/security-review path is not documented.
