# SentinelFlow Named Credential Migration Plan

## 1. Purpose

This document defines the migration plan for moving SentinelFlow Salesforce callouts from the current beta Remote Site Setting model to a production-ready Named Credential model.

Important decision:

```text
Do not change working beta callout code yet.
Document migration first.
```

The beta integration is currently working and should remain stable while the production callout model is planned, reviewed, and tested.

## 2. Current Beta Callout Model

Current beta model:

```text
ZentomIncidentClient
-> Reads Zentom_Setting__mdt.Default.Base_URL__c
-> Uses Remote Site Setting Zentom_API
-> Calls https://zentom-api.onrender.com/api/incidents/receive
```

Current endpoint construction:

```apex
// Current
request.setEndpoint(baseUrl + '/api/incidents/receive');
```

Current metadata:

```text
Zentom_Setting__mdt.Default.Base_URL__c = https://zentom-api.onrender.com
Remote Site Setting: Zentom_API
Remote Site URL: https://zentom-api.onrender.com
```

Current beta advantages:

- Simple.
- Already verified.
- Works with hosted Render API.
- Keeps private beta stable.

Current beta limitations:

- Less package/security-review friendly than Named Credential.
- Endpoint is assembled manually in Apex.
- Future auth cannot be managed cleanly through External Credential.
- Admin setup remains more manual.

## 3. Target Production Callout Model

Target production model:

```text
ZentomIncidentClient
-> Uses Named Credential
-> callout:Zentom_API/api/incidents/receive
-> Future auth through External Credential
```

Future endpoint construction:

```apex
// Future
request.setEndpoint('callout:Zentom_API/api/incidents/receive');
```

Target production posture:

- Named Credential owns the base URL.
- External Credential handles future auth configuration.
- Permission Set Mapping controls which users can access the credential.
- Apex code no longer concatenates the callout base URL from Custom Metadata.

## 4. Why Named Credential Is Needed

Named Credential is needed for production and marketplace readiness because it:

- Aligns with Salesforce security-review expectations.
- Reduces custom URL handling in Apex.
- Supports future authentication through External Credential.
- Improves admin setup and endpoint management.
- Enables permission-based access to external services.
- Avoids relying only on Remote Site Settings for production callouts.

Named Credential also creates a clearer separation between:

- Apex business logic.
- Endpoint configuration.
- Authentication configuration.
- Permission/access assignment.

## 5. Migration Architecture

Production architecture:

```text
Salesforce Apex
-> Named Credential: Zentom_API
-> External Credential: Zentom_API_External
-> Hosted Zentom API
-> Hosted PostgreSQL
```

Callout path:

```text
callout:Zentom_API/api/incidents/receive
```

Future health check path:

```text
callout:Zentom_API/
callout:Zentom_API/api/health/db
```

Recommended migration approach:

1. Keep current Remote Site beta path unchanged.
2. Add Named Credential metadata in a branch or test milestone.
3. Add Apex feature flag or controlled branch change.
4. Validate in scratch org.
5. Validate in beta org.
6. Update install and security docs.
7. Remove or deprecate Remote Site Setting after successful validation.

## 6. Required Salesforce Metadata

Required production metadata:

- Named Credential: `Zentom_API`
- External Credential: `Zentom_API_External`
- Permission Set Mapping for the external credential
- Permission set updates for:
  - `SentinelFlow_Admin`
  - `SentinelFlow_Approver`
  - `SentinelFlow_Viewer`, if read-only health checks are exposed
- Optional Custom Metadata update to stop using Base URL for incident callout

Current beta metadata to preserve until migration is complete:

- Remote Site Setting: `Zentom_API`
- Custom Metadata: `Zentom_Setting__mdt.Default.Base_URL__c`

Security-review note:

Remote Site Setting can remain documented as beta/MVP behavior, but Named Credential should be the v1.0 target before formal marketplace security review.

## 7. Apex Code Changes Required

Current code behavior:

