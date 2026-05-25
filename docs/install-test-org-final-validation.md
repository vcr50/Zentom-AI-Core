# SentinelFlow Install/Test Org Final Validation

## 1. Purpose

This document defines Milestone 28E for final install/test org validation before AppExchange / AgentExchange submission readiness wrap-up.

Goal:

```text
Prove the current SentinelFlow submission candidate deploys cleanly, passes tests, connects to the hosted Zentom API and database, processes the standard FLOW_FAILURE incident, supports approval/execution, creates a Salesforce Case, records Replay Timeline events, logs errors safely, and loads the dashboard.
```

This validation should be run against the final package candidate before submission sign-off.

## 2. Target Validation Org

Target validation org:

```text
Org alias:
Org type:
Org Id:
Username:
Validation date:
Validation owner:
```

Recommended org:

- Fresh scratch org, clean developer org, or designated packaging validation org.
- No unmanaged local metadata drift.
- No unrelated test data that could confuse screenshot/demo or validation evidence.

Org readiness checklist:

- [ ] Admin access confirmed.
- [ ] Metadata deployment access confirmed.
- [ ] Apex test execution access confirmed.
- [ ] Permission set assignment access confirmed.
- [ ] Remote Site / Named Credential visibility confirmed.
- [ ] Salesforce Case creation available.
- [ ] Debug/error evidence can be captured if needed.

## 3. Package Manifest Used

Package manifest:

```text
apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml
```

Release candidate reference:

```text
v1.0.0-rc.1
```

Target commit/reference:

```text
TBD
```

Manifest checklist:

- [ ] Stable Apex classes included.
- [ ] Stable LWC bundles included.
- [ ] Stable custom objects included.
- [ ] Stable custom metadata included.
- [ ] Permission sets included.
- [ ] App, tabs, layouts, and list views included.
- [ ] Remote Site fallback included if required.
- [ ] Named Credential path included if required.
- [ ] Experimental Agentforce metadata excluded.
- [ ] Temporary files excluded.
- [ ] No local-only URLs included.
- [ ] No hardcoded secrets included.

## 4. Deployment Command

Recommended validation command:

```powershell
sf project deploy validate --manifest apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml --target-org <target-org> --test-level RunLocalTests
```

Recommended deploy command, if a deploy is required after validation:

```powershell
sf project deploy start --manifest apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml --target-org <target-org> --test-level RunLocalTests
```

Deployment evidence:

```text
Command run:
Deploy/validation id:
Status:
Tests passing:
Tests failing:
Start time:
End time:
```

Required result:

```text
Package deploys cleanly.
17 tests pass.
0 tests fail.
```

## 5. Test Classes Run

Expected test result:

```text
17 tests passing / 0 failing
```

Test evidence:

| Test class | Result | Notes |
| --- | --- | --- |
| ZentomIncidentClientTest | TBD | Incident callout/write-back/error logging coverage. |
| ZentomApprovalControllerTest | TBD | Approval/rejection coverage. |
| ZentomExecutionControllerTest | TBD | Approved execution and Case creation coverage. |
| ZentomReplayControllerTest | TBD | Replay Timeline coverage. |
| ZentomDashboardControllerTest | TBD | Dashboard/Org Health Score coverage. |
| ZentomRunbookServiceTest | TBD | Runbook mapping coverage. |
| Other stable package tests | TBD | Confirm all local tests pass. |

Validation requirements:

- [ ] 17 tests pass.
- [ ] 0 tests fail.
- [ ] No test failure is accepted for final submission.
- [ ] Any flaky or environment-dependent failure is investigated before sign-off.

## 6. Permission Sets Assigned

Required permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

Assignment evidence:

| Permission set | Assigned user | Result | Notes |
| --- | --- | --- | --- |
| SentinelFlow_Admin | TBD | Pass/Fail/TBD | TBD |
| SentinelFlow_Approver | TBD | Pass/Fail/TBD | TBD |
| SentinelFlow_Viewer | TBD | Pass/Fail/TBD | TBD |

