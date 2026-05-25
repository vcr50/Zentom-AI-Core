# SentinelFlow Slack Outbound Alert Integration Plan

## 1. Purpose

Define the first implementation path for SentinelFlow Slack alerts.

The integration should start with outbound notifications only:

```text
Salesforce/SentinelFlow event -> controlled alert service -> Slack channel.
```

No Slack-side approval, execution, or autonomous remediation is included in this plan.

## 2. Integration Goal

Send privacy-safe SentinelFlow incident alerts to an approved Slack channel so operators know when critical traffic, approval clearance, executed actions, or Case creation needs attention.

Slack is a notification surface. Salesforce remains the system of record for review, approval, execution, and audit.

## 3. Recommended Phase 1 Architecture

Recommended path:

```text
Salesforce SentinelFlow event
-> existing SentinelFlow/Apex alert decision point
-> outbound callout or hosted API relay
-> Slack chat.postMessage / webhook
-> approved Slack channel
```

Preferred implementation order:

1. Use approved message templates.
2. Send only minimum allowed fields.
3. Link back to Salesforce records.
4. Log delivery success/failure without secrets.
5. Keep approval/execution inside Salesforce.

## 4. Alert Triggers

Initial triggers:

- CRITICAL incident created.
- Approval required.
- Approved action executed.
- Case created.
- Org Health changes to At Risk or Critical.
- Slack delivery failure detected.

Deferred triggers:

- Daily digest.
- Weekly adoption summary.
- Read-only slash-command response.
- Customer-specific routing rules.
- Direct Slack workflow buttons.

## 5. Routing Rules

Default channel:

```text
#sentinelflow-alerts
```

Optional pilot channel:

```text
#sentinelflow-pilot
```

Routing rules:

- CRITICAL incidents go to the approved alert channel.
- Approval-required incidents go to the approved alert channel.
- Case-created alerts go to the approved alert channel.
- Delivery failures go to an internal/admin-only channel if configured.
- No customer-specific channel routing until explicitly configured.

## 6. Payload Contract

Allowed outbound payload:

```json
{
  "eventType": "CRITICAL_INCIDENT",
  "incidentName": "SI-000013",
  "incidentType": "FLOW_FAILURE",
  "riskScore": 95,
  "riskLevel": "CRITICAL",
  "policyDecision": "HUMAN_APPROVAL_REQUIRED",
  "runbookKey": "FLOW_FAILURE_BASIC_RECOVERY",
  "approvalStatus": "Pending Approval",
  "executionStatus": "Not Started",
  "createdAt": "2026-05-25T00:00:00Z",
  "salesforceRecordUrl": "https://example.lightning.force.com/lightning/r/Sentinel_Incident__c/..."
}
```

Do not include:

- Request payload.
- Response payload.
- API keys.
- Slack tokens.
- Salesforce session ids.
- Customer secrets.
- Raw exception stack traces.
- Long AI reasoning.

## 7. Delivery Method Options

Option A: Slack incoming webhook

- Simple outbound delivery.
- Good for phase 1 demos.
- Webhook URL must be stored securely.
- Limited interaction model.

Option B: Slack Web API `chat.postMessage`

- Uses bot token.
- Better long-term app model.
- Supports richer blocks and future commands.
- Requires secure bot token storage.

Option C: Hosted API relay

- Salesforce calls hosted SentinelFlow/Zentom API.
- Hosted API owns Slack signing/token logic.
- Easier to rotate Slack credentials outside Salesforce.
- Requires hosted API endpoint hardening and logging.

Recommended:

```text
Start with Option C if hosted API ownership is preferred.
Use Option A only for a short demo spike.
```

## 8. Error Handling

Error handling requirements:

- Retry transient Slack delivery failures conservatively.
- Do not retry permanent permission/channel failures indefinitely.
- Log safe error context only.
- Do not log Slack tokens, webhook URLs, or full response bodies.
- Surface delivery issues in SentinelFlow system health if implemented later.

Delivery statuses:

- Pending
- Sent
- Failed Transient
- Failed Permanent
- Suppressed

## 9. Logging / Audit

Minimum delivery log fields:

- Alert event type.
- Sentinel Incident id.
- Channel alias, not secret URL.
- Delivery status.
- Attempt count.
- Safe error category.
- Created time.
- Last attempt time.

Avoid storing:

- Slack token.
- Webhook URL.
- Full Slack response body.
- Full SentinelFlow incident payload.
- User private data.

## 10. Configuration

Configuration items:

- Slack alerts enabled.
- Target channel id or safe alias.
- Slack delivery method.
- Alert trigger toggles.
- Minimum risk level.
- Hosted relay URL, if used.
- Secret reference name, not secret value.

Configuration rule:

```text
No Slack credentials should be committed to Git.
```

## 11. Security Requirements

Before implementation:

- Confirm Slack workspace and app owner.
- Confirm approved target channel.
- Confirm credential storage location.
- Confirm no direct Slack approval or execution.
- Confirm message templates are privacy reviewed.
- Confirm no raw payloads or secrets are sent.
- Confirm Slack retention and workspace policy are acceptable.

## 12. Validation Plan

Validation should prove:

- CRITICAL alert sends to approved channel.
- Approval-required alert sends to approved channel.
- Case-created alert sends after approved execution.
- Links open the correct Salesforce record.
- Unauthorized Slack users cannot access Salesforce records without Salesforce permission.
- Delivery failures are logged safely.
- No secrets appear in Slack or logs.
- Existing SentinelFlow approval/execution/replay behavior is unchanged.

## 13. Rollback Plan

Rollback options:

- Disable Slack alerts via configuration.
- Remove app from channel.
- Rotate Slack token or webhook URL.
- Disable hosted API relay route.
- Revert integration metadata/code if implementation causes regression.

Rollback must not affect:

- SentinelFlow incident creation.
- Salesforce approval flow.
- Case creation execution.
- Replay Timeline.
- Dashboard loading.

## 14. Implementation Readiness Criteria

Implementation can start only when:

- Slack app/workspace setup checklist is complete.
- Message templates are approved.
- Delivery method is selected.
- Secret storage plan is approved.
- Alert triggers are accepted.
- Validation plan is accepted.
- Product owner confirms outbound-alert-only scope.
