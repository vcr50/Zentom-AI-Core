# SentinelFlow Beta Customer Pilot Selection

## 1. Purpose

This document starts Milestone 30 Beta Customer Pilot Execution and defines 30A Select pilot customer/org.

Goal:

```text
Select a real beta customer and Salesforce org for a controlled SentinelFlow pilot before any new feature expansion.
```

Locked beta rule:

```text
No new features now.
Run pilot.
Collect feedback.
Fix only P0/P1/P2 issues.
```

## 2. Pilot Objective

Pilot objective:

- Validate SentinelFlow in a real Salesforce customer environment.
- Confirm installation and configuration can be completed with customer admin involvement.
- Confirm hosted API, hosted DB, and Salesforce package behavior work in the selected org.
- Validate the `FLOW_FAILURE` scenario end to end.
- Confirm human approval and approved Case creation.
- Confirm Replay Timeline and dashboard value.
- Capture customer feedback.
- Identify only P0/P1/P2 fixes required before broader rollout.

The pilot is not a feature expansion phase.

## 3. Ideal Pilot Customer

Ideal pilot customer:

- Has an active Salesforce org.
- Has a Salesforce admin available.
- Can start in sandbox or developer org.
- Uses Salesforce Cases or can validate Case creation.
- Has an operational workflow where incident triage and approval are useful.
- Can join a guided demo and setup session.
- Can provide feedback within the pilot window.
- Understands the pilot is controlled and limited.

Best-fit roles:

- Salesforce Admin.
- Operations lead.
- Support/service owner.
- Automation owner.
- Security/governance stakeholder.
- Executive or technical sponsor.

## 4. Org Selection Criteria

Preferred org:

- Sandbox or developer org.
- Clean enough for package validation.
- Has Case object access.
- Allows outbound callouts to hosted Zentom API.
- Allows permission set assignment.
- Allows debug/error evidence capture if needed.

Hosted API:

```text
https://zentom-api.onrender.com
```

Default callout mode:

```text
REMOTE_SITE
```

Named Credential path:

```text
Validated, not default
```

Org selection checklist:

- [ ] Org type confirmed.
- [ ] Org Id captured.
- [ ] Admin contact confirmed.
- [ ] Approver contact confirmed.
- [ ] Viewer/stakeholder contact confirmed.
- [ ] Outbound callout policy confirmed.
- [ ] Case creation acceptable.
- [ ] Support/escalation contact confirmed.
- [ ] Customer accepts beta limitations.
- [ ] Customer accepts no secrets/sensitive data in test incident text.

## 5. Candidate Evaluation

Candidate tracker:

| Customer | Org type | Admin ready | Case validation | Callouts allowed | Pilot fit | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | Sandbox / Developer / Production | TBD | TBD | TBD | Strong / Medium / Weak | TBD |

Selection scoring:

| Criterion | Score 1-5 | Notes |
| --- | --- | --- |
| Salesforce admin availability | TBD | TBD |
| Safe sandbox/developer org available | TBD | TBD |
| Operational workflow fit | TBD | TBD |
| Case creation fit | TBD | TBD |
| Callout feasibility | TBD | TBD |
| Feedback availability | TBD | TBD |
| Low-risk pilot readiness | TBD | TBD |

Recommended selection threshold:

```text
Select a customer only if there is a clear admin owner, safe org, callout path, Case validation path, and feedback commitment.
```

## 6. Pilot Scope Confirmation

Included pilot scope:

- Guided demo.
- Package install/validation.
- Permission set assignment.
- Hosted API and DB health checks.
- Standard `FLOW_FAILURE` incident.
- Sentinel Incident write-back.
- Risk/policy/recommendation/runbook review.
- Human approval/rejection.
- Approved Case creation.
- Replay Timeline review.
- Dashboard + Org Health Score review.
- Feedback capture.
- P0/P1/P2 issue tracking.

Excluded pilot scope:

- New features.
- Full autonomous remediation.
- Hosted HYBRID Ollama.
- Production Agentforce integration.
- Major AI architecture changes.
- Large object model changes.
- Customer-specific integrations.

## 7. Pilot Readiness Decision

Decision options:

- Selected.
- Backup candidate.
- Needs more qualification.
- Not selected.

Decision record:

```text
Selected customer:
Selected org type:
Org Id:
Admin contact:
Approver contact:
Viewer/stakeholder:
Pilot owner:
Selection date:
Decision:
Notes:
```

No-go criteria:

- No Salesforce admin available.
- No safe org available.
- Outbound callouts blocked with no workaround.
- Case creation cannot be validated.
- Customer requires new features for pilot.
- Customer requires full autonomous remediation.
- Customer requires Agentforce production integration.
- Customer cannot provide feedback.
- Security/privacy concerns are unresolved.

## 8. Next Step

After pilot customer/org selection:

- Confirm pilot owner.
- Schedule pilot demo.
- Confirm target org and participants.
- Prepare install/validation checklist.
- Prepare standard `FLOW_FAILURE` scenario.
- Confirm support escalation path.

Milestone 30A result:

```text
30A - Select pilot customer/org: Complete when a pilot customer and Salesforce org are selected or a backup candidate is identified.
Next - 30B Schedule pilot demo
```