Permission behavior validation:

- [ ] Admin can open SentinelFlow app.
- [ ] Approver can approve/reject incidents.
- [ ] Approver can execute approved action where permitted.
- [ ] Viewer can view dashboard/replay.
- [ ] Viewer cannot approve incidents.
- [ ] Viewer cannot execute actions.

## 7. Hosted API Verification

Hosted API:

```text
https://zentom-api.onrender.com
```

API verification checklist:

- [ ] Root endpoint returns running/ready status.
- [ ] `/api/health/db` returns healthy status.
- [ ] Hosted database is configured.
- [ ] Hosted database type is PostgreSQL.
- [ ] Required tables are present.
- [ ] `missingTables = []`.
- [ ] pgvector is enabled.
- [ ] Incident receive endpoint is reachable.
- [ ] Shared secret authentication works if enabled.
- [ ] Missing/wrong shared secret returns HTTP 401 if enabled.

Evidence:

```text
Root endpoint result:
DB health result:
Database type:
missingTables:
pgvector:
Authentication result:
Timestamp:
```

Required result:

```text
Hosted API works.
Hosted DB works.
Hosted DB + pgvector verified.
```

## 8. Salesforce Incident Test

Standard incident:

```text
Incident type: FLOW_FAILURE
Source: Salesforce Flow
Environment: sandbox or validation
Action type: CREATE_CASE
```

Expected result:

```text
FLOW_FAILURE incident creates Sentinel Incident record.
Risk score: 95
Risk level: CRITICAL
Policy decision: HUMAN_APPROVAL_REQUIRED
Runbook: FLOW_FAILURE_BASIC_RECOVERY
Approval status: Pending Approval
```

Validation checklist:

- [ ] Send standard `FLOW_FAILURE` test incident.
- [ ] Salesforce callout succeeds.
- [ ] Hosted API receives incident.
- [ ] Sentinel Incident record is created.
- [ ] Hosted Zentom incident id is populated.
- [ ] Risk score is populated.
- [ ] Risk level is populated.
- [ ] Policy decision is populated.
- [ ] Recommendation is populated.
- [ ] Runbook is populated.
- [ ] No unexpected error log is created for successful path.

Evidence:

```text
Sentinel Incident name:
Sentinel Incident id:
Hosted Zentom incident id:
Risk score:
Risk level:
Policy decision:
Runbook:
Status:
Approval status:
```

## 9. Approval + Execution Test

Approval test:

- [ ] Open the created Sentinel Incident.
- [ ] Confirm Human Approval panel loads.
- [ ] Confirm recommendation and runbook are visible.
- [ ] Approve incident as Admin or Approver.
- [ ] Confirm approval status changes to `Approved`.
- [ ] Confirm recommendation status changes as expected.
- [ ] Confirm execution readiness.

Execution test:

- [ ] Execute approved action.
- [ ] Confirm execution action is `CREATE_CASE`.
- [ ] Confirm execution status is `Executed`.
- [ ] Confirm incident status is `Action Created`.
- [ ] Confirm `Created_Case__c` or related Case reference is populated.
- [ ] Confirm Salesforce Case exists.
- [ ] Confirm Case subject references `FLOW_FAILURE`.
- [ ] Confirm Case priority reflects high/critical risk.
- [ ] Confirm Case origin is `SentinelFlow` where available.

Required result:

```text
Approval/execution creates Case.
```

Evidence:

```text
Approved by:
Approval timestamp:
Execution status:
Created Case number:
Created Case id:
Case origin:
Case priority:
```

## 10. Replay Timeline Test

Expected Replay Timeline events:

- `INCIDENT_RECEIVED`
- `RISK_CALCULATED`
- `ZENTOM_POLICY_EVALUATED`
- `AI_RECOMMENDATION_GENERATED`
- `RUNBOOK_SELECTED`
- `HUMAN_APPROVED`
- `RUNBOOK_ACTION_EXECUTED`
- `CASE_CREATED`

