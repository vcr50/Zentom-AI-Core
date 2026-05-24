# SentinelFlow Private Beta Plan

## 1. Beta Goal

The goal of SentinelFlow Private Beta is to validate the hosted Salesforce-to-Zentom incident intelligence workflow with selected users before public marketplace submission.

## 2. Beta Scope

Private beta focuses on the already verified hosted beta workflow:

- Salesforce package installation and setup.
- Permission set assignment.
- Hosted Zentom API connection.
- Hosted PostgreSQL persistence.
- Incident intake from Salesforce.
- Risk scoring.
- Policy evaluation.
- Recommendation and runbook selection.
- Human approval or rejection.
- Approved Case creation.
- Replay timeline verification.
- Dashboard review.
- Feedback capture and bug triage.

Out of scope for private beta:

- Public AppExchange listing.
- Full autonomous remediation.
- Hosted Ollama or hosted HYBRID mode.
- Customer-specific fine-tuned models.
- Named Credential migration, unless pulled forward before public security review.

## 3. Beta Org Details

Primary beta org target:

```text
TBD
```

Reference validation org:

```text
sentinelflow-beta-18f
```

Current hosted API:

```text
https://zentom-api.onrender.com
```

Required Salesforce setting:

```text
Zentom_Setting__mdt.Default.Base_URL__c = https://zentom-api.onrender.com
```

Required Remote Site Setting:

```text
Name: Zentom_API
URL: https://zentom-api.onrender.com
Active: true
```

Required permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

## 4. Beta Users

Recommended beta participants:

- Salesforce admin
- Salesforce developer
- RevOps or Sales Operations tester
- Support operations tester
- Platform owner or technical reviewer

Suggested beta roles:

- Admin tester: validates setup, permissions, configuration, and metadata.
- Approver tester: validates approval and rejection workflow.
- Viewer tester: validates dashboard, incidents, and replay timeline read-only access.
- Technical tester: captures debug logs, callout results, and integration issues.

## 5. Test Scenarios

### Scenario 1: Hosted API Health

Goal:

Confirm hosted Zentom API is reachable.

Test:

```text
GET https://zentom-api.onrender.com/
```

Expected:

```text
Zentom API is ready
```

### Scenario 2: Hosted Database Health

Goal:

Confirm hosted PostgreSQL is connected.

Test:

```text
GET https://zentom-api.onrender.com/api/health/db
```

Expected:

- Database health returns healthy.
- Required tables are available.
- Hosted DB connection succeeds.

### Scenario 3: Salesforce Test Incident

Goal:

Confirm Salesforce can send an incident to the hosted Zentom API.

Test Apex:

```apex
ZentomIncidentClient.sendIncident(
    'FLOW_FAILURE',
    'Salesforce Flow',
    'production',
    'Flow failed because owner field is null and missing account owner'
);
```

Expected:

- New `Sentinel_Incident__c` created.
- Risk: `95 / CRITICAL`.
- Policy: `HUMAN_APPROVAL_REQUIRED`.
- Status: `Approval Required`.
- Approval Status: `Pending Approval`.
- Runbook: `FLOW_FAILURE_BASIC_RECOVERY`.

### Scenario 4: Approval Workflow

Goal:

Confirm an approver can approve or reject a recommendation.

Expected:

- Approval panel is visible.
- Approve action updates incident approval fields.
- Reject action updates incident approval fields.
- Replay timeline records the approval decision.

### Scenario 5: Approved Case Creation

Goal:

Confirm approved action creates a Salesforce Case safely.

Expected:

- Case is created only after approval.
- Case `Origin = SentinelFlow`.
- Incident execution status updates.
- Created Case reference is stored on the incident.
- Replay timeline records execution.

### Scenario 6: Dashboard and Replay Review

Goal:

Confirm users can review operational status.

Expected:

- SentinelFlow dashboard loads.
- Incident counts are visible.
- Replay timeline shows intake, risk, policy, recommendation, approval, and execution events.

### Scenario 7: Permission Boundaries

Goal:

Confirm role-specific access works.

Expected:

- Admin can configure and operate SentinelFlow.
- Approver can approve, reject, and execute allowed actions.
- Viewer can read incidents, dashboard, and replay timeline without performing actions.

## 6. Success Criteria

Private beta is successful when:

- Beta package deploys cleanly to the selected org.
- Permission sets can be assigned without manual metadata repair.
- Hosted API health succeeds.
- Hosted DB health succeeds.
- Salesforce can send a test incident to hosted Zentom API.
- Incident is written back into Salesforce.
- Risk, policy, recommendation, and runbook values are correct.
- Approval and rejection workflows work.
- Approved Case creation works.
- Dashboard loads for permitted users.
- Replay timeline shows expected events.
- Beta testers can complete core scenarios with limited assistance.
- High-priority defects are captured and triaged.

## 7. Feedback Form / Questions

Recommended beta feedback questions:

1. Was the setup guide clear enough to complete installation?
2. Did the SentinelFlow app open correctly after permission assignment?
3. Did the hosted API connection work on the first attempt?
4. If the first hosted API call failed, did retrying after Render wake-up solve it?
5. Was the test incident result understandable?
6. Was the risk score useful?
7. Was the policy decision clear?
8. Was the recommended runbook useful?
9. Was the approval panel easy to use?
10. Did Case creation behave as expected?
11. Did the replay timeline help explain what happened?
12. Did the dashboard provide useful operational visibility?
13. What felt confusing or incomplete?
14. What should be improved before public marketplace submission?
15. Would you trust this workflow for a controlled production pilot?

Recommended rating fields:

- Setup clarity: 1-5
- Workflow usefulness: 1-5
- Trust and governance: 1-5
- Dashboard usefulness: 1-5
- Replay timeline usefulness: 1-5
- Overall beta readiness: 1-5

## 8. Known Limitations

- Hosted beta uses `AI_MODE=RULE`.
- Local HYBRID mode with Ollama is for advanced demo only.
- Full autonomous remediation is not enabled.
- Named Credential migration is planned before marketplace/security review.
- Remote Site Setting is used for MVP/beta.
- Render free tier may cold start after inactivity.
- Public AppExchange security review is not complete.
- Setup wizard is planned, not implemented.

## 9. Bug Triage Process

Recommended severity levels:

- Severity 1: Blocks installation, hosted API callout, or core incident creation.
- Severity 2: Breaks approval, execution, dashboard, or replay timeline.
- Severity 3: Incorrect text, confusing UI state, documentation gap, or non-blocking setup issue.
- Severity 4: Enhancement request or future product suggestion.

Recommended triage steps:

1. Capture the issue using the escalation checklist from `docs/support-troubleshooting-guide.md`.
2. Reproduce in the beta org.
3. Confirm whether the issue is Salesforce metadata, permissions, hosted API, hosted DB, or documentation.
4. Assign severity.
5. Decide fix now, document workaround, or defer.
6. Apply fix in a branch or local milestone.
7. Validate with stable tests and targeted manual scenario.
8. Update beta release notes if the issue affects testers.

## 10. Exit Criteria for Beta

Private beta can exit when:

- All core beta test scenarios pass.
- No open Severity 1 issues remain.
- No open Severity 2 issues remain without an accepted workaround.
- Install guide and troubleshooting docs reflect real tester issues.
- Feedback has been reviewed and prioritized.
- Beta release notes are complete.
- Known limitations are clearly documented.
- Decision is made for the next phase: extended beta, marketplace security-review preparation, or production pilot.
