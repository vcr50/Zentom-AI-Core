# SentinelFlow Beta Testing Scenarios

Use this document to run consistent private beta validation for the hosted Salesforce-to-Zentom incident intelligence workflow.

## 1. Install and Setup Verification

Scenario Name:
Install and Setup Verification

Objective:
Confirm the SentinelFlow beta package is installed, configured, and visible to the right users.

User Role:
Salesforce Admin

Preconditions:
- Beta package metadata is deployed.
- Hosted API URL is available: `https://zentom-api.onrender.com`.
- Admin user has access to Setup.

Steps:
1. Confirm SentinelFlow app is available in App Launcher.
2. Confirm permission sets exist: `SentinelFlow_Admin`, `SentinelFlow_Approver`, `SentinelFlow_Viewer`.
3. Assign `SentinelFlow_Admin` to the admin tester.
4. Confirm `Zentom_Setting__mdt.Default.Base_URL__c` equals `https://zentom-api.onrender.com`.
5. Confirm Remote Site Setting `Zentom_API` is active and points to `https://zentom-api.onrender.com`.
6. Open the SentinelFlow app.

Expected Result:
- SentinelFlow app opens.
- Required permission sets are available.
- Base URL and Remote Site Setting point to the hosted API.
- No Cloudflare or local URL remains in beta configuration.

Pass/Fail:
TBD

Notes:
TBD

## 2. Hosted Zentom API Health Check

Scenario Name:
Hosted Zentom API Health Check

Objective:
Confirm the hosted Zentom API is live and reachable before Salesforce testing.

User Role:
Salesforce Admin or Technical Tester

Preconditions:
- Internet access is available.
- Render service exists.

Steps:
1. Open `https://zentom-api.onrender.com/`.
2. Confirm the health response appears.
3. Open `https://zentom-api.onrender.com/docs`.
4. Open `https://zentom-api.onrender.com/api/health/db`.

Expected Result:
- Root endpoint returns `Zentom API is ready`.
- API docs open.
- DB health endpoint reports hosted database connectivity.

Pass/Fail:
TBD

Notes:
TBD

## 3. Flow Failure Incident Intake

Scenario Name:
Flow Failure Incident Intake

Objective:
Confirm Salesforce can send a Flow failure incident to the hosted Zentom API and receive a response.

User Role:
Salesforce Admin or Technical Tester

Preconditions:
- `SentinelFlow_Admin` is assigned.
- Remote Site Setting is active.
- Base URL points to `https://zentom-api.onrender.com`.

Steps:
1. Open Anonymous Apex.
2. Run:

```apex
ZentomIncidentClient.sendIncident(
    'FLOW_FAILURE',
    'Salesforce Flow',
    'production',
    'Flow failed because owner field is null and missing account owner'
);
```

3. Open the SentinelFlow app.
4. Find the latest Sentinel Incident.

Expected Result:
- New `Sentinel_Incident__c` record is created.
- Incident type is `FLOW_FAILURE`.
- Source is `Salesforce Flow`.
- Error message is stored.
- Hosted response is written back to Salesforce.

Pass/Fail:
TBD

Notes:
TBD

## 4. Risk + Policy Verification

Scenario Name:
Risk + Policy Verification

Objective:
Confirm the incident receives the expected risk and policy decision.

User Role:
Salesforce Admin or Approver

Preconditions:
- Flow Failure Incident Intake scenario has passed.
- Latest Sentinel Incident is available.

Steps:
1. Open the latest Sentinel Incident.
2. Review risk score.
3. Review risk level.
4. Review policy decision.
5. Review incident status and approval status.

Expected Result:
- Risk score is `95`.
- Risk level is `CRITICAL`.
- Policy decision is `HUMAN_APPROVAL_REQUIRED`.
- Status is `Approval Required`.
- Approval Status is `Pending Approval`.

Pass/Fail:
TBD

Notes:
TBD

## 5. AI Recommendation + Runbook Verification

Scenario Name:
AI Recommendation + Runbook Verification

Objective:
Confirm hosted RULE-mode recommendation and runbook mapping are correct.

User Role:
Salesforce Admin or Approver

Preconditions:
- Flow Failure Incident Intake scenario has passed.
- Latest Sentinel Incident is available.

Steps:
1. Open the latest Sentinel Incident.
2. Review recommendation fields.
3. Review model name.
4. Review runbook key.
5. Confirm recommendation status.

Expected Result:
- Model is `zentom-rule-v1`.
- Hosted mode is RULE-based.
- Runbook is `FLOW_FAILURE_BASIC_RECOVERY`.
- Recommendation is generated and understandable.

Pass/Fail:
TBD

Notes:
TBD

## 6. Human Approval Workflow

Scenario Name:
Human Approval Workflow

Objective:
Confirm an authorized user can approve a high-risk recommendation.

User Role:
Salesforce Admin or SentinelFlow Approver

Preconditions:
- User has `SentinelFlow_Admin` or `SentinelFlow_Approver`.
- Incident has `Approval_Status__c = Pending Approval`.
- Incident status is `Approval Required`.

Steps:
1. Open the latest Sentinel Incident.
2. Open the approval panel.
3. Click approve.
4. Refresh the incident.
5. Review approval status, incident status, and execution status.
6. Review replay timeline.

Expected Result:
- Approval succeeds.
- Approval Status becomes `Approved`.
- Execution Status becomes `Ready for Execution`.
- Replay timeline records the approval event.

Pass/Fail:
TBD

Notes:
TBD

## 7. Rejection Workflow

Scenario Name:
Rejection Workflow

Objective:
Confirm an authorized user can reject a recommendation and prevent execution.

User Role:
Salesforce Admin or SentinelFlow Approver

