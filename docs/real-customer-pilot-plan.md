# SentinelFlow Real Customer Pilot Plan

## 1. Purpose

This document defines the Milestone 27A pilot customer selection criteria and real customer pilot plan for SentinelFlow after Milestone 26 post-v1 stabilization and customer rollout planning.

Core goal:

```text
Validate SentinelFlow in a real Salesforce customer environment with a controlled, low-risk pilot before wider marketplace rollout.
```

The pilot should prove that SentinelFlow can be installed, configured, validated, supported, and trusted in a real customer Salesforce org while keeping scope narrow, execution human-approved, and rollback practical.

## 2. Pilot Goal

Pilot goal:

- Validate the end-to-end Salesforce-to-Zentom incident intelligence workflow in a real customer environment.
- Confirm customer admins can install and configure SentinelFlow with guided support.
- Confirm customer approvers understand and trust policy decisions, recommendations, runbooks, and replay evidence.
- Confirm hosted API and hosted database behavior are stable enough for controlled customer use.
- Identify blockers before broader marketplace rollout.
- Capture practical customer feedback for v1.0.1 patch planning and future roadmap decisions.

The pilot is not a broad launch. It is a controlled validation with selected customers, limited users, clear support ownership, and explicit exit criteria.

## 3. Ideal Pilot Customer Profile

Ideal pilot customer:

- Uses Salesforce as an operational system of record.
- Has a Salesforce admin who can coordinate package installation and validation.
- Has a sandbox or developer org available for first validation.
- Uses Salesforce Cases or is comfortable validating safe Case creation after human approval.
- Has a clear operational workflow where incident triage, approval, auditability, or remediation recommendations are valuable.
- Can participate in scheduled onboarding, testing, and feedback sessions.
- Can provide logs, screenshots, Sentinel Incident ids, and validation notes when issues occur.
- Accepts that the pilot is controlled and may include known limitations.

Recommended pilot roles:

- Customer Salesforce Admin.
- Customer technical contact.
- Customer approver or operations lead.
- Customer read-only stakeholder or viewer.
- SentinelFlow support owner.
- SentinelFlow product owner.

Pilot org preference:

- Start in sandbox or developer org.
- Move to production only after explicit customer approval and successful sandbox validation.
- Avoid high-risk production workflows until approval, execution, replay, and rollback behavior are verified.

## 4. Customer Selection Criteria

Required selection criteria:

- Customer has an active Salesforce org and admin access.
- Customer can install or coordinate installation of SentinelFlow package metadata.
- Customer can assign required permission sets.
- Customer can allow outbound callouts to the hosted Zentom API.
- Customer can participate in a guided onboarding session.
- Customer agrees to run a controlled validation scenario before any production use.
- Customer understands human approval remains required before execution.
- Customer agrees not to submit sensitive personal data, regulated data, secrets, or credentials in test incident descriptions.
- Customer has an identified escalation contact.

Preferred selection criteria:

- Customer has a sandbox available.
- Customer has an existing incident, support, operations, or automation review workflow.
- Customer can validate Salesforce Case creation.
- Customer has users who can test Admin, Approver, and Viewer roles.
- Customer can provide structured feedback within the pilot timeline.
- Customer is willing to join a pilot review call after validation.

Exclusion criteria:

- Customer requires full autonomous remediation for pilot success.
- Customer requires Agentforce production integration as a pilot dependency.
- Customer requires hosted HYBRID Ollama or major AI architecture changes.
- Customer cannot support Salesforce package installation or permission assignment.
- Customer cannot allow hosted API callouts.
- Customer requires large object model changes before validation.
- Customer cannot provide a safe test scenario.

## 5. Pilot Scope

Included pilot scope:

- Guided customer onboarding.
- Salesforce package installation or deployment validation.
- Permission assignment for Admin, Approver, and Viewer roles.
- Hosted Zentom API configuration.
- Remote Site or Named Credential validation, depending on customer setup.
- Hosted API health check.
- Hosted DB health check.
- Standard `FLOW_FAILURE` test incident.
- Sentinel Incident write-back validation.
- Risk score, policy decision, recommendation, and runbook validation.
- Human approval and rejection validation.
- Approved Case creation validation.
- Replay Timeline validation.
- Dashboard and Org Health Score validation.
- Support escalation and feedback capture.

Out of pilot scope:

- Major AI architecture changes.
- Hosted HYBRID Ollama.
- Agentforce production integration.
- Full autonomous remediation.
- Large object model changes.
- Broad marketplace rollout.
- Custom customer-specific integrations.
- Production rollout without prior validation and explicit customer approval.

## 6. Pilot Timeline

Recommended timeline:

| Phase | Target duration | Outcome |
| --- | --- | --- |
| Customer selection | 1 week | Pilot customer meets required selection criteria. |
| Pre-onboarding | 2-3 business days | Org, contacts, access, support path, and pilot scope confirmed. |
| Guided onboarding | 1 session | Package, permissions, API configuration, and health checks validated. |
| Workflow validation | 1-2 sessions | Test incident, approval, execution, replay, and dashboard validated. |
| Observation period | 1-2 weeks | Customer uses controlled scenarios and reports issues or feedback. |
| Pilot review | 1 session | Results, blockers, patch candidates, and go/no-go decision documented. |

