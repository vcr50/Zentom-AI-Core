# SentinelFlow Slack Security Validation Plan

## 1. Purpose

Define the security validation plan for the SentinelFlow Slack assistant before any pilot or production Slack integration is enabled.

This plan applies to:

- Outbound Slack alerts.
- Future read-only Slack commands.
- Hosted API relay paths, if selected.
- Slack app/workspace configuration.

## 2. Security Goal

Prove that Slack integration increases visibility without weakening SentinelFlow governance.

Core security goal:

```text
Slack can notify and summarize.
Salesforce remains the system of record.
Approval, rejection, execution, and audit remain in Salesforce.
```

## 3. Validation Scope

In scope:

- Slack app ownership.
- Workspace and channel restrictions.
- Bot token / webhook / signing secret handling.
- Outbound alert message content.
- Read-only command authorization design.
- Salesforce link behavior.
- Delivery failure logging.
- Privacy-safe screenshots and demo data.
- Rollback controls.

Out of scope:

- Slack-side approval.
- Slack-side execution.
- Slack-side remediation.
- Production Agentforce integration.
- Hosted HYBRID Ollama.
- Broad autonomous agent behavior.

## 4. Governance Controls

Required controls:

- [ ] Slack integration is notification/read-only only.
- [ ] No Slack message includes Approve, Reject, Execute, Remediate, or Run Action controls.
- [ ] Slack links open Salesforce for governed actions.
- [ ] Human approval remains in Salesforce.
- [ ] Execution remains controlled by existing SentinelFlow logic.
- [ ] Replay/audit evidence remains in Salesforce.
- [ ] Salesforce permissions still protect linked records.

## 5. Workspace / Channel Validation

Validate:

- [ ] Target Slack workspace is approved.
- [ ] Slack app owner is identified.
- [ ] Allowed channels are documented.
- [ ] App is installed only in approved workspace/channel.
- [ ] Test messages do not post to unrelated channels.
- [ ] Pilot users understand Slack is notification-only.
- [ ] Workspace retention policy is understood.

Evidence to capture:

- Workspace name.
- App owner.
- Approved channel names.
- Install approval owner.
- Screenshot of app/channel configuration with secrets hidden.

## 6. Credential / Secret Validation

Validate:

- [ ] Slack bot token is not committed to Git.
- [ ] Slack webhook URL is not committed to Git.
- [ ] Slack signing secret is not committed to Git.
- [ ] Credentials are stored in approved secret storage.
- [ ] Secrets are not printed in logs.
- [ ] Secrets are not shown in screenshots.
- [ ] Rotation owner is documented.
- [ ] Rotation steps are documented.

Evidence to capture:

- Secret storage location name, not secret value.
- Git search showing no Slack token/webhook/signing secret committed.
- Log review showing no secret exposure.

Search patterns:

```text
xoxb-
xapp-
hooks.slack.com/services
SLACK_BOT_TOKEN
SLACK_SIGNING_SECRET
SLACK_WEBHOOK_URL
```

## 7. Message Content Validation

Validate every Slack template:

- [ ] Message includes only allowed fields.
- [ ] Message includes Salesforce link.
- [ ] Message does not include raw payloads.
- [ ] Message does not include API keys or tokens.
- [ ] Message does not include customer secrets.
- [ ] Message does not include long AI reasoning traces.
- [ ] Message avoids mutating action wording.
- [ ] Message is readable on desktop and mobile.

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

## 8. Authorization Validation

Outbound alerts:

- [ ] Only approved channels receive alerts.
- [ ] Channel membership is reviewed for pilot/demo use.
- [ ] Sensitive data is not posted to broad public channels.

Read-only commands, if implemented later:

- [ ] Allowed workspace is enforced.
- [ ] Allowed channel or user allowlist is enforced.
- [ ] Unauthorized users receive access denied.
- [ ] Commands do not grant Salesforce access.
- [ ] Salesforce links still require Salesforce permissions.

## 9. Inbound Request Validation