```apex
// Current
request.setEndpoint(baseUrl + '/api/incidents/receive');
```

Future code behavior:

```apex
// Future
request.setEndpoint('callout:Zentom_API/api/incidents/receive');
```

Expected Apex changes:

- Update `ZentomIncidentClient` endpoint construction.
- Remove direct dependency on Base URL for the incident callout path.
- Keep Custom Metadata for other non-secret configuration if needed.
- Add or update tests to assert Named Credential endpoint usage.
- Update any test mocks that assert exact endpoint strings.

Potential optional design:

- Add a temporary configuration flag to switch between Remote Site and Named Credential during migration.
- Keep the flag internal and remove it before v1.0 if the Named Credential path is fully validated.

## 8. Permission Set Changes Required

Permission set updates may be required so intended SentinelFlow users can access the External Credential.

Required review:

- `SentinelFlow_Admin` should have setup/admin access needed for configuration.
- `SentinelFlow_Approver` should have access required for operational callouts if approval/execution flows call external services.
- `SentinelFlow_Viewer` should remain read-only and should not receive unnecessary external execution permissions.

Permission principle:

```text
Grant only the access needed for each SentinelFlow role.
```

## 9. Deployment Plan

Recommended deployment plan:

1. Create Named Credential metadata in development branch.
2. Create External Credential metadata.
3. Create Permission Set Mapping.
4. Update Apex endpoint to `callout:Zentom_API/api/incidents/receive`.
5. Update Apex tests.
6. Deploy to scratch org.
7. Run stable SentinelFlow tests.
8. Run hosted API health test.
9. Run Salesforce test incident.
10. Validate approval, rejection, Case creation, replay timeline, and dashboard.
11. Update install guide.
12. Update security-review preparation docs.
13. Deploy to beta org.
14. Monitor callout behavior.

Do not deploy to production until:

- Named Credential callout works.
- Permission Set Mapping is validated.
- Regression checklist passes.
- Rollback plan is ready.

## 10. Rollback Plan

Rollback goal:

Return to the known-good Remote Site Setting beta callout model if the Named Credential migration fails during validation.

Rollback steps:

1. Revert Apex endpoint construction to Base URL + path.
2. Confirm `Zentom_Setting__mdt.Default.Base_URL__c = https://zentom-api.onrender.com`.
3. Confirm Remote Site Setting `Zentom_API` is active.
4. Redeploy last known-good metadata.
5. Run stable SentinelFlow tests.
6. Run hosted API health check.
7. Run Salesforce test incident.
8. Confirm incident write-back and replay timeline.

Rollback should not require hosted API changes.

## 11. Testing Checklist

Named Credential migration testing checklist:

- Named Credential `Zentom_API` exists.
- External Credential exists.
- Permission Set Mapping is assigned correctly.
- Apex endpoint uses `callout:Zentom_API/api/incidents/receive`.
- Stable Apex tests pass.
- Hosted API health check works.
- Hosted DB health check works.
- Salesforce test incident works.
- Sentinel Incident is created.
- Risk score is populated.
- Policy decision is populated.
- Recommendation is populated.
- Runbook key is populated.
- Approval works.
- Rejection works.
- Case creation works.
- Replay timeline works.
- Dashboard loads.
- Viewer permission remains read-only.
- Remote Site Setting dependency is removed or documented as fallback only.

## 12. Production Readiness Criteria

Named Credential migration is production-ready when:

- Named Credential metadata is committed.
- External Credential metadata is committed or documented if org-created.
- Permission Set Mapping is validated.
- Apex callout uses `callout:Zentom_API/api/incidents/receive`.
- No hardcoded hosted API URL is required in Apex.
- Custom Metadata Base URL is no longer required for the main incident callout.
- Stable tests pass.
- Fresh-org validation passes.
- Hosted API and DB health checks pass.
- Full incident workflow passes.
- Install guide is updated.
- Security review preparation docs are updated.
- Rollback path is documented and tested.
