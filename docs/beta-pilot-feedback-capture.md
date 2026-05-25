# SentinelFlow Beta Pilot Feedback Capture

## 1. Purpose

This document defines 30E Capture feedback for Milestone 30 Beta Customer Pilot Execution.

Goal:

```text
Capture pilot feedback from the beta customer in a structured way, separate active P0/P1/P2 fixes from future backlog ideas, and prepare inputs for the go/no-go decision.
```

Locked beta rule:

```text
No new features now.
Run pilot.
Collect feedback.
Fix only P0/P1/P2 issues.
```

## 2. Pilot Customer / Org

Pilot customer/org:

- Customer name: TBD.
- Salesforce org name: TBD.
- Org type: TBD.
- Pilot date: TBD.
- Feedback session date: TBD.
- Customer participants: TBD.
- Internal participants: TBD.
- Feedback owner: TBD.

## 3. Feedback Sources

Feedback sources:

- Live demo discussion.
- Scenario run notes.
- Customer admin feedback.
- Operations/support owner feedback.
- Security/privacy stakeholder feedback.
- Screenshots or recordings approved by the customer.
- Error logs and validation evidence.
- Follow-up email or call notes.

Privacy rule:

- Do not capture customer secrets, credentials, access tokens, sensitive case data, or personally sensitive production data in feedback notes.

## 4. Feedback Categories

Feedback categories:

- Onboarding and setup.
- Package install and permission assignment.
- Hosted API and callout reliability.
- `FLOW_FAILURE` incident creation.
- Risk and policy clarity.
- AI recommendation usefulness.
- Runbook clarity.
- Approval/rejection workflow.
- Case creation execution.
- Replay Timeline and audit confidence.
- Dashboard and Org Health Score usefulness.
- Error logging and supportability.
- Security/privacy concerns.
- Documentation gaps.
- Deferred feature requests.

## 5. Issue Severity

Severity levels:

- P0: Pilot cannot proceed, install is blocked, hosted API is unavailable, authentication fails, data privacy/security issue exists, or core incident creation cannot run.
- P1: Core workflow produces incorrect or unusable result, approval/execution fails, Case creation fails, replay/audit evidence is materially wrong, or customer trust is blocked.
- P2: Important usability, reliability, supportability, documentation, or onboarding issue that should be fixed before broader beta usage.
- P3: Useful improvement that does not block beta pilot continuation.
- P4: Future idea, feature request, or broader roadmap item.

Active beta fix rule:

- Only P0/P1/P2 issues are eligible for immediate beta fixes.
- P3/P4 items must be captured for backlog review, not implemented during the current beta pilot.

## 6. Customer Value Signals

Capture customer value signals:

- Does SentinelFlow make incident triage easier?
- Does the customer understand why human approval is required?
- Does the AI recommendation feel useful and trustworthy?
- Does the runbook match how the customer thinks about flow failures?
- Does Case creation fit the customer's support process?
- Does Replay Timeline improve auditability?
- Does Org Health Score help the customer understand operational posture?
- Would the customer continue the pilot after the demo?
- Would the customer recommend expanding to another org or workflow after beta stabilization?

Value score:

- 1: No clear value.
- 2: Limited value; major concerns.
- 3: Useful, but requires fixes.
- 4: Strong value with minor issues.
- 5: Strong value and ready for continued pilot.

Selected score: TBD.

## 7. Feedback Log

Feedback log:

| ID | Source | Category | Feedback | Severity | Owner | Status | Target Fix Milestone |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

Statuses:

- New.
- Under Review.
- Accepted.
- Rejected.
- Fix In Progress.
- Fix Validated.
- Deferred.
- Closed.

## 8. Security / Privacy Feedback

Security/privacy feedback:

- Any concerns about hosted API callouts: TBD.
- Any concerns about shared secret authentication: TBD.
- Any concerns about customer data in incident text: TBD.
- Any concerns about logs or audit records: TBD.
- Any concerns about AI recommendation content: TBD.
- Any requested documentation or evidence: TBD.

Escalation rule:

- Any confirmed data privacy or security issue is P0/P1 until triaged and mitigated.

## 9. Onboarding Friction

Onboarding friction:

- Package install friction: TBD.
- Permission set friction: TBD.
- Remote Site / callout setup friction: TBD.
- API health check friction: TBD.
- Test incident setup friction: TBD.
- User navigation friction: TBD.
- Documentation gaps: TBD.

Recommended action:

- Classify setup blockers as P0/P1/P2 when they block pilot progression.
- Capture minor clarity issues as P2/P3 depending on impact.

## 10. Action Item Tracker

Action items:

| Action | Severity | Owner | Due Date | Evidence Needed | Status |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

Rules:

- P0/P1/P2 items require owner, target date, validation evidence, and customer follow-up plan.
- P3/P4 items require backlog label and should not interrupt the beta pilot.

## 11. Go/No-Go Inputs

Go/no-go inputs:

- Were all required pilot scenarios completed or blockers documented?
- Are any P0 issues open?
- Are any P1 issues open?
- Are P2 issues acceptable for continued beta with mitigation?
- Did the customer see clear product value?
- Did the customer raise security/privacy blockers?
- Is the customer willing to continue the pilot?
- Is the product ready for another beta customer/org?

Preliminary recommendation:

- Go: TBD.
- Conditional go: TBD.
- No-go: TBD.

## 12. Follow-Up Plan

Follow-up plan:

- Send pilot recap to customer.
- Confirm issue list and severity.
- Confirm P0/P1/P2 owners and target fix milestone.
- Confirm P3/P4 items are deferred to backlog.
- Schedule fix validation session if needed.
- Prepare inputs for 30F Go/No-Go decision.

Next milestone:

```text
30F - Go/No-Go decision
```

Exit criteria:

- Feedback sources reviewed.
- Customer value score captured.
- Issues categorized by severity.
- P0/P1/P2 action items assigned.
- P3/P4 backlog items separated.
- Security/privacy concerns documented.
- Go/no-go inputs prepared.
