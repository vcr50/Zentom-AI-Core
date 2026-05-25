# SentinelFlow Slack Salesforce Link / Security Validation

## 1. Purpose

Define the validation checklist for Salesforce links and security behavior used in the SentinelFlow Slack pilot.

Slack messages should guide users back to Salesforce for review, approval, execution, and audit. Slack must not bypass Salesforce permissions.

## 2. Validation Rule

Core rule:

```text
Slack links open Salesforce.
Salesforce permissions decide access.
Slack does not grant access, approval, execution, or remediation.
```

## 3. Validation Owner

Validation owner:

```text
TBD
```

Validation date:

```text
TBD
```

Target Salesforce org:

```text
astrosoft / TBD
```

Target Slack channel:

```text
TBD
```

## 4. Link Inventory

Required links:

- SentinelFlow Command Center.
- Sentinel Incident record.
- Created Case record.
- Replay Timeline or incident detail page.
- System Health / dashboard view.

Link inventory:

| Link Type | Safe Label | Target | Test User | Result |
| --- | --- | --- | --- | --- |
| Command Center | Open Command Center | TBD | TBD | TBD |
| Incident | Review Incident | TBD | TBD | TBD |
| Case | Open Case | TBD | TBD | TBD |
| Replay | View Replay Timeline | TBD | TBD | TBD |
| System Health | View System Health | TBD | TBD | TBD |

## 5. Link Format Rules

Allowed:

- Standard Salesforce Lightning URLs.
- Record links that require Salesforce authentication.
- Dashboard/app links that require Salesforce authentication.

Not allowed:

- Session ids in URL.
- OAuth tokens in URL.
- One-time secrets in URL.
- Embedded API keys.
- Public unauthenticated links to sensitive records.
- Direct Slack action links that approve, reject, execute, or remediate.

Checklist:

- [ ] No URL includes `sid=`.
- [ ] No URL includes bearer token.
- [ ] No URL includes API key.
- [ ] No URL includes webhook URL.
- [ ] No URL executes a mutating action.
- [ ] URL opens Salesforce UI only.

## 6. Authorized User Test

Authorized test user:

```text
TBD
```

Expected access:

- Can open SentinelFlow Command Center.
- Can open assigned Sentinel Incident records.
- Can open Case records if Salesforce permissions allow.
- Can view Replay Timeline or incident audit view if permissions allow.

Test result:

```text
TBD
```

Evidence:

```text
TBD
```

## 7. Unauthorized User Test

Unauthorized or limited test user:

```text
TBD
```

Expected behavior:

- Cannot access records without Salesforce permission.
- Receives Salesforce login or access-denied behavior.
- Does not see sensitive record details from Slack alone.
- Cannot approve, reject, execute, or remediate from Slack.

Test result:

```text
TBD
```

Evidence:

```text
TBD
```

## 8. Message Data Leakage Check

Validate Slack messages do not expose:

- API keys.
- Slack tokens.
- Webhook URLs.
- Salesforce session ids.
- Customer secrets.
- Raw request payloads.
- Raw response payloads.
- Full stack traces.
- Sensitive personal data.
- Long AI reasoning traces.

Checklist:

- [ ] CRITICAL incident alert checked.
- [ ] Approval-required alert checked.
- [ ] Executed-action alert checked.
- [ ] Case-created alert checked.
- [ ] Org Health watch alert checked.
- [ ] Replay/audit alert checked.
- [ ] Delivery issue alert checked.

## 9. Salesforce Permission Set Check

Relevant permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

Validation checklist:

- [ ] Admin user can access expected dashboard and records.
- [ ] Approver user can access expected incident approval views in Salesforce.
- [ ] Viewer user remains read-only.
- [ ] User without SentinelFlow permission cannot access protected records.
- [ ] Slack message content does not reveal protected record details beyond approved summary fields.

## 10. Link Click Behavior

Expected behavior:

- If user is logged in and authorized, Salesforce opens the target page.
- If user is logged out, Salesforce prompts login.
- If user is unauthorized, Salesforce denies access.
- Slack does not display hidden record data after click failure.

Checklist:

- [ ] Logged-in authorized user behavior tested.
- [ ] Logged-out user behavior tested.
- [ ] Unauthorized user behavior tested.
- [ ] Mobile Slack link behavior checked if possible.
- [ ] Desktop Slack link behavior checked.

## 11. Screenshot Rules

Screenshot evidence must:

- Use demo/sample data.
- Hide user names if not approved.
- Hide org ids if not approved.
- Hide tokens, webhook URLs, signing secrets, and session ids.
- Avoid real customer data.
- Avoid exposing full Salesforce URLs if they contain sensitive parameters.

Required screenshots:

- [ ] Slack message with safe Salesforce link.
- [ ] Authorized user opens Salesforce link.
- [ ] Unauthorized/access-denied behavior.
- [ ] Message content with no secrets visible.

## 12. Pass / Fail Result

Result options:

```text
PASS - Links preserve Salesforce permissions and messages are privacy-safe.
CONDITIONAL PASS - Fix listed P0/P1/P2 gaps first.
FAIL - Access bypass, secret exposure, or mutating Slack behavior found.
```

Result:

```text
TBD
```

## 13. Issues / Gaps

| ID | Severity | Area | Description | Owner | Target Fix |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

Severity rules:

- P0: access bypass, secret exposure, Slack-side mutation, or sensitive customer data exposure.
- P1: broken core links, incorrect permission behavior, or unsafe channel visibility.
- P2: unclear message/link wording, missing evidence, or minor privacy cleanup.

## 14. Exit Criteria

34D is complete when:

- Required link inventory is documented.
- Authorized user link behavior is validated.
- Unauthorized user behavior is validated.
- Message data leakage check is complete.
- Permission set behavior is checked.
- Screenshot rules are followed.
- Pass/fail result is recorded.
- P0/P1/P2 gaps are listed for triage.
