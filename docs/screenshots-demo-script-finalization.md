# SentinelFlow Screenshots + Demo Script Finalization

## 1. Purpose

This document defines Milestone 28C for finalizing marketplace screenshots and the demo script for AppExchange / AgentExchange submission.

Goal:

```text
Create a clean, consistent, privacy-safe screenshot and demo package that proves the SentinelFlow Salesforce workflow from app launch through incident review, approval, Case creation, replay, and governance explanation.
```

This document should be used before capturing final listing screenshots or recording the demo video.

## 2. Required Screenshots

Required screenshot list:

| # | Screenshot | Purpose | Required content |
| --- | --- | --- | --- |
| 1 | SentinelFlow App Home / Dashboard | Establish product home and operating view. | App name, recent incidents, status/risk summary, dashboard layout. |
| 2 | Sentinel Incident record | Show Salesforce-native incident record. | Incident name, type, status, risk score, risk level, policy decision, runbook. |
| 3 | AI Recommendation section | Show recommendation and runbook guidance. | Recommendation summary, confidence/decision text if available, runbook key. |
| 4 | Human Approval panel | Show governance control. | Approve/reject controls, recommendation context, approval state. |
| 5 | Replay Timeline | Show auditability. | Ordered events from intake through approval/execution/Case creation. |
| 6 | Policy Decision record | Show policy governance evidence. | Policy decision, rationale/status, related incident. |
| 7 | Audit Log list | Show event evidence. | Incident events, event types, timestamps, related incident. |
| 8 | Case created from approved action | Show safe Salesforce follow-up action. | Case subject, priority, origin, related incident where visible. |
| 9 | Org Health Score card | Show operational health view. | Score/card area, current health status, supporting dashboard context. |

Optional supporting screenshots:

- Permission set assignment view.
- Zentom API setup/configuration view.
- Salesforce error log example with sanitized data.
- Support/troubleshooting documentation excerpt.

Screenshot capture rules:

- Use a clean demo or validation org.
- Use the standard `FLOW_FAILURE` scenario.
- Use consistent browser zoom and viewport.
- Use consistent Salesforce theme.
- Hide browser bookmarks and personal profile details where possible.
- Do not show real customer data.
- Do not show secrets, credentials, tokens, or API keys.
- Do not show sensitive personal data or regulated data.

## 3. Screenshot Naming Convention

Recommended file naming:

```text
sentinelflow-01-app-dashboard.png
sentinelflow-02-sentinel-incident-record.png
sentinelflow-03-ai-recommendation.png
sentinelflow-04-human-approval-panel.png
sentinelflow-05-replay-timeline.png
sentinelflow-06-policy-decision-record.png
sentinelflow-07-audit-log-list.png
sentinelflow-08-created-case.png
sentinelflow-09-org-health-score.png
```

Optional screenshot names:

```text
sentinelflow-10-permission-sets.png
sentinelflow-11-api-configuration.png
sentinelflow-12-error-log-sanitized.png
```

Naming rules:

- Use lowercase file names.
- Use hyphens between words.
- Prefix with `sentinelflow`.
- Use two-digit sequence numbers.
- Keep final names stable once referenced in listing materials.
- Do not include customer names, org names, user names, or dates in filenames.

## 4. Demo Video Flow

Final demo flow:

1. Open SentinelFlow app.
2. Show dashboard and Org Health Score.
3. Trigger test `FLOW_FAILURE` incident.
4. Open created incident.
5. Explain risk/policy/recommendation/runbook.
6. Approve incident.
7. Execute approved action.
8. Show created Case.
9. Show Replay Timeline.
10. Close with security/governance explanation.

Recommended demo length:

```text
3-5 minutes
```

Demo setup checklist:

- [ ] Demo org is clean.
- [ ] Standard `FLOW_FAILURE` scenario is ready.
- [ ] Hosted API health passes.
- [ ] Hosted DB health passes.
- [ ] Required permission sets are assigned.
- [ ] Demo user has Admin or Approver permissions.
- [ ] Viewer read-only behavior is validated separately if shown.
- [ ] No real customer records are visible.
- [ ] No secrets are visible.
- [ ] Browser and Salesforce UI are clean.
- [ ] Replay Timeline has expected events.
- [ ] Created Case is easy to identify.

## 5. Demo Script Final Version

Opening:

```text
SentinelFlow by Tomcodex is Salesforce-native incident intelligence and governed automation powered by Zentom AI. In this demo, we will show how a Salesforce operational incident moves from signal to risk scoring, policy decision, recommendation, human approval, safe Case creation, and replayable audit evidence.
```

Step 1: Open SentinelFlow app.

```text
We start in the SentinelFlow app, where Salesforce admins and operations teams can review incidents, approvals, and operational health from a Salesforce-native experience.
```

Step 2: Show dashboard and Org Health Score.

```text
The dashboard gives a quick view of recent incidents, risk distribution, approval status, and Org Health Score. This is the operating view for teams reviewing Salesforce workflow health.
```