Preconditions:
- User has `SentinelFlow_Admin` or `SentinelFlow_Approver`.
- A separate test incident exists with `Approval_Status__c = Pending Approval`.

Steps:
1. Open a pending Sentinel Incident.
2. Open the approval panel.
3. Click reject.
4. Refresh the incident.
5. Review approval status and execution status.
6. Review replay timeline.

Expected Result:
- Rejection succeeds.
- Approval Status becomes `Rejected`.
- Execution does not proceed.
- Replay timeline records the rejection event.

Pass/Fail:
TBD

Notes:
TBD

## 8. Execute Approved Action / Case Creation

Scenario Name:
Execute Approved Action / Case Creation

Objective:
Confirm approved recommendations can execute safe Case creation.

User Role:
Salesforce Admin or SentinelFlow Approver

Preconditions:
- User has `SentinelFlow_Admin` or `SentinelFlow_Approver`.
- Incident has `Approval_Status__c = Approved`.
- Incident has `Execution_Status__c = Ready for Execution`.
- User has permission to create Cases.
- Case Origin includes `SentinelFlow`.

Steps:
1. Open the approved Sentinel Incident.
2. Click execute action.
3. Refresh the incident.
4. Open the created Case reference.
5. Review Case fields.
6. Review replay timeline.

Expected Result:
- Case is created.
- Case Origin is `SentinelFlow`.
- Case Priority is appropriate for the incident.
- Incident stores the created Case reference.
- Execution Status becomes `Executed`.
- Replay timeline records the execution event.

Pass/Fail:
TBD

Notes:
TBD

## 9. Replay Timeline Verification

Scenario Name:
Replay Timeline Verification

Objective:
Confirm the replay timeline explains the full incident lifecycle.

User Role:
Salesforce Admin, Approver, or Viewer

Preconditions:
- At least one incident has completed intake, risk, policy, recommendation, approval, and execution.
- User has access to replay/audit data.

Steps:
1. Open the Sentinel Incident.
2. Open the replay timeline.
3. Review each event in order.
4. Confirm approval and execution events are visible.

Expected Result:
- Replay timeline loads.
- Events are visible in logical order.
- Timeline includes intake, risk calculation, policy evaluation, recommendation, runbook selection, approval decision, and execution.

Pass/Fail:
TBD

Notes:
TBD

## 10. Dashboard + Org Health Score Verification

Scenario Name:
Dashboard + Org Health Score Verification

Objective:
Confirm dashboard and org health views load for beta users.

User Role:
Salesforce Admin or Viewer

Preconditions:
- User has a SentinelFlow permission set.
- Test incidents exist.
- Dashboard metadata is deployed.

Steps:
1. Open the SentinelFlow app.
2. Open the dashboard.
3. Review incident counts.
4. Review risk summary.
5. Review org health score if visible.
6. Confirm the dashboard does not show Apex or LWC errors.

Expected Result:
- Dashboard loads.
- Incident metrics are visible.
- Org Health Score area loads or displays the expected beta value.
- No permission or controller errors appear.

Pass/Fail:
TBD

Notes:
TBD

## 11. Permission Set Validation

Scenario Name:
Permission Set Validation

Objective:
Confirm each beta permission set provides the expected access level.

User Role:
Salesforce Admin

Preconditions:
- Test users are available for Admin, Approver, and Viewer roles.
- Permission sets are deployed.

Steps:
1. Assign `SentinelFlow_Admin` to an admin tester.
2. Confirm admin tester can configure, approve, execute, view dashboard, and view replay.
3. Assign `SentinelFlow_Approver` to an approver tester.
4. Confirm approver tester can approve/reject and execute allowed actions.
5. Assign `SentinelFlow_Viewer` to a viewer tester.
6. Confirm viewer tester can view incidents, dashboard, and replay but cannot approve or execute.

Expected Result:
- Admin has full beta access.
- Approver has approval and execution access.
- Viewer has read-only access.
- No tester has broader access than intended.

Pass/Fail:
TBD

Notes:
TBD

## 12. Render Cold Start Retry Test

Scenario Name:
Render Cold Start Retry Test

Objective:
Confirm testers understand and can recover from Render free-tier cold starts.

User Role:
Salesforce Admin or Technical Tester

Preconditions:
- Hosted Render service may have been idle.
- Tester has browser access.

Steps:
1. Attempt the hosted API root health check.
2. If it times out or fails, wait 30-60 seconds.
3. Open `https://zentom-api.onrender.com/` in a browser.
4. Retry the Salesforce incident test.
5. Record whether cold start affected the test.

Expected Result:
- Service wakes after retry.
- Root endpoint returns `Zentom API is ready`.
- Salesforce incident test succeeds after service wake-up.
- Any cold start delay is captured in notes.

Pass/Fail:
TBD

Notes:
TBD

## 13. Support/Troubleshooting Evidence Capture

Scenario Name:
Support/Troubleshooting Evidence Capture

Objective:
Confirm testers capture enough evidence for support escalation.

User Role:
Salesforce Admin, Technical Tester, or Support Tester

Preconditions:
- A test incident exists or a failure has occurred.
- Tester has access to Salesforce logs and SentinelFlow records.

Steps:
1. Capture Salesforce Org Id.
2. Capture Sentinel Incident Id.
3. Capture Apex debug log.
4. Capture Render request timestamp.
5. Capture exact error message.
6. Capture user permission set.
7. Capture screenshot of SentinelFlow incident.
8. Capture replay timeline events.
9. Record hosted API health result.
10. Record hosted DB health result.

Expected Result:
- Support package contains enough evidence to reproduce or triage the issue.
- Escalation checklist matches `docs/support-troubleshooting-guide.md`.

Pass/Fail:
TBD

Notes:
TBD