Timeline rules:

- P0/P1 issues pause pilot expansion until resolved or accepted as risk.
- Production use should wait until sandbox/developer validation passes unless the customer explicitly approves a production-first pilot.
- Pilot feedback should be reviewed at least weekly during the observation period.
- Patch candidates should be linked to v1.0.1 planning when appropriate.

## 7. Success Criteria

Pilot success criteria:

- Customer completes onboarding with guided support.
- SentinelFlow package installs or validates without unresolved blockers.
- Required permission sets are assigned and role behavior is understood.
- Hosted API health check passes.
- Hosted DB health check passes.
- Standard test incident is submitted successfully.
- Sentinel Incident write-back succeeds.
- Risk score, policy decision, recommendation, and runbook are populated as expected.
- Customer approver understands the approval decision and recommendation.
- Approval and rejection workflows work as expected.
- Approved Case creation works in the agreed validation org.
- Replay Timeline shows required audit events in order.
- Dashboard and Org Health Score load for expected users.
- No secrets, credentials, or prohibited sensitive data are exposed in logs or replay evidence.
- Customer feedback is captured and triaged.
- No unresolved P0/P1 blockers remain at pilot close.

Customer trust signals:

- Customer can explain what SentinelFlow did and why.
- Customer trusts the Replay Timeline as audit evidence.
- Customer understands when human approval is required.
- Customer understands support and escalation paths.
- Customer can identify at least one real workflow where SentinelFlow is useful.

## 8. Support Process

Pilot support process:

- Assign one SentinelFlow support owner for the customer.
- Confirm customer admin and escalation contacts before onboarding.
- Use the support SLA / response policy for severity handling.
- Route production-impacting issues through production issue tracking.
- Route repeated usability or documentation issues through feedback-to-roadmap review.
- Route patch-worthy fixes into v1.0.1 patch planning.
- Capture evidence without storing secrets or prohibited sensitive data.

Required support evidence:

- Customer org type.
- Salesforce Org Id.
- Target release or commit.
- Callout mode.
- Hosted API target.
- Sentinel Incident id, if applicable.
- `Sentinel_Error_Log__c` id, if applicable.
- Hosted Zentom incident id, if applicable.
- Error message or screenshot, sanitized where needed.
- Replay Timeline event list, if applicable.
- Steps to reproduce.
- Business impact.

Severity handling:

- P0: pilot-blocking outage, security/privacy issue, unsafe execution, or approval bypass.
- P1: core workflow blocker with no reasonable workaround.
- P2: onboarding, documentation, replay, dashboard, or support issue that slows adoption.
- P3: enhancement or future roadmap request.
- P4: backlog idea or non-blocking preference.

## 9. Feedback Process

Feedback sources:

- Guided onboarding notes.
- Customer pilot review calls.
- Support tickets or email.
- Customer screenshots and validation notes.
- Sentinel Incident records.
- Replay Timeline evidence.
- `Sentinel_Error_Log__c` records.
- Hosted API logs.
- Usage and adoption metrics.

Feedback categories:

- Bug.
- Onboarding issue.
- Documentation gap.
- Usability issue.
- Security or privacy concern.
- Performance or reliability issue.
- AI recommendation quality issue.
- Feature request.
- Future integration request.

Feedback review rules:

- P0/P1 feedback receives immediate review.
- P2 feedback is reviewed during weekly pilot review.
- Security or privacy feedback is escalated immediately.
- Repeated onboarding or documentation issues should become v1.0.1 candidates when low risk.
- Major roadmap requests should not expand pilot scope unless approved separately.
- Every accepted patch candidate should have validation requirements and a rollback note.

Feedback record template:

```text
Customer:
Org type:
Date:
Reporter:
Category:
Severity:
Summary:
Evidence:
Impact:
Decision:
Owner:
Target release:
Validation needed:
Customer follow-up:
```

## 10. Pilot Exit Criteria

Pilot may close successfully when:

- Required pilot scenarios are complete.
- Customer onboarding evidence is captured.
- Hosted API and hosted DB validation pass.
- Package install or deployment validation has no unresolved blockers.
- Approval, execution, replay, dashboard, and support workflows are validated.
- Customer feedback has been reviewed and triaged.
- P0/P1 issues are resolved, hotfixed, or formally accepted as risk.
- v1.0.1 patch candidates are identified.
- Future roadmap items are separated from patch scope.
- Customer communication summary is complete.
- Decision is recorded: proceed to broader pilot, extend pilot, patch before expanding, or pause rollout.

No-go criteria:

- Unresolved package install blocker.
- Hosted API or hosted DB failure without accepted workaround.
- Callout/authentication failure without accepted workaround.
- Approval or execution defect.
- Replay/audit defect that undermines trust.
- Security or data privacy issue.
- Customer cannot complete onboarding.
- Customer does not trust the workflow enough for controlled use.

Milestone 27A result:

```text
27A - Pilot Customer Selection Criteria: Complete
Next - 27B Pilot Onboarding Runbook
```
