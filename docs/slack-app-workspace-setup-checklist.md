# SentinelFlow Slack App / Workspace Setup Checklist

## 1. Purpose

Define the setup checklist for the SentinelFlow Slack assistant before any integration code is built.

This checklist keeps Milestone 33 focused on a safe, controlled Slack rollout path:

```text
Outbound alerts first.
No Slack-side execution.
No autonomous remediation.
Salesforce remains the system of record.
```

## 2. Setup Owner

Setup owner:

```text
TBD
```

Responsibilities:

- Own Slack app creation.
- Confirm workspace access.
- Manage app installation approval.
- Coordinate channel selection.
- Store and rotate Slack credentials safely.
- Confirm privacy/security review before production use.

## 3. Target Workspace

Target Slack workspace:

```text
TBD
```

Workspace checklist:

- [ ] Workspace owner/admin identified.
- [ ] Workspace is approved for SentinelFlow pilot/demo use.
- [ ] Workspace is not a customer production workspace unless explicitly approved.
- [ ] Demo/pilot data rules are accepted.
- [ ] Security reviewer or admin contact identified.

## 4. Slack App

Slack app name:

```text
SentinelFlow
```

Recommended app description:

```text
SentinelFlow sends governed Salesforce incident alerts and links operators back to Salesforce for review, approval, and audit.
```

App setup checklist:

- [ ] Slack app created.
- [ ] App owner assigned.
- [ ] App icon added.
- [ ] App description added.
- [ ] Development workspace selected.
- [ ] Production/customer workspace install deferred until pilot approval.

## 5. App Permissions / Scopes

Initial outbound-alert-only scopes:

- `chat:write`
- `chat:write.public`, only if posting to channels where the app is not explicitly invited is required.

Avoid in first phase:

- Broad user profile scopes.
- Channel history read scopes.
- File upload scopes.
- Admin scopes.
- Any scope that enables mutating Salesforce state from Slack.

Scope checklist:

- [ ] Minimum scopes selected.
- [ ] No read-history scopes added unless explicitly justified.
- [ ] No admin scopes added.
- [ ] No direct approval/execution capability added.
- [ ] Scope list reviewed before install.

## 6. Allowed Channels

Recommended pilot channels:

```text
#sentinelflow-alerts
#sentinelflow-pilot
```

Channel checklist:

- [ ] Pilot alert channel created.
- [ ] Channel owner assigned.
- [ ] Channel membership limited to approved pilot users.
- [ ] Channel purpose explains SentinelFlow alert testing.
- [ ] No customer secrets or sensitive payloads are permitted in channel messages.
- [ ] App invited to the approved channel.

## 7. Credentials / Secrets

Credentials expected:

- Slack bot token.
- Slack signing secret, if inbound events or commands are added later.
- Webhook URL, if using incoming webhooks.

Storage rules:

- Do not commit Slack tokens, webhook URLs, signing secrets, or app secrets.
- Store secrets in approved environment variables or secure Salesforce configuration only after implementation design is approved.
- Rotate credentials after demos if any secret is exposed.
- Do not paste secrets into docs, screenshots, tickets, or Slack messages.

Credential checklist:

- [ ] Bot token generated.
- [ ] Token stored securely.
- [ ] Signing secret captured only if needed for inbound interactions.
- [ ] Webhook URL captured only if incoming webhooks are used.
- [ ] No credentials committed to Git.
- [ ] Rotation owner identified.

## 8. Message Posting Model

Phase 1 recommendation:

```text
Outbound alerts only.
```

Allowed message types:

- CRITICAL incident created.
- Approval required.
- Approved action executed.
- Case created.
- System health watch/attention status.

Message model checklist:

- [ ] Message templates approved before implementation.
- [ ] Messages include Salesforce links, not sensitive payloads.
- [ ] Messages use minimum necessary data.
- [ ] Messages are short enough for Slack scanning.
- [ ] No direct approve/reject/execute buttons in first phase.

## 9. Salesforce Link Requirements

Slack messages should link back to Salesforce for action:

- SentinelFlow dashboard.
- Sentinel Incident record.
- Created Case record.
- Replay Timeline view, if available.

Link checklist:

- [ ] Base Salesforce org URL identified.
- [ ] Link format confirmed for Lightning record pages.
- [ ] Links tested with pilot users.
- [ ] Access-denied behavior documented.
- [ ] No session ids or one-time tokens placed in links.

## 10. Privacy / Security Checklist

Before posting alerts:

- [ ] Demo/sample data confirmed.
- [ ] No real customer secrets.
- [ ] No API keys, bearer tokens, session ids, or webhook URLs.
- [ ] No full request/response payloads.
- [ ] No unnecessary personal data.
- [ ] No long AI reasoning traces.
- [ ] Alerts reviewed for marketplace/demo screenshots.
- [ ] Slack workspace retention settings understood.

## 11. Validation Checklist

Setup validation should prove:

- [ ] Slack app installs in the target workspace.
- [ ] App can post to the approved channel.
- [ ] Test message renders correctly.
- [ ] Links open Salesforce records or dashboard.
- [ ] Pilot users can access linked Salesforce records.
- [ ] Unauthorized users cannot access Salesforce records.
- [ ] No secrets appear in Slack messages.
- [ ] No unrelated channels receive alerts.

## 12. Setup Exit Criteria

33B is complete when:

- Slack workspace is identified.
- Slack app owner is identified.
- Allowed channel is identified.
- Minimum scopes are documented.
- Credential storage rules are documented.
- Message posting model is outbound-alert-only.
- Privacy/security checklist is accepted.
- No direct Slack execution or approval is included.
