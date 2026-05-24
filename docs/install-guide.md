# SentinelFlow Install Guide

## 1. Overview

This guide helps a Salesforce admin install and verify the SentinelFlow beta package.

SentinelFlow beta flow:

```text
Salesforce
-> Hosted Zentom API
-> Risk + policy + recommendation
-> Salesforce write-back
-> Human approval
-> Case creation
-> Replay timeline
```

Hosted Zentom API:

```text
https://zentom-api.onrender.com
```

Hosted beta uses `AI_MODE=RULE`.

## 2. Prerequisites

Required:

- Salesforce org with permission to deploy metadata.
- Salesforce CLI installed and authenticated.
- Access to the SentinelFlow Salesforce project.
- Hosted Zentom API reachable at `https://zentom-api.onrender.com`.

Recommended validation manifest:

```text
apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml
```

## 3. Package Deployment

From the Salesforce project folder:

```powershell
cd "D:\TomCodeX Inc\zentom-suite\apps\sentinelflow-salesforce"
```

Validate first:

```powershell
sf project deploy validate `
  --manifest manifest/package-sentinelflow-beta.xml `
  --test-level RunSpecifiedTests `
  --tests ZentomIncidentClientTest `
  --tests ZentomApprovalControllerTest `
  --tests ZentomExecutionControllerTest `
  --tests ZentomReplayControllerTest `
  --tests ZentomDashboardControllerTest `
  --target-org <target-org>
```

Deploy:

```powershell
sf project deploy start `
  --manifest manifest/package-sentinelflow-beta.xml `
  --test-level RunSpecifiedTests `
  --tests ZentomIncidentClientTest `
  --tests ZentomApprovalControllerTest `
  --tests ZentomExecutionControllerTest `
  --tests ZentomReplayControllerTest `
  --tests ZentomDashboardControllerTest `
  --target-org <target-org>
```

## 4. Permission Set Assignment

Assign the required permission sets to the appropriate users.

Permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

CLI examples:

```powershell
sf org assign permset --name SentinelFlow_Admin --target-org <target-org>
sf org assign permset --name SentinelFlow_Approver --target-org <target-org>
sf org assign permset --name SentinelFlow_Viewer --target-org <target-org>
```

Role guidance:

- Admin: setup, full beta package access, troubleshooting.
- Approver: approve/reject and execute approved actions.
- Viewer: read-only dashboard, incident, audit, policy, and replay access.

## 5. Zentom API Configuration

Verify the Custom Metadata record:

```text
Zentom_Setting__mdt.Default.Base_URL__c
```

Expected value:

```text
https://zentom-api.onrender.com
```

CLI verification:

```powershell
sf data query `
  --target-org <target-org> `
  --query "SELECT QualifiedApiName, Base_URL__c FROM Zentom_Setting__mdt WHERE QualifiedApiName = 'Default'"
```

## 6. Remote Site Setting

Verify Remote Site Setting:

```text
Name: Zentom_API
URL: https://zentom-api.onrender.com
```

The Remote Site URL must be the base URL only.

Correct:

```text
https://zentom-api.onrender.com
```

Incorrect:

```text
https://zentom-api.onrender.com/api/incidents/receive
```

## 7. Verify SentinelFlow App

Open Salesforce App Launcher and search:

```text
SentinelFlow
```

Expected:

- SentinelFlow app is visible.
- SentinelFlow Home opens.
- Dashboard loads.
- Sentinel Incident tab is available.
- Sentinel Audit Log tab is available.
- Zentom Policy Decision tab is available.

## 8. Run Test Incident

Run Anonymous Apex:

```apex
ZentomIncidentClient.sendIncident(
    'FLOW_FAILURE',
    'Salesforce Flow',
    'production',
    'Flow failed because owner field is null and missing account owner'
);
```

Expected result:

- New Sentinel Incident created.
- Risk: `95 / CRITICAL`.
- Policy: `HUMAN_APPROVAL_REQUIRED`.
- Status: `Approval Required`.
- Approval Status: `Pending Approval`.
- Runbook: `FLOW_FAILURE_BASIC_RECOVERY`.
- Audit logs created.
- Replay timeline visible.

If this is the first call after inactivity, Render may need to wake up. Retry after the hosted service responds.

## 9. Approve / Reject Recommendation

Open the created Sentinel Incident.

Use the approval panel to:

- Approve the recommendation.
- Reject the recommendation with a reason.

Expected approve result:

- Status: `Approved`.
- Approval Status: `Approved`.
- Recommendation Status: `Approved`.
- Execution Status: `Ready for Execution`.
- Audit log: `HUMAN_APPROVED`.

Expected reject result:

- Status: `Closed`.
- Approval Status: `Rejected`.
- Recommendation Status: `Rejected`.
- Audit log: `HUMAN_REJECTED`.

## 10. Execute Approved Action

After approval, execute the approved action.

Expected result:

- Salesforce Case is created.
- Case Subject begins with `[SentinelFlow]`.
- Case Origin is `SentinelFlow`.
- Case Priority is `High` for `CRITICAL` or `HIGH` incidents.
- Incident Status becomes `Action Created`.
- Execution Status becomes `Executed`.
- Created Case reference is populated.

## 11. Verify Replay Timeline

Open the replay timeline for the incident.

Expected audit events:

- `INCIDENT_RECEIVED`
- `RISK_CALCULATED`
- `ZENTOM_POLICY_EVALUATED`
- `AI_RECOMMENDATION_GENERATED`
- `RUNBOOK_SELECTED`
- `HUMAN_APPROVED` or `HUMAN_REJECTED`
- `RUNBOOK_ACTION_EXECUTED`
- `CASE_CREATED`

## 12. Troubleshooting

### Render Cold Start

Symptom:

- First call times out or no incident appears immediately.

Fix:

- Open `https://zentom-api.onrender.com`.
- Wait for the health response.
- Retry the anonymous Apex call.

### Remote Site Error

Symptom:

- Apex callout fails because endpoint is not authorized.

Fix:

- Verify Remote Site Setting `Zentom_API`.
- URL must be `https://zentom-api.onrender.com`.
- Do not include `/api/incidents/receive`.

### Permission Issue

Symptom:

- User cannot see app, tabs, records, dashboard, approval panel, or replay timeline.

Fix:

- Assign `SentinelFlow_Admin` for admin users.
- Assign `SentinelFlow_Approver` for approval/execution users.
- Assign `SentinelFlow_Viewer` for read-only users.

### No Incident Record

Symptom:

- Anonymous Apex executes, but no Sentinel Incident appears.

Fix:

- Check Apex debug logs.
- Verify `Zentom_Setting__mdt.Default.Base_URL__c`.
- Confirm hosted API health at `https://zentom-api.onrender.com`.
- Retry after Render wakes up.

### Case Origin Issue

Symptom:

- Case creation fails or Case Origin is not `SentinelFlow`.

Fix:

- Verify Case Origin includes `SentinelFlow`.
- Confirm `CaseOrigin` standard value set was deployed.
- The execution controller falls back to `Web` only if `SentinelFlow` is unavailable.
