# SentinelFlow Slack Pilot Setup and Manual Validation

## 1. Purpose

Open Milestone 34 and define the manual Slack pilot setup path before any integration code is built.

This milestone validates Slack workspace, app, channel, message templates, links, privacy, and operator usefulness manually.

## 2. Milestone Goal

Prove that SentinelFlow Slack alerts are safe and useful as a notification layer before building automated delivery.

Core rule:

```text
Manual validation first.
No production Slack integration code yet.
No Slack-side approval.
No Slack-side execution.
No autonomous remediation.
Salesforce remains the system of record.
```

## 3. Pilot Setup Scope

In scope:

- Select Slack workspace.
- Create or verify SentinelFlow Slack app.
- Create approved pilot channel.
- Confirm pilot participants.
- Manually render alert templates using demo/sample data.
- Test Salesforce links from Slack.
- Run security/privacy checks.
- Capture screenshots with no secrets.
- Record pilot findings.

Out of scope:

- Automated Slack delivery.
- Slash command implementation.
- Slack approval/rejection.
- Slack execution.
- Slack remediation.
- Agentforce production integration.
- Major AI architecture changes.

## 4. Pilot Workspace

Workspace:

```text
TBD
```

Workspace owner:

```text
TBD
```

Checklist:

- [ ] Workspace selected.
- [ ] Workspace owner confirmed.
- [ ] Workspace approved for SentinelFlow pilot/demo.
- [ ] Retention/security settings reviewed.
- [ ] No customer production data used unless explicitly approved.

## 5. Pilot Channel

Recommended channel:

```text
#sentinelflow-alerts
```

Alternative pilot channel:

```text
#sentinelflow-pilot
```

Checklist:

- [ ] Channel created or selected.
- [ ] Channel owner confirmed.
- [ ] Channel purpose set.
- [ ] Participants limited to approved pilot users.
- [ ] SentinelFlow app invited if needed.
- [ ] No broad public/customer channel used without approval.

## 6. Slack App Setup

App name:

```text
SentinelFlow
```

Checklist:

- [ ] Slack app exists.
- [ ] App owner confirmed.
- [ ] App icon configured.
- [ ] App description configured.
- [ ] Minimum scopes reviewed.
- [ ] App installation approved.
- [ ] No secrets pasted into docs/screenshots.

## 7. Manual Message Validation

Use templates from:

```text
docs/slack-alert-message-templates.md
```

Messages to manually validate:

- [ ] CRITICAL incident alert.
- [ ] Approval-required alert.
- [ ] Approved action executed alert.
- [ ] Case-created alert.
- [ ] Org Health watch alert.
- [ ] Replay/audit ready alert.
- [ ] Alert delivery issue alert.

Validation checks:

- [ ] Message is readable.
- [ ] Message is short enough for Slack.
- [ ] Risk/policy/action context is clear.
- [ ] Message uses demo/sample data.
- [ ] Message links back to Salesforce.
- [ ] Message has no Approve/Reject/Execute/Remediate action.
- [ ] Message has no secrets, raw payloads, or sensitive personal data.

## 8. Salesforce Link Validation

Links to test:

- SentinelFlow Command Center.
- Sentinel Incident record.
- Created Case record.
- Replay Timeline view or incident page.
- System Health / dashboard view.

Validation checks:

- [ ] Authorized pilot user can open links.
- [ ] Unauthorized/non-Salesforce user cannot bypass Salesforce permissions.
- [ ] Links do not include session ids.
- [ ] Links do not include tokens.
- [ ] Links open the expected record/view.

## 9. Security / Privacy Validation

Security checklist:

- [ ] No Slack token shown.
- [ ] No webhook URL shown.
- [ ] No signing secret shown.
- [ ] No Salesforce session id shown.
- [ ] No API keys shown.
- [ ] No raw request/response payloads shown.
- [ ] No full stack traces shown.
- [ ] No customer secrets shown.
- [ ] No direct Slack approval/execution path shown.

## 10. Screenshot Evidence

Screenshots to capture:

- Slack channel with safe demo alert.
- CRITICAL incident alert.
- Approval-required alert.
- Case-created alert.
- Org Health watch alert.
- Salesforce link opened successfully.

Screenshot rules:

- Hide Slack workspace ids if needed.
- Hide user names if not approved.
- Hide tokens, webhook URLs, signing secrets, and app secrets.
- Use demo/sample data.
- Do not show customer secrets or raw payloads.

## 11. User Feedback

Questions:

- Are alerts understandable?
- Is the control-tower language useful?
- Does the message clearly say what needs attention?
- Is the Salesforce link obvious?
- Is the message too noisy?
- Should any alert be routed differently?
- Does the alert create trust without implying automation bypass?

Feedback notes:

```text
TBD
```

## 12. Issue Tracking

| ID | Severity | Area | Description | Owner | Target Fix |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

Severity rule:

- P0/P1/P2 issues must be fixed before implementation.
- P3/P4 issues can be deferred.

## 13. Go / No-Go Decision

Options:

```text
GO - Manual Slack pilot safe; proceed to outbound alert implementation.
CONDITIONAL GO - Fix listed P0/P1/P2 items first.
NO-GO - Security, privacy, or governance blocker found.
```

Decision:

```text
TBD
```

## 14. Milestone 34 Breakdown

Recommended breakdown:

- 34A - Slack pilot setup/manual validation plan.
- 34B - Slack workspace/app/channel setup evidence.
- 34C - Manual alert template rendering.
- 34D - Salesforce link/security validation.
- 34E - Pilot feedback and issue triage.
- 34F - Go/No-Go for implementation.

## 15. Exit Criteria

Milestone 34 can move to implementation only when:

- Slack workspace is approved.
- Slack app/channel setup is validated.
- Manual message templates are accepted.
- Salesforce links are validated.
- Security/privacy checks pass.
- Screenshots are safe.
- No P0/P1/P2 blocker remains.
- Go decision is recorded.

## 16. Next Milestone

Recommended next milestone if GO:

```text
Milestone 35 - Slack Outbound Alert Implementation
```

If CONDITIONAL GO:

```text
Milestone 35 - Slack Pilot Fixes
```

If NO-GO:

```text
Milestone 35 - Slack Security Remediation
```
