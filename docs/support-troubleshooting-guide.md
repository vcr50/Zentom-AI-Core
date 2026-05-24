# SentinelFlow Support and Troubleshooting Guide

## 1. Purpose

This guide helps Salesforce admins, developers, and support teams diagnose common SentinelFlow beta issues across installation, Salesforce callouts, hosted Zentom API connectivity, incident processing, approvals, execution, dashboards, and replay timeline behavior.

## 2. Support Scope

Supported beta scope:

- Salesforce package installation and metadata validation.
- Permission set assignment.
- Hosted Zentom API connection.
- Incident intake and write-back.
- Risk scoring and policy decision review.
- Recommendation and runbook verification.
- Human approval workflow.
- Approved Case creation.
- Dashboard and replay timeline validation.

Out of scope for hosted beta:

- Public Ollama hosting.
- Hosted HYBRID or RAG mode.
- Autonomous remediation without approval.
- Custom customer-specific model training.
- Production AppExchange security review certification.

## 3. Common Installation Issues

### Package deployment fails

Check:

- Deploying from the correct Salesforce project folder.
- Manifest path is correct.
- Target org alias is correct.
- Required metadata exists in the repo.
- Stable tests are selected for validation.

Recommended validation command:

```powershell
sf project deploy validate `
  --manifest manifest/package-sentinelflow-beta.xml `
  --test-level RunSpecifiedTests `
  --tests ZentomIncidentClientTest `
  --tests ZentomApprovalControllerTest `
  --tests ZentomExecutionControllerTest `
  --tests ZentomReplayControllerTest `
  --tests ZentomDashboardControllerTest `
  --target-org astrosoft
```

### SentinelFlow app is not visible

Fix:

- Assign one of the SentinelFlow permission sets.
- Confirm the app metadata deployed.
- Confirm the user has access to the relevant tabs.

Permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

## 4. Common API / Callout Issues

### Render cold start

Issue:

First call to hosted Zentom API may timeout or fail.

Cause:

Render free-tier service may sleep when idle.

Fix:

- Retry after 30-60 seconds.
- Open `https://zentom-api.onrender.com/` to wake the service.
- Retry the Salesforce action after the health endpoint responds.

### Remote Site error

Issue:

Salesforce callout fails with unauthorized endpoint.

Fix:

Verify Remote Site Setting:

```text
Name: Zentom_API
URL: https://zentom-api.onrender.com
Active: true
```

The Remote Site URL should be the base URL only. Do not include `/api/incidents/receive`.

### Wrong Base URL

Issue:

Apex callout still points to an old Cloudflare or local URL.

Fix:

Verify:

```text
Zentom_Setting__mdt.Default.Base_URL__c
=
https://zentom-api.onrender.com
```

Also search metadata for old URLs before a beta deploy.

### Hosted API health check fails

Check:

```text
https://zentom-api.onrender.com/
```

Expected:

```json
{
  "status": "running",
  "service": "zentom-api",
  "message": "Zentom API is ready"
}
```

Database health check:

```text
https://zentom-api.onrender.com/api/health/db
```

Expected:

- Database status is healthy.
- Required tables are present.
- Hosted PostgreSQL connection succeeds.

## 5. Common Permission Issues

### User cannot open SentinelFlow records

Check:

- User has a SentinelFlow permission set.
- User has object access to `Sentinel_Incident__c`.
- User has object access to `Sentinel_Audit_Log__c`.
- User has object access to `Zentom_Policy_Decision__c`.

### Approval panel not visible

Fix:

