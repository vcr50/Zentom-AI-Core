# SentinelFlow AppExchange / AgentExchange Submission Checklist

## 1. Purpose

This checklist defines Milestone 28A for final AppExchange / AgentExchange submission readiness.

Goal:

```text
Confirm that SentinelFlow has the required package, listing, demo, security, install validation, support, and rollback evidence before final marketplace submission.
```

This checklist is a submission control document. It should be reviewed before any final AppExchange, AgentExchange, Salesforce security review, or marketplace readiness submission step.

## 2. Submission Scope

Submission target:

- AppExchange / AgentExchange readiness.
- Salesforce package security review readiness.
- Final listing and demo asset readiness.
- Final install/test org validation.
- Controlled marketplace rollout after real customer pilot preparation.

Included:

- Stable SentinelFlow Salesforce package components.
- Hosted Zentom API integration.
- Hosted PostgreSQL backend evidence.
- Human approval workflow.
- Safe Case creation after approval.
- Replay Timeline auditability.
- Dashboard and Org Health Score.
- Support, privacy, install, and troubleshooting documentation.

Excluded unless separately approved:

- Hosted HYBRID Ollama.
- Full autonomous remediation.
- Agentforce production integration.
- Major AI architecture changes.
- Large object model changes.
- Experimental metadata or unstable package drift.

## 3. Final Package Checklist

Package readiness:

- [ ] Stable package manifest identified.
- [ ] Package manifest excludes experimental Agentforce metadata.
- [ ] Package manifest excludes temporary files and unstable metadata.
- [ ] Apex classes included and validated.
- [ ] Lightning Web Components included and validated.
- [ ] Custom objects included and validated.
- [ ] Custom metadata included and validated.
- [ ] Permission sets included and validated.
- [ ] App, tabs, layouts, and list views included and validated.
- [ ] Remote Site fallback metadata included where required.
- [ ] Named Credential path documented and validated where required.
- [ ] No hardcoded secrets in package metadata.
- [ ] No local-only URLs in package metadata.
- [ ] No public Ollama endpoint exposed.

Required package evidence:

- Latest validation org:
- Latest deploy/validation id:
- Tests passing:
- Tests failing:
- Package manifest path:
- Release candidate or target commit:

## 4. Install And Test Org Checklist

Install readiness:

- [ ] Fresh org or clean validation org identified.
- [ ] Package installs or deploys cleanly.
- [ ] Required permission sets assign correctly:
  - `SentinelFlow_Admin`
  - `SentinelFlow_Approver`
  - `SentinelFlow_Viewer`
- [ ] SentinelFlow app opens.
- [ ] Dashboard loads.
- [ ] Approval panel loads.
- [ ] Replay Timeline loads.
- [ ] `Zentom_Setting__mdt.Default.Base_URL__c` is correct.
- [ ] Remote Site or Named Credential mode is verified.
- [ ] Hosted API health passes.
- [ ] Hosted DB health passes.
- [ ] Test incident creates a Sentinel Incident.
- [ ] Risk, policy, recommendation, and runbook fields populate.
- [ ] Approval and rejection work.
- [ ] Approved Case creation works.
- [ ] Replay Timeline includes expected events.
- [ ] Viewer role remains read-only.

Install evidence:

- Org type:
- Org alias/name:
- Org Id:
- Deploy/installation id:
- Test result:
- Validation date:
- Evidence owner:

## 5. Security Review Checklist

Security review evidence:

- [ ] Security review evidence pack complete.
- [ ] CRUD/FLS and sharing review complete.
- [ ] Apex/LWC security scan checklist complete.
- [ ] External callout and Named Credential decision documented.
- [ ] Data privacy and retention documentation complete.
- [ ] Salesforce callout security documentation complete.
- [ ] API authentication/shared-secret evidence documented.
- [ ] Error logging avoids storing secrets.
- [ ] Replay evidence avoids exposing secrets.
- [ ] Permission sets follow least-privilege expectations.
- [ ] Human approval boundary documented.
- [ ] Full autonomous remediation excluded from submission.
- [ ] Hosted HYBRID Ollama excluded from hosted submission.
- [ ] Agentforce production integration excluded unless separately reviewed.
- [ ] Known gaps and mitigations documented.

Security evidence references:

- `docs/security-review-evidence-pack.md`
- `docs/crud-fls-sharing-review.md`
- `docs/apex-lwc-security-scan-checklist.md`
- `docs/security-review-final-checklist.md`
- `docs/salesforce-callout-security.md`
- `docs/data-privacy-retention.md`
- `docs/production-issue-tracking.md`
- `docs/support-troubleshooting-guide.md`

## 6. Listing Asset Checklist

Listing assets:

- [ ] Product name finalized.
- [ ] Short description finalized.
- [ ] Long description finalized.
- [ ] Feature list finalized.
- [ ] Business value copy finalized.
- [ ] Target user/customer profile finalized.
- [ ] Setup summary finalized.
- [ ] Support contact/path finalized.
- [ ] Privacy and security summary finalized.
- [ ] Known limitations documented.
- [ ] Screenshots selected.
- [ ] Demo script finalized.
- [ ] Customer-facing pilot message reviewed for consistency.

Listing evidence references:

- `docs/publisher-listing-copy.md`
- `docs/pilot-outreach-pack.md`
- `docs/customer-facing-pilot-outreach-message.md`
- `docs/pilot-demo-script.md`

## 7. Screenshot And Demo Checklist

Screenshots to prepare:

- [ ] SentinelFlow app landing/dashboard.
- [ ] Sentinel Incident detail.
- [ ] Approval panel.
- [ ] Policy decision / recommendation view.
- [ ] Created Case from approved action.
- [ ] Replay Timeline.
- [ ] Dashboard + Org Health Score.
- [ ] Permission or setup view, if useful.

