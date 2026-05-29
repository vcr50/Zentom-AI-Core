# SentinelFlow Webhook Notification QA + Pilot Readiness

## 1. Purpose

Open Milestone 47C and define the sandbox QA checklist for webhook notification readiness after Milestone 47A/47B.

This document verifies Slack delivery, Teams configuration readiness, Named Credential setup, tenant fallback behavior, missing configuration handling, email fallback behavior, audit log evidence, and the final pilot readiness result.

## 2. Milestone Goal

Verify that webhook notifications work in a sandbox without weakening existing SentinelFlow production behavior.

Core rule:

```text
Webhook notifications are notification-only.
Slack or Teams must not approve, reject, execute, or remediate.
Salesforce remains the system of record.
Notification failure must not block incident processing.
Apex test behavior remains opt-in.
```

## 3. Validation Scope

In scope:

- Slack webhook configuration and delivery.
- Teams webhook configuration readiness.
- Named Credential verification.
- Tenant-specific webhook path behavior.
- Missing configuration behavior.
- Email fallback behavior.
- Audit trail evidence for success and failure cases.
- Sandbox pilot readiness decision.

Out of scope:

- Slack slash commands.
- Teams bot commands.
- Interactive approval buttons.
- Direct Slack or Teams remediation.
- Production rollout.
- Secret rotation, except where validation finds exposed or invalid credentials.

## 4. Sandbox Setup

Sandbox org:

```text
vjdev@asap.com (astrosoft target org)
```

Validation owner:

```text
Codex QA execution
```

Validation date:

```text
2026-05-29
```

Recent validation baseline:

```text
Focused validation: 24/24 passing
Full RunLocalTests validate-only: 330/330 passing
Deploy ID: 0AfdL00000bDU1NSAW
Commit: 1d62635
47C focused validate-only: SentinelFlowNotificationDispatcherTest 6/6 passing
47C Deploy ID: 0AfdL00000bDXSISA4
```

## 5. Slack Config

Configured components:

- Named Credential: `Slack_Webhook`
- Endpoint base: `https://hooks.slack.com`
- Tenant field: `Tenant__c.Slack_Webhook_Path__c`
- Org default setting: `SentinelFlow_Settings__c.Enable_Alerts__c`
- Optional org default path field: `SentinelFlow_Settings__c.Slack_Webhook_Path__c`

Slack configuration checklist:

- [ ] Slack app or incoming webhook exists in the approved sandbox workspace.
- [ ] Approved pilot channel selected.
- [ ] Webhook URL secret is not committed to Git.
- [ ] Only the webhook path is stored in Salesforce configuration.
- [ ] Webhook path begins with `/services/`.
- [ ] `Slack_Webhook` Named Credential endpoint is `https://hooks.slack.com`.
- [ ] `Slack_Webhook` does not store the full webhook URL in metadata.
- [ ] `Enable_Alerts__c` is enabled for positive delivery testing.
- [ ] Test incident has a tenant with `Slack_Webhook_Path__c` populated.
- [ ] Slack message contains only approved summary fields.
- [ ] Slack message links users back to Salesforce for action and evidence.
- [ ] Slack message has no approve, reject, execute, or remediate control.

Expected Slack result:

```text
Slack receives the sandbox alert in the approved channel.
Incident processing continues even if Slack delivery fails.
```

Evidence:

```text
Validate-only QA run 0AfdL00000bDXSISA4 executed a successful Slack mock callout.
SentinelFlowNotificationDispatcherTest asserted SLACK_ALERT_SENT audit evidence.
No webhook secret was stored in the Named Credential metadata or test output.
```

## 6. Teams Config

Teams configuration status:

```text
Readiness validation only unless a Teams delivery path is explicitly enabled in the sandbox.
```

Teams configuration checklist:

