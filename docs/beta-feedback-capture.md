# SentinelFlow Beta Feedback Capture

## 1. Purpose

This document defines how SentinelFlow private beta feedback should be collected, reviewed, prioritized, and converted into fixes or follow-up work.

The goal is to capture useful evidence from selected beta users while validating the hosted Salesforce-to-Zentom incident intelligence workflow before public marketplace submission.

## 2. Who Should Provide Feedback

Recommended feedback participants:

- Salesforce Admins
- Salesforce Developers
- SentinelFlow Approvers
- SentinelFlow Viewers
- RevOps / Sales Operations users
- Support Operations users
- Platform owners or technical reviewers

Each beta tester should identify their role when submitting feedback so issues can be interpreted against expected permissions and workflow access.

## 3. Feedback Channels

Recommended beta feedback channels:

- Shared beta feedback form
- GitHub issues or internal issue tracker
- Email to the beta support contact
- Live review notes from beta walkthrough sessions
- Screenshots and logs attached to bug reports

Minimum evidence for bugs:

- Salesforce org
- User role
- Scenario tested
- Steps to reproduce
- Expected result
- Actual result
- Screenshots or logs
- Sentinel Incident Id, if applicable
- Replay timeline events, if applicable

## 4. Feedback Form Questions

1. Was SentinelFlow easy to install and configure?
2. Did the SentinelFlow app open correctly?
3. Did the hosted Zentom API connection work?
4. Was the incident risk score understandable?
5. Was the policy decision clear?
6. Was the AI recommendation useful?
7. Was the runbook helpful?
8. Was the approval/rejection workflow clear?
9. Did the Case creation action work as expected?
10. Was the Replay Timeline useful for trust/audit?
11. Did the dashboard give a clear overview?
12. What confused you?
13. What should be improved before public release?
14. Would you use this in a real Salesforce org? Why or why not?

Recommended rating fields:

- Install and setup clarity: 1-5
- Incident workflow usefulness: 1-5
- Trust and governance: 1-5
- Approval workflow clarity: 1-5
- Replay timeline usefulness: 1-5
- Dashboard usefulness: 1-5
- Overall private beta readiness: 1-5

## 5. Bug Report Template

```text
Title:
Severity:
Org:
User Role:
Steps to Reproduce:
Expected Result:
Actual Result:
Screenshots/Logs:
Sentinel Incident Id:
Replay Timeline Events:
Notes:
```

## 6. Feature Request Template

```text
Title:
Requested By:
Problem:
Suggested Improvement:
Business Value:
Priority:
Notes:
```

## 7. Severity Levels

```text
P0 - Blocks install or package deployment
P1 - Blocks incident processing or write-back
P2 - Approval/execution/replay issue
P3 - UI, wording, dashboard, or documentation issue
P4 - Enhancement or nice-to-have
```

Severity guidance:

- P0 issues should be fixed before any further beta testing.
- P1 issues should be fixed before expanding the beta group.
- P2 issues should be fixed or given a clear workaround before beta exit.
- P3 issues should be batched into polish/documentation updates.
- P4 issues should be reviewed for roadmap fit.

## 8. Feedback Review Cadence

Recommended cadence during private beta:

- Daily review during the first active beta week.
- Twice-weekly review after the first week if P0/P1 issues are low.
- Immediate review for any P0 or P1 issue.
- End-of-beta review before release notes are finalized.

Each review should answer:

- What was reported?
- Is it reproducible?
- What severity is it?
- Is it a bug, setup issue, documentation issue, or enhancement?
- Does it block private beta exit?
- Who owns the fix or response?

## 9. Beta Success Signals

Positive beta signals:

- Admins can install and configure SentinelFlow using the docs.
- Testers can send a Flow failure incident successfully.
- Hosted Zentom API and hosted DB remain stable enough for beta testing.
- Risk and policy results are understood by testers.
- Approvers understand approve and reject actions.
- Approved Case creation works as expected.
- Replay timeline increases trust in the workflow.
- Dashboard gives a useful operational overview.
- Most feedback is P3/P4 rather than P0/P1/P2.
- Testers say they would consider using SentinelFlow in a real Salesforce org.

## 10. Feedback-to-Fix Workflow

Recommended workflow:

1. Capture feedback using the feedback form, bug report template, or feature request template.
2. Add missing evidence if the report is incomplete.
3. Assign severity.
4. Reproduce the issue in a beta or validation org.
5. Classify the issue as product bug, configuration issue, permission issue, hosted API issue, documentation gap, or enhancement.
6. Decide one of: fix now, provide workaround, document limitation, defer to roadmap.
7. Implement the fix in the appropriate code or documentation area.
8. Validate with targeted scenario from `docs/beta-testing-scenarios.md`.
9. Update `docs/support-troubleshooting-guide.md` if the issue is likely to recur.
10. Include resolved beta issues in release notes.

Fix priority:

- P0: fix immediately.
- P1: fix before broader beta.
- P2: fix before beta exit unless an accepted workaround exists.
- P3: fix during polish pass.
- P4: triage into future milestone.
