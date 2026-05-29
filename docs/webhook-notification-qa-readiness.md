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
TBD
```

Validation owner:

```text
TBD
```

Validation date:

```text
TBD
```

Recent validation baseline:

```text
Focused validation: 24/24 passing
Full RunLocalTests validate-only: 330/330 passing
Deploy ID: 0AfdL00000bDU1NSAW
Commit: 1d62635
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
TBD - Add screenshot or audit trail reference with webhook secrets hidden.
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
TBD - Add Teams config screenshot or deferment note with secrets hidden.
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
TBD
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
TBD
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
TBD
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
TBD - Add email delivery screenshot or Salesforce email log reference.
```

## 11. Audit Log Evidence

Audit objects / services:

- `Audit_Trail__c`
- `AuditTrailService.log`
- Notification actions such as `Slack Alert Sent`, `Slack Alert Failed`, `Alert Sent`, and `Alert Failed`

Audit validation checklist:

- [ ] Successful Slack delivery writes `Slack Alert Sent`.
- [ ] Non-200 Slack delivery writes `Slack Alert Failed`.
- [ ] Slack exception writes `Slack Alert Failed`.
- [ ] Email fallback success writes `Alert Sent`.
- [ ] Email fallback failure writes `Alert Failed`.
- [ ] Audit entry includes related record id where available.
- [ ] Audit entry includes timestamp.
- [ ] Audit entry includes running user where available.
- [ ] Audit entry does not include webhook URL or token.
- [ ] Audit entry does not include raw request payload.
- [ ] Audit entry does not include sensitive customer data beyond approved summary context.

Evidence table:

| Scenario | Expected Audit Action | Record Id | Result | Evidence Link / Note |
| --- | --- | --- | --- | --- |
| Slack success | Slack Alert Sent | TBD | TBD | TBD |
| Slack non-200 | Slack Alert Failed | TBD | TBD | TBD |
| Slack exception | Slack Alert Failed | TBD | TBD | TBD |
| Email fallback success | Alert Sent | TBD | TBD | TBD |
| Email fallback failure | Alert Failed | TBD | TBD | TBD |
| Alerts disabled | No delivery attempt / safe exit | TBD | TBD | TBD |
| Missing webhook path | No Slack attempt / safe exit | TBD | TBD | TBD |

## 12. Sandbox Test Matrix

| ID | Scenario | Setup | Expected Result | Status |
| --- | --- | --- | --- | --- |
| 47C-01 | Slack success | Valid tenant webhook path | Slack alert delivered and audited | TBD |
| 47C-02 | Alerts disabled | `Enable_Alerts__c = false` | No outbound alert; incident processing continues | TBD |
| 47C-03 | Missing tenant webhook | Blank `Tenant__c.Slack_Webhook_Path__c` | Safe exit; no exception | TBD |
| 47C-04 | Invalid Slack path | Bad webhook path | Slack failure audited; email fallback attempted | TBD |
| 47C-05 | Slack non-200 | Mock or invalid endpoint response | Slack failure audited; email fallback attempted | TBD |
| 47C-06 | Slack exception | Callout exception path | Slack failure audited; email fallback attempted | TBD |
| 47C-07 | Email fallback success | Current user/admin email available | Email sent; audit entry written | TBD |
| 47C-08 | Email fallback failure | Simulated email send issue if practical | Failure logged; core flow continues | TBD |
| 47C-09 | Teams deferred | No Teams delivery path enabled | Deferment recorded; no production impact | TBD |
| 47C-10 | Secret scan | Search metadata/docs/code | No webhook secrets committed | TBD |

## 13. Security Checks

Security checklist:

- [ ] No Slack webhook URL committed.
- [ ] No Teams webhook URL committed.
- [ ] No Slack token committed.
- [ ] No Teams token or connector secret committed.
- [ ] No raw callout response with secrets is logged.
- [ ] No session id appears in notification links.
- [ ] Salesforce links enforce Salesforce permissions.
- [ ] Notifications do not include protected fields beyond approved summary data.
- [ ] Notifications do not expose cross-tenant configuration.
- [ ] Notification failure cannot stop incident creation, approval, execution, replay, or dashboard flows.

Suggested local checks:

```text
rg -n "hooks.slack.com/services|xoxb-|xoxp-|webhook.office.com|logic.azure.com" .
git status --short
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
TBD
```

Open issues:

| ID | Severity | Area | Description | Owner | Target Fix |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

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
