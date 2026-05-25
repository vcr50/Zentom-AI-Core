# SentinelFlow P0/P1/P2 Fix Plan

## 1. Purpose

This document defines 31B P0/P1/P2 Fix Plan for Milestone 31 v1.0.1 Patch / Pilot Feedback Fixes.

Goal:

```text
Convert approved pilot feedback triage items into a controlled v1.0.1 fix plan with owners, validation evidence, rollback paths, and patch readiness criteria.
```

Patch rule:

```text
No new features.
Only pilot feedback fixes: P0/P1/P2.
```

## 2. Fix Scope

Included fix scope:

- P0/P1/P2 issues accepted during 31A Pilot Feedback Triage.
- Pilot blockers.
- Hosted API failures.
- Salesforce package install blockers.
- Callout/authentication failures.
- Approval or execution defects.
- Case creation defects.
- Replay/audit defects.
- Dashboard or Org Health Score defects that materially affect pilot value.
- Error logging defects.
- Data privacy or security issues.
- Onboarding/documentation corrections tied to pilot blockers or material friction.

Patch constraints:

- Fixes must be small, targeted, and evidence-backed.
- Fixes must preserve the existing v1.0.0 release candidate architecture unless a P0/P1 requires a minimal correction.
- Fixes must include validation evidence before patch readiness.

## 3. P0 Issues

P0 definition:

- Customer or pilot is blocked.
- Package cannot install.
- Hosted API is unavailable.
- Authentication is broken.
- Data privacy/security issue is confirmed.
- Core incident creation cannot run.

P0 fix table:

| Issue ID | Summary | Source Evidence | Owner | Required Fix | Validation Required | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD |

P0 rule:

- No patch release readiness while any P0 remains open.

## 4. P1 Issues

P1 definition:

- Core pilot workflow fails or returns materially incorrect results.
- Approval/execution fails.
- Case creation fails.
- Replay/audit evidence is materially wrong.
- Customer trust is blocked.

P1 fix table:

| Issue ID | Summary | Source Evidence | Owner | Required Fix | Validation Required | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD |

P1 rule:

- No patch release readiness while any unmitigated P1 remains open.

## 5. P2 Issues

P2 definition:

- Important usability, reliability, onboarding, documentation, dashboard, or supportability issue that should be fixed before broader controlled rollout.

P2 fix table:

| Issue ID | Summary | Source Evidence | Owner | Required Fix | Validation Required | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD |

P2 rule:

- P2 items may ship with documented mitigation only if accepted by the patch owner and pilot/customer owner.

## 6. Out-of-Scope Items

Out of scope:

- New features.
- P3/P4 improvements.
- Major AI architecture changes.
- Hosted HYBRID Ollama.
- Agentforce production integration.
- Full autonomous remediation.
- Large object model changes.
- Marketplace listing expansion.
- Broad UI redesign.
- Non-pilot roadmap ideas.

Out-of-scope tracker:

| Item ID | Summary | Reason Out of Scope | Backlog Location |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

## 7. Fix Owner

Required ownership fields:

- Patch owner: TBD.
- Technical owner: TBD.
- QA/validation owner: TBD.
- Customer/pilot follow-up owner: TBD.
- Security/privacy reviewer, if applicable: TBD.
- Release notes owner: TBD.

Ownership rules:

- Every P0/P1/P2 must have an owner.
- Every P0/P1/P2 must have expected validation evidence.
- Security/privacy items require reviewer sign-off before patch readiness.

## 8. Validation Required

Validation required by issue type:

- Package/install: package deploy or install evidence, test results, and permission assignment verification.
- Hosted API: API health check, authenticated request evidence, and error handling evidence.
- Hosted DB: persistence/retrieval verification and sanitized evidence.
- Callout/authentication: Salesforce callout success, authentication success/failure behavior, and sanitized logs.
- Incident creation: `FLOW_FAILURE` incident record creation and expected field values.
- Risk/policy: expected risk, severity, and policy decision evidence.
- Approval/execution: approval state, execution state, and Case creation evidence.
- Replay/audit: timeline event ordering and audit record evidence.
- Dashboard/Org Health Score: dashboard load and expected card visibility.
- Error logging: expected error capture without sensitive data.
- Documentation/onboarding: corrected doc reviewed against pilot issue.

Required validation record:

| Issue ID | Validation Step | Expected Result | Actual Result | Evidence | Result |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

## 9. Rollback Plan

Rollback plan:

- Identify files changed for each fix.
- Keep each fix scoped to the smallest safe change.
- Document pre-fix behavior and post-fix behavior.
- Preserve a clean commit history for each accepted patch change.
- Revert individual fix commits if validation fails and the change cannot be corrected safely.
- If hosted API changes are involved, retain previous deploy artifact or previous commit reference.
- If Salesforce metadata changes are involved, retain previous manifest/package state.

Rollback decision rules:

- Roll back any fix that introduces a new P0/P1.
- Pause patch readiness if rollback affects another approved fix.
- Re-run validation after rollback.

## 10. Patch Readiness Criteria

Patch readiness criteria:

- All accepted P0 issues fixed and validated.
- All accepted P1 issues fixed or explicitly mitigated and accepted.
- P2 issues fixed, mitigated, or consciously deferred with owner approval.
- No new features added.
- No out-of-scope architecture changes added.
- Validation evidence captured for every accepted fix.
- Security/privacy items reviewed and signed off.
- Rollback plan documented.
- Release notes inputs prepared for 31F.
- Patch scope ready for 31C Patch Scope Freeze.

Next milestone:

```text
31C - Patch Scope Freeze
```

Exit criteria:

- P0/P1/P2 fix candidates listed.
- Owners assigned.
- Validation requirements defined.
- Out-of-scope items separated.
- Rollback plan documented.
- Patch readiness criteria agreed.