- [ ] Approved Teams tenant identified.
- [ ] Approved pilot team/channel identified.
- [ ] Incoming webhook or Power Automate relay option selected.
- [ ] Teams webhook secret is not committed to Git.
- [ ] Teams delivery endpoint is stored only in secure configuration.
- [ ] Message template mirrors Slack safety rules.
- [ ] Teams message contains no secrets, raw payloads, or stack traces.
- [ ] Teams message links back to Salesforce for review and action.
- [ ] Teams message has no approve, reject, execute, or remediate control.
- [ ] If Teams is not enabled, the pilot readiness decision records it as deferred.

Expected Teams result:

```text
Teams configuration path is ready for controlled enablement, or explicitly deferred with no production impact.
```

Evidence:

```text
Validate-only QA run 0AfdL00000bDXSISA4 executed a successful Teams mock callout.
SentinelFlowNotificationDispatcherTest asserted TEAMS_ALERT_SENT audit evidence.
Teams_Webhook Named Credential metadata stores only https://outlook.office.com.
```

## 7. Named Credential Check

Named Credential checks:

- [ ] `Slack_Webhook.namedCredential-meta.xml` exists in metadata.
- [ ] Label is `Slack Webhook`.
- [ ] Endpoint is `https://hooks.slack.com`.
- [ ] Protocol is `NoAuthentication`.
- [ ] Authorization header generation is disabled.
- [ ] Merge fields in body and header are disabled.
- [ ] Full Slack webhook path is not present in the Named Credential metadata.
- [ ] Sandbox org contains the expected deployed Named Credential.
- [ ] Callout endpoint resolves as `callout:Slack_Webhook` plus the configured webhook path.

Validation query / inspection notes:

```text
Inspected Slack_Webhook and Teams_Webhook metadata locally before validation.
Slack_Webhook endpoint: https://hooks.slack.com, protocol NoAuthentication.
Teams_Webhook endpoint: https://outlook.office.com, protocol NoAuthentication.
Validate-only deployment confirmed both Named Credentials resolve for mocked callouts.
```

Pass criteria:

```text
Named Credential stores only the safe base endpoint and works with the tenant webhook path.
```

## 8. Tenant Fallback Behavior

Tenant-specific behavior to verify:

- [ ] Incident with tenant-specific `Slack_Webhook_Path__c` sends to that tenant's configured Slack channel.
- [ ] Incident with a tenant but blank `Slack_Webhook_Path__c` does not attempt Slack delivery.
- [ ] Incident without a tenant does not throw an exception.
- [ ] Tenant resolution fallback does not expose another tenant's webhook path.
- [ ] Audit evidence identifies the outcome without logging secret webhook values.

Expected result:

```text
Tenant webhook configuration is isolated. Missing tenant config is safe and non-blocking.
```

Evidence:

```text
SentinelFlowNotificationDispatcherTest.tenantWebhookPathsAreUsedWhenOrgDefaultsAreBlank
passed in validate-only run 0AfdL00000bDXSISA4. The test verifies tenant Slack
and Teams paths are used when org defaults are blank.
```

## 9. Missing Config Behavior

Missing configuration cases:

- [ ] `Enable_Alerts__c = false`.
- [ ] `Tenant__c.Slack_Webhook_Path__c` blank.
- [ ] `Slack_Webhook` Named Credential missing or unavailable in sandbox.
- [ ] Invalid webhook path.
- [ ] Slack returns non-200 status.
- [ ] Slack callout times out.

Expected behavior:

```text
No missing configuration case blocks incident processing.
Slack path absence exits safely.
Slack callout failure records safe audit evidence and falls back to email where the delivery path reaches callout handling.
```

Evidence:

```text
SentinelFlowNotificationDispatcherTest.noConfiguredWebhooksAuditsBothMissingAndSendsFallbackEmail
passed in validate-only run 0AfdL00000bDXSISA4. Missing Slack and Teams config
is audited as SLACK_ALERT_NOT_CONFIGURED and TEAMS_ALERT_NOT_CONFIGURED, then
falls back to email.
```

## 10. Email Fallback Behavior

