# SentinelFlow Slack Bot / Conversational Incident Assistant Plan

## 1. Purpose

Define Milestone 33 for a Slack-based conversational incident assistant that extends SentinelFlow visibility into the team workspace while preserving the existing Salesforce approval, execution, replay, and audit controls.

This milestone should plan the assistant before implementation. No production Slack bot code should be added until scope, security, and validation are agreed.

## 2. Goal

Give Salesforce operations teams a controlled way to see SentinelFlow incident context in Slack, ask basic incident questions, and navigate back to Salesforce for governed review and approval.

The assistant should make the command center feel present in the team workflow without bypassing SentinelFlow governance.

## 3. User Experience

Primary experience:

- Receive Slack alerts for high-risk or approval-required SentinelFlow incidents.
- Ask for recent critical incidents.
- Ask for pending approvals.
- Ask for incident summary by incident number.
- Open the Salesforce Sentinel Incident record from Slack.
- Open the Replay Timeline or dashboard from Slack.

Slack should act as a notification and assistant layer, not the system of record.

## 4. Initial Use Cases

Milestone 33 should start with low-risk read-only and navigation use cases:

- Notify channel when a CRITICAL incident is created.
- Notify channel when an incident requires human approval.
- Notify channel when an approved action creates a Salesforce Case.
- Show a short incident summary.
- Show current Org Health status.
- Show top pending approvals.
- Link users to the SentinelFlow dashboard, incident record, Case record, or Replay Timeline.

## 5. Out-of-Scope Actions

Do not include in the first Slack assistant scope:

- Autonomous remediation from Slack.
- Direct execution of runbook actions from Slack.
- Approval or rejection from Slack unless a later security-reviewed milestone explicitly adds it.
- Sending sensitive payloads, API keys, tokens, customer secrets, or full request/response bodies to Slack.
- Broad natural language agent actions that can mutate Salesforce data.
- Agentforce production integration.
- Hosted HYBRID Ollama or major AI architecture changes.

## 6. Safety Rules

The Slack assistant must preserve these guardrails:

- Salesforce remains the system of record.
- Human approval remains in Salesforce.
- Execution remains governed by existing SentinelFlow approval and execution logic.
- Slack messages must use minimum necessary incident data.
- Slack must not expose secrets, API headers, tokens, request payloads, or sensitive customer details.
- Every Slack-triggered lookup should be auditable if implemented later.
- Any mutating action requires a separate security and governance review.

## 7. Architecture Options

Option A: Hosted API Slack endpoint

- Slack sends events or slash commands to the hosted SentinelFlow/Zentom API.
- Hosted API validates Slack signature.
- Hosted API reads allowed summary data from Salesforce through a controlled integration path.
- Slack response includes short summary and Salesforce links.

Option B: Salesforce outbound alert only

- Salesforce emits selected alerts to Slack through a webhook or named integration path.
- No inbound Slack commands in the first phase.
- Lowest risk and fastest validation path.

Option C: Hybrid phased path

- Phase 1: outbound Slack alerts only.
- Phase 2: read-only slash commands.
- Phase 3: guarded approval links that open Salesforce, not direct Slack approvals.

Recommended starting path:

```text
Option C, Phase 1 first: outbound alerts only.
```

## 8. Data Shared To Slack

Allowed initial fields:

- Sentinel Incident name.
- Incident type.
- Risk level and risk score.
- Policy decision.
- Recommendation status.
- Runbook key.
- Approval status.
- Execution status.
- Created time.
- Salesforce record link.

Do not send:

- Full request payloads.
- Full response payloads.
- API keys or headers.
- Customer secrets.
- Personal data unless explicitly approved.
- Long AI reasoning traces.

## 9. Commands / Interactions

Candidate read-only commands for later phases:

```text
/sentinelflow health
/sentinelflow critical
/sentinelflow approvals
/sentinelflow incident SI-000013
```

Initial implementation should avoid commands until outbound alerting is validated.

## 10. Security Requirements

Before implementation:

- Confirm Slack app ownership and workspace.
- Define allowed channels.
- Define signing secret storage.
- Define token storage.
- Define environment separation.
- Validate Slack request signature verification.
- Define least-privilege Salesforce access.
- Define audit/error logging.
- Confirm no secrets are logged.
- Confirm privacy-safe message templates.

## 11. Validation Requirements

Validation should prove:

- CRITICAL incident alert is sent to the correct Slack channel.
- Approval-required alert is sent to the correct Slack channel.
- Case-created alert is sent after approved execution.
- Slack message links open the correct Salesforce records.
- No sensitive payloads or secrets appear in Slack.
- Existing Apex/controller tests remain unchanged unless a later implementation milestone adds covered code.
- Existing SentinelFlow dashboard, approval, execution, and replay behavior remain unchanged.

## 12. Milestone 33 Breakdown

Recommended breakdown:

- 33A - Slack assistant scope and safety plan.
- 33B - Slack app / workspace setup checklist.
- 33C - Slack alert message templates.
- 33D - Outbound alert integration plan.
- 33E - Read-only command design.
- 33F - Security validation plan.
- 33G - Pilot Slack assistant validation report.

## 13. Exit Criteria

Milestone 33 planning is ready to move to implementation only when:

- Initial scope is approved as outbound alerts first.
- Slack app/workspace owner is identified.
- Allowed channels are defined.
- Data shared to Slack is approved.
- Security requirements are documented.
- Validation checklist is accepted.
- No autonomous remediation or Slack-side execution is included.
