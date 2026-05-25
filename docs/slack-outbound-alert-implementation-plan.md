# SentinelFlow Slack Outbound Alert Implementation Plan

## 1. Purpose

Open Milestone 35 and define the implementation path for SentinelFlow outbound Slack alerts.

This plan converts the Milestone 33/34 Slack planning and manual validation artifacts into a controlled implementation path.

## 2. Implementation Goal

Implement outbound Slack alerts for SentinelFlow events without changing Salesforce approval, execution, replay, or dashboard behavior.

Core rule:

```text
Outbound Slack alerts only.
No Slack-side approval.
No Slack-side execution.
No autonomous remediation.
Salesforce remains the system of record.
```

## 3. Initial Scope

Implement only these alert types first:

- CRITICAL incident created.
- Approval required.
- Approved action executed.
- Case created.
- Org Health watch, if data is already available.
- Delivery failure, admin-only if configured.

Do not implement:

- Slash commands.
- Read-only command API.
- Interactive Slack buttons.
- Slack approval/rejection.
- Slack execution.
- Slack remediation.
- Agentforce production integration.
- Major AI architecture changes.

## 4. Recommended Technical Path

Recommended first implementation path:

```text
Salesforce SentinelFlow event
-> Apex alert formatter/service
-> Slack webhook or hosted relay
-> approved Slack channel
```

Preferred phase 1 approach:

```text
Salesforce-side formatter + safe outbound delivery abstraction.
```

Reason:

- Keeps alert content close to SentinelFlow records.
- Preserves Salesforce as source of truth.
- Allows tests around message formatting without needing real Slack.
- Keeps secrets out of Git.
- Allows delivery to be disabled by configuration.

## 5. Candidate Salesforce Components

Candidate new/updated Apex components:

- `SentinelFlowSlackAlertService`
- `SentinelFlowSlackAlertServiceTest`
- Optional `SentinelFlowSlackAlertQueueable`
- Optional `SentinelFlowSlackAlertConfig`

Candidate existing references to inspect before coding:

- `SettingsController`
- `SentinelFlow_Settings__c.Slack_Webhook_Path__c`
- `Tenant__c.Slack_Webhook_Path__c`
- `NotificationService`
- `SlackNotificationTest`
- Existing SentinelFlow incident, approval, execution, replay, and dashboard classes.

Implementation rule:

```text
Reuse existing safe settings or notification patterns if they are stable.
Do not wire alerts into production flows until tests and validation pass.
```

## 6. Configuration Strategy

Configuration should support:

- Slack alerts enabled/disabled.
- Minimum risk level.
- Approved channel or webhook path reference.
- Delivery method.
- Admin-only delivery failure target, if available.

Secret handling:

- Do not commit webhook URLs or tokens.
- Prefer storing only a webhook path or secret reference.
- Use Named Credential or protected configuration where practical.
- Logs must not include secret values.

## 7. Message Formatting Strategy

Message formatter should:

- Use templates from `docs/slack-alert-message-templates.md`.
- Include only approved fields.
- Include Salesforce links.
- Avoid raw request/response payloads.
- Avoid secrets.
- Avoid mutating action language.
- Be testable without callouts.

Allowed fields:

- Incident name.
- Incident type.
- Risk score / risk level.
- Policy decision.
- Runbook key.
- Approval status.
- Execution status.
- Created time.
- Salesforce record/dashboard link.

## 8. Delivery Strategy

Recommended delivery options:

Option A: Salesforce callout to Slack webhook

- Simple first implementation.
- Requires secure webhook storage.
- Requires callout test mocking.

Option B: Salesforce callout to hosted API relay

- Hosted API owns Slack credentials.
- Salesforce sends safe alert payload only.
- Requires hosted relay endpoint.

Phase 1 recommendation:

```text
Implement formatter/test harness first, then choose delivery after secret storage is confirmed.
```

## 9. Trigger / Invocation Strategy

Potential invocation points:

- After Sentinel Incident creation for CRITICAL incident.
- After policy marks approval required.
- After approval execution succeeds.
- After Case is created.
- After Org Health status changes, if tracked.

Implementation guardrail:

```text
Do not add trigger-side callouts directly.
Use queueable or async delivery if live callouts are added.
```

## 10. Error Handling

Required behavior:

- Slack failure must not block SentinelFlow incident processing.
- Slack failure must not block approval/execution.
- Delivery errors are logged safely.
- Secrets are not logged.
- Permanent delivery errors are not retried indefinitely.
- Transient errors can be retried conservatively.

## 11. Test Requirements

Required tests:

- Formats CRITICAL incident alert.
- Formats approval-required alert.
- Formats executed-action alert.
- Formats Case-created alert.
- Excludes secrets and raw payloads.
- Includes Salesforce links.
- Does not include approve/reject/execute/remediate controls.
- Handles null/missing fields safely.
- Handles disabled configuration.
- Handles delivery failure without throwing into core flow.

## 12. Validation Requirements

Before live deployment:

- Apex tests pass.
- Existing SentinelFlow tests still pass for touched logic.
- No secrets are committed.
- Static search confirms no Slack token/webhook value in Git.
- Manual alert template validation remains current.
- Salesforce link/security validation remains current.
- Slack app/workspace/channel evidence remains current.

## 13. Rollback Plan

Rollback options:

- Disable Slack alerts through configuration.
- Remove Slack app from channel.
- Rotate/revoke Slack token or webhook.
- Disable hosted relay route if used.
- Revert Apex alert service if needed.

Rollback must not affect:

- Incident creation.
- Approval/rejection.
- Case creation.
- Replay Timeline.
- Dashboard loading.
- Hosted API health.

## 14. Milestone 35 Breakdown

Recommended breakdown:

- 35A - Slack outbound alert implementation plan.
- 35B - Alert formatter/service skeleton.
- 35C - Message formatter tests.
- 35D - Safe delivery abstraction.
- 35E - Delivery failure logging.
- 35F - Salesforce validation.
- 35G - Slack pilot implementation wrap-up.

## 15. Exit Criteria

Milestone 35 can close when:

- Outbound Slack alert code is implemented or explicitly deferred.
- Tests validate formatting and safety behavior.
- No Slack-side approval/execution/remediation exists.
- No secrets are committed.
- Slack failure does not block SentinelFlow core flows.
- Deployment validation passes.
- Documentation and rollback instructions are updated.