Demo readiness:

- [ ] 30-minute demo script finalized.
- [ ] Standard `FLOW_FAILURE` demo scenario validated.
- [ ] Expected risk score `95` confirmed.
- [ ] Expected risk level `CRITICAL` confirmed.
- [ ] Expected policy `HUMAN_APPROVAL_REQUIRED` confirmed.
- [ ] Expected runbook `FLOW_FAILURE_BASIC_RECOVERY` confirmed.
- [ ] Approved action `CREATE_CASE` confirmed.
- [ ] Replay events confirmed from intake through Case creation.
- [ ] Demo org cleaned of confusing test data.
- [ ] No secrets or sensitive data visible in screenshots or demo data.

Demo reference:

- `docs/pilot-demo-script.md`

## 8. Support And Operations Checklist

Support readiness:

- [ ] Support SLA / response policy complete.
- [ ] Support troubleshooting guide complete.
- [ ] Production issue tracking process complete.
- [ ] Customer onboarding checklist complete.
- [ ] Usage monitoring and adoption metrics plan complete.
- [ ] Feedback-to-roadmap process complete.
- [ ] v1.0.1 patch planning complete.
- [ ] Pilot feedback review template complete.
- [ ] Pilot success report template complete.

Support evidence references:

- `docs/support-sla-response-policy.md`
- `docs/support-troubleshooting-guide.md`
- `docs/production-issue-tracking.md`
- `docs/customer-onboarding-checklist.md`
- `docs/usage-monitoring-adoption-metrics.md`
- `docs/feedback-to-roadmap-process.md`
- `docs/v1.0.1-patch-planning.md`
- `docs/pilot-feedback-review-template.md`
- `docs/pilot-success-report.md`

## 9. Hosted API Checklist

Hosted API readiness:

- [ ] Hosted API base URL confirmed.
- [ ] Root health endpoint passes.
- [ ] `/api/health/db` passes.
- [ ] PostgreSQL database configured.
- [ ] Required tables present.
- [ ] pgvector enabled.
- [ ] Incident receive endpoint works.
- [ ] API authentication behavior validated.
- [ ] Unauthorized requests return expected 401 behavior.
- [ ] Hosted error logging works without storing secrets.
- [ ] Render cold-start/uptime strategy documented.
- [ ] Production hosting limitations documented.

Current hosted API:

```text
https://zentom-api.onrender.com
```

Hosted API evidence references:

- `docs/monitoring-error-alerts.md`
- `docs/backup-recovery-plan.md`
- `docs/render-uptime-strategy.md`
- `docs/security-review-evidence-pack.md`

## 10. Customer Pilot Evidence Checklist

Pilot readiness evidence:

- [ ] Real customer pilot plan complete.
- [ ] Pilot outreach pack complete.
- [ ] Customer-facing pilot message complete.
- [ ] Pilot demo script complete.
- [ ] Pilot feedback review template complete.
- [ ] Pilot success report template complete.
- [ ] Pilot success report populated after real customer execution, when available.
- [ ] Pilot blockers mapped to v1.0.1 or roadmap.
- [ ] Go/no-go decision recorded after pilot execution, when available.

Pilot evidence references:

- `docs/real-customer-pilot-plan.md`
- `docs/pilot-outreach-pack.md`
- `docs/customer-facing-pilot-outreach-message.md`
- `docs/pilot-demo-script.md`
- `docs/pilot-feedback-review-template.md`
- `docs/pilot-success-report.md`

## 11. Release And Rollback Checklist

Release readiness:

- [ ] Target release version identified.
- [ ] Target commit or tag identified.
- [ ] Release notes prepared.
- [ ] Known limitations documented.
- [ ] Customer communication prepared.
- [ ] Support owner assigned.
- [ ] Submission owner assigned.
- [ ] Final go/no-go decision recorded.

Rollback readiness:

- [ ] Last known good package manifest identified.
- [ ] Last known good hosted API version identified.
- [ ] Hosted API environment configuration documented.
- [ ] Salesforce callout fallback documented.
- [ ] Remote Site fallback documented.
- [ ] Named Credential path documented.
- [ ] Documentation rollback path documented.
- [ ] Customer workaround path documented.

## 12. Submission Go/No-Go Criteria

Go criteria:

- [ ] Package validates cleanly.
- [ ] Install/test org validation passes.
- [ ] Hosted API and DB health pass.
- [ ] Security review evidence is complete.
- [ ] Listing copy and assets are ready.
- [ ] Demo script and screenshots are ready.
- [ ] Support and escalation path is ready.
- [ ] No unresolved P0/P1 blockers remain.
- [ ] No unresolved security/privacy concerns remain.
- [ ] Known limitations are documented honestly.
- [ ] Submission owner approves.

No-go criteria:

- Package install blocker.
- Hosted API failure without accepted workaround.
- Hosted DB failure without accepted workaround.
- Callout/authentication failure.
- Approval or execution defect.
- Replay/audit defect that undermines trust.
- Secret exposure or data privacy issue.
- Missing required listing/security asset.
- Unsupported claim in listing copy or demo.
- Unresolved P0/P1 pilot blocker.

## 13. Final Sign-Off

Submission owner:

```text
Name:
Date:
Decision: Go / Conditional go / No-go
Notes:
```

Security owner:

```text
Name:
Date:
Decision: Go / Conditional go / No-go
Notes:
```

Product owner:

```text
Name:
Date:
Decision: Go / Conditional go / No-go
Notes:
```

Milestone 28A result:

```text
28A - Final Submission Checklist: Complete
Next - 28B Final Listing Assets
```