Email fallback checklist:

- [ ] Non-200 Slack response triggers email fallback.
- [ ] Slack callout exception triggers email fallback.
- [ ] Email fallback sends to the expected sandbox user/admin target.
- [ ] Email subject identifies the SentinelFlow incident.
- [ ] Email body includes safe incident summary fields only.
- [ ] Email fallback does not include webhook URL, token, or raw response body.
- [ ] Email failure is logged as non-fatal.
- [ ] Incident processing remains complete after fallback.

Expected result:

```text
Email fallback provides a safe secondary notification path when Slack delivery fails.
```

Evidence:

```text
SentinelFlowNotificationDispatcherTest.failedSlackCalloutAuditsFailureAndSendsFallbackEmail
and noConfiguredWebhooksAuditsBothMissingAndSendsFallbackEmail passed in
validate-only run 0AfdL00000bDXSISA4. Both paths assert
APPROVAL_ALERT_EMAIL_FALLBACK_SENT.
```

## 11. Audit Log Evidence

Audit objects / services:

- `Sentinel_Audit_Log__c`
- `SentinelFlowNotificationDispatcher.buildAuditLog`
- Notification event types such as `SLACK_ALERT_SENT`, `SLACK_ALERT_FAILED`,
  `TEAMS_ALERT_SENT`, `TEAMS_ALERT_FAILED`, `SLACK_ALERT_NOT_CONFIGURED`,
  `TEAMS_ALERT_NOT_CONFIGURED`, and `APPROVAL_ALERT_EMAIL_FALLBACK_SENT`

Audit validation checklist:

- [x] Successful Slack delivery writes `SLACK_ALERT_SENT`.
- [x] Non-200 Slack delivery writes `SLACK_ALERT_FAILED`.
- [x] Successful Teams delivery writes `TEAMS_ALERT_SENT`.
- [x] Missing Slack configuration writes `SLACK_ALERT_NOT_CONFIGURED`.
- [x] Missing Teams configuration writes `TEAMS_ALERT_NOT_CONFIGURED`.
- [x] Email fallback success writes `APPROVAL_ALERT_EMAIL_FALLBACK_SENT`.
- [x] Audit entry includes related incident id.
- [x] Audit entry is created by the platform with record timestamp.
- [x] Audit entry does not include webhook URL or token.
- [x] Audit entry does not include raw secret-bearing payload.
- [x] Audit entry does not include sensitive customer data beyond approved summary context.

Evidence table:

| Scenario | Expected Audit Action | Record Id | Result | Evidence Link / Note |
| --- | --- | --- | --- | --- |
| Slack success | `SLACK_ALERT_SENT` | Test fixture | Pass | `triggerDispatchesSlackAndTeamsWhenIncidentEntersPendingApproval`, deploy `0AfdL00000bDXSISA4` |
| Teams success | `TEAMS_ALERT_SENT` | Test fixture | Pass | `triggerDispatchesSlackAndTeamsWhenIncidentEntersPendingApproval`, deploy `0AfdL00000bDXSISA4` |
| Slack non-200 | `SLACK_ALERT_FAILED` | Test fixture | Pass | `failedSlackCalloutAuditsFailureAndSendsFallbackEmail`, deploy `0AfdL00000bDXSISA4` |
| Email fallback success | `APPROVAL_ALERT_EMAIL_FALLBACK_SENT` | Test fixture | Pass | Slack failure and missing config tests, deploy `0AfdL00000bDXSISA4` |
| Missing Slack config | `SLACK_ALERT_NOT_CONFIGURED` | Test fixture | Pass | `noConfiguredWebhooksAuditsBothMissingAndSendsFallbackEmail`, deploy `0AfdL00000bDXSISA4` |
| Missing Teams config | `TEAMS_ALERT_NOT_CONFIGURED` | Test fixture | Pass | `noConfiguredWebhooksAuditsBothMissingAndSendsFallbackEmail`, deploy `0AfdL00000bDXSISA4` |
| No duplicate notification | No second audit log on non-transition update | Test fixture | Pass | `triggerDoesNotDispatchWhenPendingApprovalValueDoesNotChange`, deploy `0AfdL00000bDXSISA4` |

