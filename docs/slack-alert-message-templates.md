# SentinelFlow Slack Alert Message Templates

## 1. Purpose

Define privacy-safe Slack alert templates for the first SentinelFlow Slack assistant phase.

Phase 1 remains outbound-alert-only:

```text
No Slack-side approval.
No Slack-side execution.
No autonomous remediation.
Salesforce remains the system of record.
```

## 2. Message Principles

Slack messages should be:

- Short enough to scan quickly.
- Clear about risk and required action.
- Linked back to Salesforce for review, approval, execution, and audit.
- Free of secrets, raw payloads, tokens, and sensitive customer data.
- Consistent with SentinelFlow control-tower language.

## 3. Shared Message Fields

Allowed fields:

- Incident name.
- Incident type.
- Risk level.
- Risk score.
- Policy decision.
- Recommendation status.
- Runbook key.
- Approval status.
- Execution status.
- Created time.
- Salesforce record link.

Never include:

- API keys.
- Slack tokens.
- Salesforce session ids.
- Webhook URLs.
- Full request or response payloads.
- Customer secrets.
- Sensitive personal data.
- Long AI reasoning traces.

## 4. CRITICAL Incident Alert

Trigger:

```text
New Sentinel Incident created with Risk Level = CRITICAL.
```

Template:

```text
:rotating_light: SentinelFlow critical incident
Incident: <IncidentName>
Type: <IncidentType>
Risk: <RiskScore> / <RiskLevel>
Policy: <PolicyDecision>
Runbook: <RunbookKey>

Review in Salesforce: <IncidentLink>
```

Operator meaning:

```text
Critical traffic detected. Review the incident in Salesforce before action.
```

## 5. Approval Required Alert

Trigger:

```text
Policy Decision = HUMAN_APPROVAL_REQUIRED or Status = Approval Required.
```

Template:

```text
:warning: SentinelFlow clearance required
Incident: <IncidentName>
Risk: <RiskScore> / <RiskLevel>
Recommended action: <RecommendedAction>
Runbook: <RunbookKey>

Approve or reject in Salesforce: <IncidentLink>
```

Operator meaning:

```text
The incident is waiting for human clearance in Salesforce.
```

## 6. Approved Action Executed Alert

Trigger:

```text
Execution Status = Executed.
```

Template:

```text
:white_check_mark: SentinelFlow cleared action executed
Incident: <IncidentName>
Action: <ExecutionAction>
Status: <ExecutionStatus>
Executed at: <ExecutedAt>

View execution evidence: <IncidentLink>
```

Operator meaning:

```text
A governed action was executed after approval.
```

## 7. Case Created Alert

Trigger:

```text
Created Case is populated after approved execution.
```

Template:

```text
:page_with_curl: SentinelFlow case created
Incident: <IncidentName>
Case: <CaseNumber>
Action: <ExecutionAction>

Open Case: <CaseLink>
Open Incident: <IncidentLink>
```

Operator meaning:

```text
SentinelFlow created a Salesforce Case from an approved incident action.
```

## 8. Org Health Watch Alert

Trigger:

```text
Org Health status changes to At Risk or Critical.
```

Template:

```text
:satellite: SentinelFlow org health watch
Status: <OrgHealthStatus>
Score: <OrgHealthScore> / 100
Reason: <OrgHealthReason>

Open Command Center: <DashboardLink>
```

Operator meaning:

```text
The control tower posture changed and should be reviewed.
```

## 9. Replay / Audit Ready Alert

Trigger:

```text
Replay Timeline has enough events to support incident review.
```

Template:

```text
:black_square_for_stop: SentinelFlow flight recorder ready
Incident: <IncidentName>
Latest event: <LatestReplayEvent>
Decision: <Decision>

Open Replay Timeline: <IncidentLink>
```

Operator meaning:

```text
Audit evidence is available in Salesforce for this incident.
```

## 10. Error / Delivery Failure Alert

Trigger:

```text
Slack alert delivery fails or SentinelFlow detects an alerting issue.
```

Template:

```text
:grey_exclamation: SentinelFlow alert delivery issue
Context: <SafeContext>
Status: <DeliveryStatus>
Time: <CreatedAt>

Review system health: <DashboardLink>
```

Operator meaning:

```text
Alert delivery needs review. Do not include raw error payloads in Slack.
```

## 11. Link Button Labels

Recommended link labels:

- Open Command Center
- Review Incident
- View Replay Timeline
- Open Case
- View System Health

Avoid:

- Approve
- Reject
- Execute
- Remediate
- Run Action

## 12. Formatting Rules

Formatting checklist:

- [ ] Message starts with clear SentinelFlow event type.
- [ ] Risk and policy are visible near the top.
- [ ] Salesforce link is included.
- [ ] No secrets or sensitive payloads are included.
- [ ] No direct mutating action button is included.
- [ ] Message works without relying on color alone.
- [ ] Message remains readable on desktop and mobile Slack.

## 13. Template Validation

Before implementation:

- [ ] Templates reviewed by product owner.
- [ ] Templates reviewed for privacy/security.
- [ ] Demo/sample data rendered in Slack.
- [ ] Links tested against the target Salesforce org.
- [ ] No secrets appear in screenshots.
- [ ] Channel recipients understand Slack is notification-only.

## 14. Exit Criteria

33C is complete when:

- CRITICAL incident template is approved.
- Approval-required template is approved.
- Executed-action template is approved.
- Case-created template is approved.
- Org Health watch template is approved.
- Replay/audit template is approved.
- Delivery failure template is approved.
- All templates link back to Salesforce for action.