Validation checklist:

- [ ] Replay Timeline loads.
- [ ] Expected events are present.
- [ ] Events are in expected order.
- [ ] Approval event is present.
- [ ] Execution event is present.
- [ ] Case creation event is present.
- [ ] Replay evidence does not expose secrets.
- [ ] Replay evidence is suitable for screenshot/demo if needed.

Required result:

```text
Replay timeline shows expected events.
```

Evidence:

```text
Replay component loaded:
Event count:
Events present:
Order verified:
Notes:
```

## 11. Dashboard Test

Dashboard validation:

- [ ] SentinelFlow app opens.
- [ ] Dashboard component loads.
- [ ] Recent incident appears.
- [ ] Risk/status summary reflects test incident.
- [ ] Approval queue/status reflects current state.
- [ ] Created Case/execution activity appears where supported.
- [ ] Org Health Score card loads.
- [ ] Admin view works.
- [ ] Approver view works.
- [ ] Viewer read-only view works.

Required result:

```text
Dashboard loads.
Org Health Score loads.
```

Evidence:

```text
Dashboard loaded:
Recent incident visible:
Org Health Score visible:
Admin result:
Approver result:
Viewer result:
Notes:
```

## 12. Error Logging Test

Error logging validation:

- [ ] Trigger a safe, controlled callout failure or bad-path validation.
- [ ] Confirm `Sentinel_Error_Log__c` record is created.
- [ ] Confirm error type is populated.
- [ ] Confirm status code is populated where applicable.
- [ ] Confirm endpoint is populated without secrets.
- [ ] Confirm request/response payloads are sanitized.
- [ ] Confirm API key/shared-secret is not stored.
- [ ] Confirm hosted API error logging works for unauthorized request if tested.
- [ ] Confirm hosted API error logs do not store secret values.

Required result:

```text
Error logging works.
Error logging does not expose secrets.
```

Evidence:

```text
Sentinel Error Log name/id:
Error type:
Status code:
Endpoint:
Hosted API error log result:
Secret exposure check:
Notes:
```

## 13. Pass/Fail Summary

Validation summary:

| Area | Required result | Actual result | Pass/Fail |
| --- | --- | --- | --- |
| Package deploy | Deploys cleanly | TBD | TBD |
| Apex tests | 17 passing / 0 failing | TBD | TBD |
| Hosted API | Works | TBD | TBD |
| Hosted DB | Works | TBD | TBD |
| pgvector | Verified | TBD | TBD |
| FLOW_FAILURE incident | Creates Sentinel Incident | TBD | TBD |
| Approval/execution | Creates Case | TBD | TBD |
| Replay Timeline | Expected events visible | TBD | TBD |
| Dashboard | Loads | TBD | TBD |
| Org Health Score | Loads | TBD | TBD |
| Error logging | Works without secrets | TBD | TBD |

Blockers:

| Blocker | Severity | Owner | Resolution required |
| --- | --- | --- | --- |
| TBD | P0/P1/P2/P3/P4 | TBD | TBD |

## 14. Final Submission Readiness Result

Final readiness result:

```text
Ready / Conditional readiness / Not ready
```

Readiness criteria:

- [ ] Package deploys cleanly.
- [ ] 17 tests pass.
- [ ] Hosted API works.
- [ ] Hosted DB works.
- [ ] FLOW_FAILURE incident creates record.
- [ ] Approval/execution creates Case.
- [ ] Replay Timeline shows expected events.
- [ ] Error logging works.
- [ ] Dashboard loads.
- [ ] No unresolved P0/P1 blockers.
- [ ] No unresolved security/privacy blockers.

Final notes:

```text
TBD
```

Milestone 28E result:

```text
28E - Install/Test Org Final Validation: Complete
Next - 28F Submission Readiness Wrap-up
```