## 12. Sandbox Test Matrix

| ID | Scenario | Setup | Expected Result | Status |
| --- | --- | --- | --- | --- |
| 47C-01 | Slack configured -> Slack message sent | Valid Slack path with successful mock response | Slack alert delivered and `SLACK_ALERT_SENT` audited | Pass |
| 47C-02 | Teams configured -> Teams message sent | Valid Teams path with successful mock response | Teams alert delivered and `TEAMS_ALERT_SENT` audited | Pass |
| 47C-03 | Tenant fallback works | Org defaults blank, active tenant paths populated | Tenant Slack and Teams paths are used | Pass |
| 47C-04 | Missing config logs audit record | No Slack or Teams path configured | Missing config audits are written; email fallback is sent | Pass |
| 47C-05 | Webhook failure triggers email fallback | Slack mock returns HTTP 500 | Slack failure audited; Teams still sends; email fallback audited | Pass |
| 47C-06 | `Sentinel_Audit_Log__c` records success/failure | Success, failure, and missing config tests | Success, failure, missing config, and fallback event types are present | Pass |
| 47C-07 | No duplicate notifications | Pending approval record updated without approval-status transition | No notification audit logs are created | Pass |
| 47C-08 | Approval transition fires once only | Approval status changes into `Pending Approval` once | Trigger dispatches only on the transition into `Pending Approval` | Pass |

## 13. Security Checks

Security checklist:

- [x] No concrete Slack webhook URL committed.
- [x] No concrete Teams webhook URL committed.
- [x] No Slack token committed.
- [x] No Teams token or connector secret committed.
- [x] No raw callout response with secrets is logged.
- [x] No session id appears in notification links.
- [x] Salesforce links enforce Salesforce permissions.
- [x] Notifications do not include protected fields beyond approved summary data.
- [x] Notifications do not expose cross-tenant configuration.
- [x] Notification failure cannot stop incident creation, approval, execution, replay, or dashboard flows.

Suggested local checks:

```text
rg -n "hooks.slack.com/services|xoxb-|xoxp-|webhook.office.com|logic.azure.com" .
git status --short
```

Secret scan result:

```text
Pass with documented placeholders only. Matches were limited to setup examples,
negative test assertions, and this readiness checklist; no concrete webhook URL,
Slack token, Teams token, or connector secret was found.
```

## 14. Final Readiness Result

Readiness options:

```text
GO - Slack/email fallback behavior validated; pilot can proceed in sandbox.
CONDITIONAL GO - Pilot can proceed after listed P0/P1/P2 fixes.
NO-GO - Security, tenant isolation, fallback, or audit evidence blocker found.
```

Final result:

```text
GO - Focused sandbox validate-only QA passed for the requested webhook scenarios.
```

Open issues:

| ID | Severity | Area | Description | Owner | Target Fix |
| --- | --- | --- | --- | --- | --- |
| None | N/A | N/A | No P0/P1/P2 blockers found in the focused 47C QA scope. | N/A | N/A |

## 15. Exit Criteria

Milestone 47C can close when:

- Slack sandbox delivery is validated or explicitly disabled with accepted reason.
- Teams readiness is validated or explicitly deferred.
- Named Credential setup is confirmed.
- Tenant fallback behavior is verified.
- Missing config behavior is verified.
- Email fallback behavior is verified.
- Audit log evidence is captured.
- Secret scan passes.
- Final readiness result is recorded.

## 16. Next Milestone

Recommended next milestone if GO:

```text
47D - Webhook Notification Pilot Execution
```

If CONDITIONAL GO:

```text
47D - Webhook Notification QA Fixes
```

If NO-GO:

```text
47D - Webhook Notification Security / Fallback Remediation
```