Assign one of:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`

### Dashboard not loading

Check:

- User has a SentinelFlow permission set.
- User has access to `Sentinel_Incident__c`.
- User has Apex class access to `ZentomDashboardController`.
- Browser console does not show LWC permission or Apex errors.

## 6. Common Incident Processing Issues

### No incident created

Check:

- Apex debug logs.
- `ZentomIncidentClient` response logs.
- Render API health.
- `/api/health/db`.
- Remote Site Setting.
- Permission set assignment.
- `Zentom_Setting__mdt.Default.Base_URL__c`.

### Incident created but risk fields are blank

Check:

- Hosted API response includes `risk`.
- Salesforce field mappings in `ZentomIncidentClient`.
- User has field-level access to risk fields.
- Apex debug logs for JSON parsing errors.

### Incident does not show expected FLOW_FAILURE runbook

Check:

- Error message includes a Flow failure signal.
- Hosted beta API is running in `AI_MODE=RULE`.
- Response includes `runbookKey = FLOW_FAILURE_BASIC_RECOVERY`.
- Salesforce write-back maps runbook values correctly.

## 7. Common Approval / Execution Issues

### Approval button does not work

Check:

- User has `SentinelFlow_Admin` or `SentinelFlow_Approver`.
- Incident status is `Approval Required`.
- Approval status is `Pending Approval`.
- Apex class access exists for `ZentomApprovalController`.

### Rejection does not update the incident

Check:

- Approval panel Apex call succeeds.
- User has update access to `Sentinel_Incident__c`.
- Replay timeline audit record is created.

### Case creation fails

Check:

- User has Case create permission.
- Case Origin includes `SentinelFlow`.
- Incident `Approval_Status__c = Approved`.
- Incident `Execution_Status__c = Ready for Execution`.
- Apex class access exists for `ZentomExecutionController`.

### Case created with wrong Origin

Fix:

- Verify Case Origin includes `SentinelFlow`.
- Confirm latest `ZentomExecutionController` metadata is deployed.
- If `SentinelFlow` is unavailable, the controller may fall back to `Web`.

## 8. Common Dashboard / Replay Issues

### Replay timeline is empty

Check:

- `Sentinel_Audit_Log__c` records exist for the incident.
- Current user has read access to audit logs.
- Apex class access exists for `ZentomReplayController`.
- Incident lookup on audit logs points to the correct incident.

### Dashboard counts look wrong

Check:

- User can read all relevant SentinelFlow records.
- Test data exists in the current org.
- Dashboard controller filters match the expected beta records.
- Browser cache is not showing an old LWC bundle.

### LWC component fails to load

Check:

- Component deployed successfully.
- User has Apex class access.
- Browser console for LWC or Apex errors.
- Salesforce session is not expired.

## 9. Render Hosted API Issues

### Render service is suspended or sleeping

Fix:

- Open Render dashboard and confirm service is live.
- Visit `https://zentom-api.onrender.com/`.
- Wait 30-60 seconds and retry.

### Render deploy failed

Check:

- Build logs.
- Dockerfile path.
- Root directory: `services/zentom-api`.
- Required environment variables.
- `DATABASE_URL` is set.

### Hosted database connection fails

Check Render environment variables:

```text
DATABASE_URL=<hosted postgres url>
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_MODEL=zentom-rule-v1
```

Then test:

```text
https://zentom-api.onrender.com/api/health/db
```

### Hosted API returns non-RULE model

Fix:

Verify Render environment variables:

```text
AI_MODE=RULE
AI_MODEL=zentom-rule-v1
```

Hosted beta should not depend on Ollama.

## 10. Salesforce Debugging Steps

Recommended debugging flow:

1. Confirm the hosted API health endpoint works.
2. Confirm `/api/health/db` works.
3. Confirm `Zentom_Setting__mdt.Default.Base_URL__c` points to `https://zentom-api.onrender.com`.
4. Confirm Remote Site Setting `Zentom_API` is active.
5. Assign `SentinelFlow_Admin` to the testing user.
6. Enable Apex debug logs for the testing user.
7. Run the anonymous Apex test incident.
8. Review Apex debug logs for callout status and response body.
9. Open the latest `Sentinel_Incident__c`.
10. Review related replay timeline / audit events.

Anonymous Apex test:

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

## 11. Escalation Checklist

Before escalating, capture:

- Salesforce Org Id
- Sentinel Incident Id
- Apex debug log
- Render request timestamp
- Error message
- User permission set
- Screenshot of SentinelFlow incident
- Replay timeline events

Also include:

- Hosted API health result.
- Hosted DB health result.
- Current `Zentom_Setting__mdt.Default.Base_URL__c` value.
- Remote Site Setting URL and active status.
- Whether the issue happened on first call after idle time.

## 12. Known Beta Limitations

- Hosted beta uses `AI_MODE=RULE`.
- Hosted beta does not expose Ollama.
- HYBRID Ollama mode is available only for advanced local demos.
- Named Credential migration is planned before marketplace security review.
- Remote Site Setting is used for MVP/beta.
- Full autonomous remediation is not enabled.
- Human approval is required for production and high-risk actions.
- Render free-tier cold starts may delay the first request after inactivity.
- Support contact is a placeholder until public marketplace submission.
