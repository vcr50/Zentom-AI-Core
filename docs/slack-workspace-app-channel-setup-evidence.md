# SentinelFlow Slack Workspace / App / Channel Setup Evidence

## 1. Purpose

Capture evidence that the Slack workspace, SentinelFlow Slack app, and pilot channel are ready for manual validation.

This evidence must not include tokens, webhook URLs, signing secrets, app secrets, or sensitive customer data.

## 2. Validation Date

Validation date:

```text
TBD
```

Validation owner:

```text
TBD
```

## 3. Target Workspace

Workspace name:

```text
TBD
```

Workspace type:

```text
Internal / Demo / Pilot / Customer-approved
```

Workspace checklist:

- [ ] Workspace selected.
- [ ] Workspace owner/admin identified.
- [ ] Workspace approved for SentinelFlow Slack pilot.
- [ ] Retention/security policy reviewed.
- [ ] Demo/sample data policy accepted.
- [ ] Customer production data excluded unless explicitly approved.

Evidence notes:

```text
TBD
```

## 4. Slack App Evidence

Slack app name:

```text
SentinelFlow
```

App owner:

```text
TBD
```

App checklist:

- [ ] App exists.
- [ ] App owner assigned.
- [ ] App description configured.
- [ ] App icon configured.
- [ ] App installed only in approved workspace.
- [ ] App installation approved by workspace owner/admin.
- [ ] No secrets captured in screenshots.

Approved app description:

```text
SentinelFlow sends governed Salesforce incident alerts and links operators back to Salesforce for review, approval, and audit.
```

Evidence notes:

```text
TBD
```

## 5. Permission / Scope Evidence

Expected phase 1 scope:

```text
Outbound alert validation only.
```

Allowed minimum scopes:

- `chat:write`
- `chat:write.public`, only if required and approved.

Scope checklist:

- [ ] Scope list reviewed.
- [ ] No admin scopes added.
- [ ] No broad channel history scopes added.
- [ ] No user profile read scopes added unless explicitly justified.
- [ ] No direct approve/reject/execute/remediate capability added.
- [ ] Scope screenshot captured with secrets hidden.

Evidence notes:

```text
TBD
```

## 6. Pilot Channel Evidence

Approved pilot channel:

```text
#sentinelflow-alerts
```

Alternative pilot channel:

```text
#sentinelflow-pilot
```

Channel owner:

```text
TBD
```

Channel checklist:

- [ ] Channel created or selected.
- [ ] Channel owner assigned.
- [ ] Channel purpose set.
- [ ] Pilot participants reviewed.
- [ ] Channel membership limited to approved users.
- [ ] SentinelFlow app invited to the channel if needed.
- [ ] Channel is not a broad customer/public channel unless approved.

Evidence notes:

```text
TBD
```

## 7. Credential Handling Evidence

Credentials that may exist:

- Slack bot token.
- Slack webhook URL.
- Slack signing secret, only if inbound commands/events are later enabled.
- Slack app client secret.

Credential checklist:

- [ ] No credential committed to Git.
- [ ] No credential pasted into docs.
- [ ] No credential captured in screenshots.
- [ ] No credential posted to Slack.
- [ ] Storage location documented by name only.
- [ ] Rotation owner identified.
- [ ] Rotation path understood.

Storage location name:

```text
TBD - name only, no secret value
```

## 8. Secret Search Evidence

Search patterns:

```text
xoxb-
xapp-
hooks.slack.com/services
SLACK_BOT_TOKEN
SLACK_SIGNING_SECRET
SLACK_WEBHOOK_URL
```

Search result:

```text
TBD
```

Checklist:

- [ ] Slack token pattern not found in committed files.
- [ ] Slack webhook pattern not found in committed files.
- [ ] Slack signing secret environment variable not committed with a value.
- [ ] Screenshots checked for visible secrets.

## 9. Manual Test Message Evidence

Manual test message:

```text
SentinelFlow manual pilot test
This channel will be used to validate privacy-safe SentinelFlow alert templates.
No approval, execution, or remediation happens in Slack.
```

Checklist:

- [ ] Test message sent.
- [ ] Test message visible in approved channel.
- [ ] Message has no secrets.
- [ ] Message has no customer data.
- [ ] Participants understand Slack is notification-only.

Evidence notes:

```text
TBD
```

## 10. Salesforce Link Readiness

Links to prepare:

- SentinelFlow Command Center.
- Sentinel Incident record.
- Created Case record.
- Replay Timeline / incident record.

Checklist:

- [ ] Base Salesforce org URL identified.
- [ ] Dashboard link prepared.
- [ ] Incident link prepared.
- [ ] Case link prepared.
- [ ] Links do not include session ids or tokens.
- [ ] Links require Salesforce authentication.

Evidence notes:

```text
TBD
```

## 11. Screenshot Evidence Checklist

Screenshots to capture:

- [ ] Slack app configuration, with secrets hidden.
- [ ] App scopes, with secrets hidden.
- [ ] Approved pilot channel.
- [ ] Manual test message.
- [ ] Salesforce link opened from Slack.

Screenshot rules:

- Hide tokens, webhook URLs, signing secrets, and app secrets.
- Hide personal user names unless approved.
- Hide customer org ids unless intentionally approved.
- Use demo/sample data only.

## 12. Pass / Fail Result

Result options:

```text
PASS - Workspace/app/channel setup ready for manual template validation.
CONDITIONAL PASS - Fix listed setup gaps first.
FAIL - Security, privacy, ownership, or channel blocker found.
```

Result:

```text
TBD
```

## 13. Issues / Gaps

| ID | Severity | Area | Description | Owner | Target Fix |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

## 14. Exit Criteria

34B is complete when:

- Workspace is selected and approved.
- Slack app exists and owner is confirmed.
- Pilot channel is selected and owner is confirmed.
- Minimum scopes are reviewed.
- Credential handling is documented without exposing secrets.
- Secret search evidence is recorded.
- Manual test message is posted safely.
- Salesforce link readiness is confirmed.
- Pass/fail result is recorded.
