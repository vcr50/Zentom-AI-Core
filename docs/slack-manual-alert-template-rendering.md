# SentinelFlow Slack Manual Alert Template Rendering

## 1. Purpose

Define the manual rendering checklist for SentinelFlow Slack alert templates before automated Slack delivery is implemented.

Manual rendering proves that messages are useful, safe, scannable, and aligned with the SentinelFlow control-tower model.

## 2. Rendering Rule

Manual rendering must use safe demo data only:

```text
No real customer secrets.
No API keys.
No webhook URLs.
No Slack tokens.
No Salesforce session ids.
No raw request/response payloads.
No Slack-side approval or execution.
```

## 3. Demo Data Set

Recommended demo values:

```text
Incident: SI-000013
Type: FLOW_FAILURE
Risk: 95 / CRITICAL
Policy: HUMAN_APPROVAL_REQUIRED
Runbook: FLOW_FAILURE_BASIC_RECOVERY
Approval: Pending Approval
Execution: Not Started
Case: 00001051
Org Health: Critical
Org Health Score: 0 / 100
Latest Replay Event: RUNBOOK_ACTION_EXECUTED
```

Salesforce links:

```text
Command Center: TBD
Incident: TBD
Case: TBD
Replay Timeline: TBD
```

## 4. Rendering Workspace / Channel

Workspace:

```text
TBD
```

Channel:

```text
TBD
```

Renderer:

```text
TBD
```

Validation date:

```text
TBD
```

## 5. CRITICAL Incident Alert Rendering

Template:

```text
:rotating_light: SentinelFlow critical incident
Incident: SI-000013
Type: FLOW_FAILURE
Risk: 95 / CRITICAL
Policy: HUMAN_APPROVAL_REQUIRED
Runbook: FLOW_FAILURE_BASIC_RECOVERY

Review in Salesforce: <IncidentLink>
```

Checklist:

- [ ] Message renders clearly in Slack.
- [ ] Risk and policy are visible.
- [ ] Salesforce link is present.
- [ ] No secrets or raw payloads appear.
- [ ] No approve/reject/execute control appears.

Result:

```text
TBD
```

## 6. Approval Required Alert Rendering

Template:

```text
:warning: SentinelFlow clearance required
Incident: SI-000013
Risk: 95 / CRITICAL
Recommended action: CREATE_CASE
Runbook: FLOW_FAILURE_BASIC_RECOVERY

Approve or reject in Salesforce: <IncidentLink>
```

Checklist:

- [ ] Message clearly says clearance is required.
- [ ] Salesforce remains the approval location.
- [ ] No Slack-side approval button appears.
- [ ] No sensitive data appears.
- [ ] Message is understandable on mobile.

Result:

```text
TBD
```

## 7. Approved Action Executed Alert Rendering

Template:

```text
:white_check_mark: SentinelFlow cleared action executed
Incident: SI-000013
Action: CREATE_CASE
Status: Executed
Executed at: 2026-05-25 23:04:50

View execution evidence: <IncidentLink>
```

Checklist:

- [ ] Message clearly says action already executed.
- [ ] Message does not imply Slack executed the action.
- [ ] Incident evidence link is present.
- [ ] No secrets or payloads appear.

Result:

```text
TBD
```

## 8. Case Created Alert Rendering

Template:

```text
:page_with_curl: SentinelFlow case created
Incident: SI-000013
Case: 00001051
Action: CREATE_CASE

Open Case: <CaseLink>
Open Incident: <IncidentLink>
```

Checklist:

- [ ] Case number is visible.
- [ ] Case link opens Salesforce.
- [ ] Incident link opens Salesforce.
- [ ] No session id or token appears in links.
- [ ] Message is short and scannable.

Result:

```text
TBD
```

## 9. Org Health Watch Alert Rendering

Template:

```text
:satellite: SentinelFlow org health watch
Status: Critical
Score: 0 / 100
Reason: 8 critical open incidents, 4 pending approvals, and 1 rejected recommendation reduced the score.

Open Command Center: <DashboardLink>
```

Checklist:

- [ ] Status is clear.
- [ ] Score is visible.
- [ ] Reason is concise.
- [ ] Command Center link is present.
- [ ] Message does not expose sensitive data.

Result:

```text
TBD
```

## 10. Replay / Audit Ready Alert Rendering

Template:

```text
:black_square_for_stop: SentinelFlow flight recorder ready
Incident: SI-000013
Latest event: RUNBOOK_ACTION_EXECUTED
Decision: APPROVED

Open Replay Timeline: <IncidentLink>
```

Checklist:

- [ ] Flight recorder language is understandable.
- [ ] Latest event is visible.
- [ ] Decision is visible.
- [ ] Link opens Salesforce.
- [ ] No raw audit payload is shown.

Result:

```text
TBD
```

## 11. Alert Delivery Issue Rendering

Template:

```text
:grey_exclamation: SentinelFlow alert delivery issue
Context: Slack channel delivery failed
Status: Failed Transient
Time: 2026-05-25 23:10:00

Review system health: <DashboardLink>
```

Checklist:

- [ ] Error context is safe.
- [ ] No raw Slack response body appears.
- [ ] No token/webhook appears.
- [ ] System health link is present.
- [ ] Message is suitable for admin-only channel if needed.

Result:

```text
TBD
```

## 12. Overall Rendering Result

Result options:

```text
PASS - Templates are safe and ready for link/security validation.
CONDITIONAL PASS - Fix listed template issues first.
FAIL - Security/privacy/governance issue found.
```

Overall result:

```text
TBD
```

## 13. Issues / Fixes

| ID | Severity | Template | Issue | Owner | Target Fix |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

## 14. Exit Criteria

34C is complete when:

- All required templates are manually rendered.
- Messages are readable in Slack.
- Messages use demo/sample data only.
- Salesforce links are included as placeholders or safe test links.
- No secrets or raw payloads are visible.
- No Slack-side approve/reject/execute/remediate controls appear.
- Overall rendering result is recorded.
