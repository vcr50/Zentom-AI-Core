# SentinelFlow Beta Bug Fix Sprint Plan

## 1. Purpose

This document defines the process for handling private beta bugs before SentinelFlow beta release notes are finalized.

The goal is to turn beta feedback, logs, and support evidence into prioritized fixes, validated workarounds, or clearly documented known limitations.

## 2. Sprint Scope

In scope:

- Installation and package deployment issues.
- Permission set and access issues.
- Hosted Zentom API connectivity issues.
- Hosted database health and persistence issues.
- Salesforce incident intake and write-back issues.
- Risk, policy, recommendation, and runbook population issues.
- Approval, rejection, and execution workflow issues.
- Case creation issues.
- Replay timeline issues.
- Dashboard and Org Health Score issues.
- Documentation fixes required for beta testers.

Out of scope:

- Public AppExchange security review changes.
- Full autonomous remediation.
- Hosted Ollama or hosted HYBRID mode.
- New major product features.
- Customer-specific fine-tuning.

## 3. Bug Intake Sources

Bug intake sources:

- Beta feedback form
- Salesforce debug logs
- SentinelFlow Replay Timeline
- Render logs
- Hosted DB health endpoint
- User screenshots
- Support/troubleshooting guide

Recommended evidence:

- Salesforce Org Id
- User role
- Permission set
- Sentinel Incident Id
- Steps to reproduce
- Expected result
- Actual result
- Apex debug logs
- Render request timestamp
- Hosted API health result
- Hosted DB health result
- Screenshots
- Replay timeline events

## 4. Severity Levels

```text
P0 - Blocks install or package deployment
P1 - Blocks incident processing or write-back
P2 - Approval/execution/replay issue
P3 - UI, wording, dashboard, or documentation issue
P4 - Enhancement or nice-to-have
```

## 5. Triage Rules

```text
P0 - Fix immediately before beta continues
P1 - Fix before release candidate
P2 - Fix if reproducible and impacts core workflow
P3 - Fix if low-risk and quick
P4 - Move to backlog
```

Triage questions:

1. Can the issue be reproduced?
2. Does it block installation or package deployment?
3. Does it block incident intake or write-back?
4. Does it create a governance or approval risk?
5. Does it affect the hosted API or database?
6. Does it affect a documented beta test scenario?
7. Is there a safe workaround?
8. Does the documentation need to be updated?

## 6. Fix Workflow

Recommended fix workflow:

1. Log the bug with severity and evidence.
2. Reproduce the issue in a beta or validation org.
3. Identify ownership: Salesforce metadata, Apex, LWC, hosted API, database, configuration, or documentation.
4. Create a focused fix.
5. Avoid unrelated refactors during beta stabilization.
6. Run targeted validation for the affected workflow.
7. Run the regression checklist before release candidate.
8. Update support/troubleshooting docs if the issue may recur.
9. Update release notes with fixed issues or known limitations.

Fix decision:

- Fix now if the issue is P0 or P1.
- Fix now if the issue is P2 and reproducible in the core workflow.
- Fix P3 only when the change is low-risk and improves tester clarity.
- Move P4 items to backlog unless they are trivial and safe.

## 7. Validation Workflow

For each fixed bug:

1. Re-run the original reproduction steps.
2. Confirm the expected result now occurs.
3. Confirm no new error appears in Apex debug logs.
4. Confirm hosted API health remains successful.
5. Confirm hosted DB health remains successful when persistence is involved.
6. Confirm relevant replay timeline events still appear.
7. Confirm permission boundaries are unchanged.
8. Capture the validation result in the bug record.

For Salesforce metadata or Apex fixes:

- Validate against the beta manifest.
- Run stable SentinelFlow tests.
- Test the specific beta scenario affected by the change.

For hosted API fixes:

- Confirm Render deploy succeeds.
- Confirm `/` returns healthy.
- Confirm `/api/health/db` returns healthy.
- Confirm `/api/incidents/receive` works in RULE mode.

## 8. Regression Test Checklist

Regression checklist:

- Hosted API health works
- `/api/health/db` works
- Salesforce Apex callout works
- Incident write-back works
- Risk/policy/recommendation populated
- Approval works
- Rejection works
- Case creation works
- Replay timeline works
- Dashboard loads
- Org Health Score loads
- Permission sets behave correctly

Recommended regression order:

1. Hosted API health.
2. Hosted DB health.
3. Salesforce test incident.
4. Risk, policy, recommendation, and runbook check.
5. Approval workflow.
6. Rejection workflow.
7. Approved Case creation.
8. Replay timeline.
9. Dashboard and Org Health Score.
10. Permission set validation.

## 9. Release Candidate Criteria

A beta release candidate is ready when:

- No open P0 issues remain.
- No open P1 issues remain.
- Open P2 issues have either a fix or accepted workaround.
- Core beta scenarios pass.
- Regression checklist passes.
- Install guide reflects current setup.
- Support/troubleshooting guide reflects known recurring issues.
- Release notes list known limitations clearly.
- Hosted API and hosted DB health are verified.
- Salesforce package behavior is stable enough for selected beta users.

## 10. Known Beta Risks

Known beta risks:

- Render free-tier cold starts may affect first request latency.
- Hosted beta uses `AI_MODE=RULE` only.
- Local HYBRID mode with Ollama is for advanced demos only.
- Remote Site Setting is used for beta.
- Named Credential migration is planned before marketplace/security review.
- Setup wizard is planned but not implemented.
- Full autonomous remediation is not enabled.
- Beta testers may need admin support for permission assignment and debug logs.
- Hosted database or Render environment variable changes can affect incident persistence.