Applies only if slash commands or Slack events are implemented later.

Validate:

- [ ] Slack signature verification is implemented.
- [ ] Timestamp replay protection is implemented.
- [ ] Invalid signatures are rejected.
- [ ] Old timestamps are rejected.
- [ ] Request body is not logged with secrets.
- [ ] Rate limiting or abuse protection is considered.

Do not enable inbound commands until this section passes.

## 10. Salesforce Permission Validation

Validate:

- [ ] Linked Sentinel Incident records require Salesforce access.
- [ ] Linked Case records require Salesforce access.
- [ ] Linked dashboard requires Salesforce access.
- [ ] Viewer users remain read-only.
- [ ] Approver users still approve only in Salesforce.
- [ ] Slack user identity is not treated as Salesforce authorization.

Evidence:

- Authorized user can open linked record.
- Unauthorized user cannot open linked record.
- Slack message does not include data that bypasses Salesforce permissions.

## 11. Logging / Audit Validation

Validate logs include:

- Alert event type.
- Safe incident reference.
- Safe channel alias.
- Delivery status.
- Attempt count.
- Safe error category.
- Timestamp.

Validate logs exclude:

- Slack token.
- Webhook URL.
- Signing secret.
- Full Slack response body.
- Full Salesforce payload.
- API keys.
- Customer secrets.

## 12. Failure Mode Validation

Test:

- Invalid Slack channel.
- Revoked token or webhook.
- Slack API rate limit.
- Hosted API relay unavailable.
- Salesforce link access denied.
- Alert delivery retry exhaustion.

Expected behavior:

- Failure is logged safely.
- No secret appears in error.
- SentinelFlow core incident/approval/execution flow continues.
- Slack failure does not block Salesforce operations.

## 13. Privacy / Demo Data Validation

Before screenshots or demos:

- [ ] Use demo/sample incident data.
- [ ] Hide workspace ids if needed.
- [ ] Hide Slack app secrets.
- [ ] Hide personal user names if not approved.
- [ ] Hide customer org ids unless intentionally shown.
- [ ] Confirm no API keys or tokens appear.
- [ ] Confirm no raw payloads appear.

## 14. Rollback Validation

Rollback actions:

- Disable Slack alerts.
- Remove app from channel.
- Revoke bot token.
- Rotate webhook/signing secret.
- Disable hosted relay route.
- Revert integration code/metadata if needed.

Validate rollback does not break:

- Sentinel Incident creation.
- Approval/rejection in Salesforce.
- Case creation.
- Replay Timeline.
- Dashboard loading.
- Hosted API health.

## 15. Pass / Fail Criteria

Pass:

- Alerts are notification-only.
- Secrets are not exposed.
- Messages contain minimum necessary data.
- Unauthorized users cannot use Slack to bypass Salesforce access.
- Failures are logged safely.
- Rollback is documented and tested.

Fail:

- Slack can approve, reject, execute, or remediate.
- Slack message exposes secrets or raw payloads.
- Slack link bypasses Salesforce permissions.
- Invalid inbound Slack requests are accepted.
- Slack delivery failure blocks core SentinelFlow workflow.

## 16. Validation Evidence Checklist

Required evidence:

- [ ] Slack app/workspace setup checklist completed.
- [ ] Message templates reviewed.
- [ ] Allowed channel screenshot captured with secrets hidden.
- [ ] Secret search completed.
- [ ] Test alert screenshot captured with demo data.
- [ ] Salesforce link access test completed.
- [ ] Unauthorized access test completed.
- [ ] Delivery failure test completed.
- [ ] Rollback test completed.
- [ ] Final security result recorded.

## 17. Exit Criteria

33F is complete when:

- Security validation scope is documented.
- Credential handling checks are documented.
- Message content checks are documented.
- Authorization checks are documented.
- Inbound request checks are documented for later commands.
- Salesforce permission checks are documented.
- Logging/audit and failure-mode checks are documented.
- Rollback and pass/fail criteria are documented.