Step 3: Trigger test `FLOW_FAILURE` incident.

```text
For the demo, we use a controlled FLOW_FAILURE test incident. This represents a Salesforce automation issue that needs triage, risk review, and governed follow-up.
```

Step 4: Open created incident.

```text
The incident is written back into Salesforce as a Sentinel Incident record, so the team can review it using familiar Salesforce records and permissions.
```

Step 5: Explain risk/policy/recommendation/runbook.

```text
SentinelFlow calculates risk, records the policy decision, recommends a runbook, and explains the suggested next step. In this standard scenario, the expected policy is HUMAN_APPROVAL_REQUIRED and the runbook is FLOW_FAILURE_BASIC_RECOVERY.
```

Step 6: Approve incident.

```text
This is the governance boundary. SentinelFlow can recommend, but a human approver decides whether the action should proceed.
```

Step 7: Execute approved action.

```text
After approval, the authorized user can execute the safe action. For this workflow, the action is Salesforce Case creation.
```

Step 8: Show created Case.

```text
The created Case gives the operations team a Salesforce-native follow-up record with the incident context preserved.
```

Step 9: Show Replay Timeline.

```text
Replay Timeline shows the ordered audit trail: incident received, risk calculated, policy evaluated, recommendation generated, runbook selected, human approval, action execution, and Case creation.
```

Step 10: Close with security/governance explanation.

```text
SentinelFlow is designed for governed operations. Human approval remains required before execution, Viewer access is read-only, error and replay evidence should not expose secrets, and the current submission scope does not include full autonomous remediation, hosted HYBRID Ollama, or production Agentforce integration.
```

Closing:

```text
This workflow gives Salesforce teams a controlled way to understand incidents, approve safe actions, and audit what happened from one Salesforce-native experience.
```

## 6. Visual QA Checklist

Before finalizing screenshots:

- [ ] Image is sharp and readable.
- [ ] Browser zoom is consistent.
- [ ] Salesforce UI is not clipped.
- [ ] Main subject is visible without scrolling ambiguity.
- [ ] Screenshot title/context is understandable.
- [ ] No unrelated tabs, bookmarks, or personal information are visible.
- [ ] No real customer data is visible.
- [ ] No secrets, tokens, credentials, or API keys are visible.
- [ ] No placeholder text appears unless intentionally part of template.
- [ ] Screenshot matches listing copy.
- [ ] Screenshot matches demo flow.
- [ ] File name follows naming convention.

Before finalizing demo video:

- [ ] Audio is clear.
- [ ] Visuals are readable.
- [ ] Demo stays within target time.
- [ ] Demo follows final flow.
- [ ] No unsupported claims are made.
- [ ] No autonomous remediation claim is made.
- [ ] No production Agentforce claim is made.
- [ ] No hosted HYBRID Ollama claim is made.
- [ ] Human approval boundary is clearly stated.
- [ ] Replay/audit value is clearly shown.
- [ ] Security/privacy explanation is included.

## 7. Privacy/Sample Data Rules

Sample data rules:

- Use synthetic incident names and descriptions.
- Use synthetic user names where possible.
- Use sandbox, developer, or approved demo org data.
- Do not use real customer records.
- Do not use real customer org names in screenshots.
- Do not use regulated data or sensitive personal data.
- Do not use production credentials or real API keys.

Sensitive data that must not appear:

- API keys.
- Passwords.
- Access tokens.
- Session ids.
- Customer names unless approved.
- Real emails unless approved.
- Regulated data.
- Sensitive personal data.
- Internal-only infrastructure details.

Approved demo scenario:

```text
Incident type: FLOW_FAILURE
Risk score: 95
Risk level: CRITICAL
Policy decision: HUMAN_APPROVAL_REQUIRED
Runbook: FLOW_FAILURE_BASIC_RECOVERY
Approved action: CREATE_CASE
```

## 8. Final Asset Checklist

Final screenshot assets:

- [ ] `sentinelflow-01-app-dashboard.png`
- [ ] `sentinelflow-02-sentinel-incident-record.png`
- [ ] `sentinelflow-03-ai-recommendation.png`
- [ ] `sentinelflow-04-human-approval-panel.png`
- [ ] `sentinelflow-05-replay-timeline.png`
- [ ] `sentinelflow-06-policy-decision-record.png`
- [ ] `sentinelflow-07-audit-log-list.png`
- [ ] `sentinelflow-08-created-case.png`
- [ ] `sentinelflow-09-org-health-score.png`

Final demo assets:

- [ ] Demo video recorded.
- [ ] Demo video reviewed.
- [ ] Demo script approved.
- [ ] Demo captions/transcript prepared, if required.
- [ ] Final screenshots match demo story.
- [ ] Final listing copy references only validated features.
- [ ] Final privacy/security review complete.
- [ ] Submission owner approved assets.

Milestone 28C result:

```text
28C - Screenshots + Demo Script Finalization: Complete
Next - 28D Security Review Evidence Cross-check
```
