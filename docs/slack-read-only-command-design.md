# SentinelFlow Slack Read-only Command Design

## 1. Purpose

Define the read-only Slack command design for a later phase of Milestone 33.

This document does not approve implementation yet. It defines a safe command shape for when outbound alerts are already validated.

## 2. Command Goal

Allow approved Slack users to ask for basic SentinelFlow status and incident summaries without changing Salesforce data.

Commands should answer:

- Is the org healthy?
- What critical incidents need attention?
- What is waiting for approval?
- What happened for a specific incident?
- Where do I open the Salesforce record or Replay Timeline?

## 3. Scope Rule

Read-only commands must remain notification and lookup only:

```text
No approve.
No reject.
No execute.
No remediate.
No Salesforce data mutation.
```

Salesforce remains the system of record for review, approval, execution, and audit.

## 4. Candidate Commands

Initial candidate commands:

```text
/sentinelflow health
/sentinelflow critical
/sentinelflow approvals
/sentinelflow incident <incident-name>
/sentinelflow help
```

Deferred commands:

```text
/sentinelflow cases
/sentinelflow replay <incident-name>
/sentinelflow errors
/sentinelflow digest
```

Do not add:

```text
/sentinelflow approve
/sentinelflow reject
/sentinelflow execute
/sentinelflow remediate
```

## 5. `/sentinelflow health`

Purpose:

```text
Show current SentinelFlow org posture.
```

Response fields:

- Org Health status.
- Org Health score.
- Critical incident count.
- Pending approval count.
- Failed action count.
- Dashboard link.

Example response:

```text
SentinelFlow org health
Status: Critical
Score: 0 / 100
Critical traffic: 14
Awaiting clearance: 4
Failed actions: 0

Open Command Center: <DashboardLink>
```

## 6. `/sentinelflow critical`

Purpose:

```text
Show recent CRITICAL incidents.
```

Response fields:

- Incident name.
- Incident type.
- Risk score.
- Policy decision.
- Approval status.
- Salesforce link.

Limit:

```text
Return at most 5 incidents.
```

## 7. `/sentinelflow approvals`

Purpose:

```text
Show incidents waiting for human clearance in Salesforce.
```

Response fields:

- Incident name.
- Incident type.
- Risk score / risk level.
- Recommended action.
- Runbook key.
- Salesforce incident link.

Response rule:

```text
Include Review Incident links only. Do not include Approve, Reject, Execute, or Remediate buttons.
```

## 8. `/sentinelflow incident <incident-name>`

Purpose:

```text
Show a short summary for one SentinelFlow incident.
```

Response fields:

- Incident name.
- Type.
- Risk score / level.
- Policy decision.
- Recommendation status.
- Approval status.
- Execution status.
- Created Case, if available.
- Incident link.
- Replay Timeline link or incident link.

Privacy rule:

```text
Do not return raw request payloads, raw response payloads, exception stack traces, or long AI reasoning.
```

## 9. `/sentinelflow help`

Purpose:

```text
Show supported read-only commands and safety rule.
```

Example response:

```text
SentinelFlow Slack assistant
Commands:
/sentinelflow health
/sentinelflow critical
/sentinelflow approvals
/sentinelflow incident <incident-name>

This assistant is read-only. Approvals and execution happen in Salesforce.
```

## 10. Authorization Model

Before implementation, define:

- Allowed Slack workspace.
- Allowed Slack channels.
- Allowed Slack user groups or user allowlist.
- Salesforce integration user permissions.
- Access denied response.
- Audit log expectations.

Authorization rule:

```text
Slack access should not grant Salesforce access. Linked Salesforce records must still enforce Salesforce permissions.
```

## 11. Data Access Model

Read-only commands may use:

- Hosted API relay with Salesforce integration access.
- Salesforce Apex REST endpoint, if separately designed and reviewed.
- Precomputed alert/status cache, if implemented later.

Commands must not:

- Query unrestricted Salesforce data.
- Return sensitive fields.
- Return raw payloads.
- Return secrets.
- Mutate any Salesforce record.

## 12. Error Responses

Recommended safe responses:

```text
I could not find that SentinelFlow incident. Check the incident number and try again.
```

```text
SentinelFlow status is unavailable right now. Open the Command Center in Salesforce for the latest view: <DashboardLink>
```

```text
You are not authorized to use SentinelFlow Slack commands in this workspace or channel.
```

Error responses must not expose:

- Stack traces.
- Tokens.
- API URLs with secrets.
- Raw Salesforce errors.
- Internal object ids unless already visible through allowed links.

## 13. Audit / Logging

If commands are implemented, log:

- Command name.
- Safe Slack workspace id.
- Safe channel id or alias.
- Request timestamp.
- Result status.
- Safe error category.

Do not log:

- Slack tokens.
- Signing secret.
- Full command text if it may contain sensitive data.
- Raw Salesforce response payload.
- Personal data beyond what is necessary for security review.

## 14. Validation Requirements

Validation should prove:

- `/sentinelflow help` returns only read-only commands.
- `/sentinelflow health` returns safe org health summary.
- `/sentinelflow critical` returns at most 5 safe incident summaries.
- `/sentinelflow approvals` returns Review Incident links only.
- `/sentinelflow incident <incident-name>` returns a safe summary or not-found response.
- Unauthorized channel/user receives access denied.
- No command mutates Salesforce data.
- No secrets or raw payloads appear in Slack or logs.

## 15. Exit Criteria

33E is complete when:

- Read-only command list is documented.
- Mutating commands are explicitly excluded.
- Response fields are documented.
- Authorization model is documented.
- Data access model is documented.
- Error response rules are documented.
- Audit/logging expectations are documented.
- Validation requirements are documented.
