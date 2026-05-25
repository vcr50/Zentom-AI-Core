# SentinelFlow Pilot Feedback Triage

## 1. Purpose

This document defines 31A Pilot Feedback Triage for Milestone 31 v1.0.1 Patch / Pilot Feedback Fixes.

Goal:

```text
Review beta pilot feedback, identify only P0/P1/P2 issues eligible for v1.0.1 patch work, and defer all feature requests or low-priority improvements.
```

Patch rule:

```text
No new features.
Only pilot feedback fixes: P0/P1/P2.
```

## 2. Triage Inputs

Primary inputs:

- `docs/beta-pilot-success-report.md`.
- `docs/beta-pilot-feedback-capture.md`.
- `docs/beta-pilot-go-no-go-decision.md`.
- Scenario evidence from `docs/beta-pilot-scenario-run.md`.
- Install validation evidence from `docs/beta-pilot-install-validation.md`.
- Customer follow-up notes.
- Error logs and validation screenshots.

Do not use:

- New product ideas that were not raised by the pilot.
- General roadmap expansion requests.
- Agentforce expansion ideas.
- Major AI architecture changes.

## 3. Triage Scope

Included:

- Pilot blockers.
- Hosted API failures.
- Salesforce install/package blockers.
- Callout or authentication failures.
- Approval or execution defects.
- Case creation defects.
- Replay/audit defects.
- Dashboard or Org Health Score defects that materially affect pilot value.
- Error logging defects.
- Data privacy or security issues.
- Onboarding/documentation corrections that blocked or slowed pilot use.

Excluded:

- New features.
- Major AI architecture changes.
- Hosted HYBRID Ollama.
- Agentforce production integration.
- Full autonomous remediation.
- Large object model changes.
- P3/P4 enhancements unless reclassified as P0/P1/P2 with evidence.

## 4. Severity Rules

Severity rules:

- P0: Pilot cannot proceed, customer is blocked, package cannot install, hosted API is unavailable, authentication is broken, or data privacy/security issue is confirmed.
- P1: Core pilot workflow fails or produces materially incorrect result, including incident creation, risk/policy, approval/execution, Case creation, or replay/audit.
- P2: Important pilot usability, onboarding, documentation, reliability, dashboard, or supportability issue that should be fixed before controlled rollout.
- P3: Useful improvement, not required for patch.
- P4: Future feature idea or roadmap item.

Patch eligibility:

- P0: Eligible.
- P1: Eligible.
- P2: Eligible.
- P3: Not eligible.
- P4: Not eligible.

## 5. Triage Workflow

Workflow:

1. Collect all feedback and evidence from Milestone 30.
2. Remove duplicates.
3. Separate feature requests from defects or pilot blockers.
4. Assign severity using the rules above.
5. Confirm whether each P0/P1/P2 has evidence.
6. Assign an owner.
7. Define expected fix outcome.
8. Define validation evidence required.
9. Defer P3/P4 items to backlog.
10. Prepare approved P0/P1/P2 list for 31B P0/P1/P2 Fix Plan.

## 6. Triage Table

Triage table:

| ID | Source | Summary | Area | Severity | Patch Eligible | Owner | Evidence | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

Areas:

- Install/package.
- Permission/access.
- Hosted API.
- Hosted DB.
- Callout/authentication.
- Incident creation.
- Risk/policy.
- AI recommendation/runbook.
- Approval/rejection.
- Case creation.
- Replay/audit.
- Dashboard/Org Health Score.
- Error logging.
- Security/privacy.
- Documentation/onboarding.

## 7. Evidence Requirements

Evidence required for patch-eligible items:

- Customer/org context.
- Scenario or validation step where the issue occurred.
- Expected result.
- Actual result.
- Severity rationale.
- Screenshot, log, record link, or written customer note.
- Proposed validation step after fix.

Security/privacy issues:

- Treat as P0/P1 until reviewed.
- Record only sanitized evidence.
- Do not include secrets, credentials, access tokens, or sensitive customer data.

## 8. Decision Outcomes

Allowed triage decisions:

- Accept for v1.0.1 patch.
- Needs more evidence.
- Duplicate.
- Defer to backlog.
- Reject as out of scope.

Decision rules:

- Accept only P0/P1/P2 pilot feedback fixes.
- Defer P3/P4 items even if they are useful.
- Reject new feature work from v1.0.1 scope.
- Escalate ambiguous security/privacy findings for review before deferral.

## 9. Approved Patch Candidate List

Approved patch candidates:

| Candidate ID | Severity | Summary | Owner | Required Fix | Validation Needed |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

Handoff target:

```text
31B - P0/P1/P2 Fix Plan
```

## 10. Deferred Backlog List

Deferred backlog:

| Item ID | Summary | Reason Deferred | Suggested Future Milestone |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

Backlog rule:

- Deferred items should not enter Milestone 31 unless re-triaged as P0/P1/P2 with pilot evidence.

## 11. Exit Criteria

31A exit criteria:

- All Milestone 30 feedback sources reviewed.
- Duplicate feedback removed.
- Feature requests separated from fix candidates.
- Severity assigned to each item.
- P0/P1/P2 candidates identified.
- P3/P4 items deferred.
- Evidence requirements documented.
- Approved patch candidate list prepared for 31B.
