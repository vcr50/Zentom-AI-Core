# SentinelFlow Pilot Demo Script

## 1. Demo Goal

The demo goal is to show a real pilot customer how SentinelFlow turns a Salesforce operational incident into an explainable, approval-gated, auditable workflow.

Core demo outcome:

```text
Customer understands how SentinelFlow receives an incident, scores risk, records a policy decision, recommends a runbook, requires human approval, creates a safe Salesforce Case, and preserves replay evidence.
```

The demo should stay controlled and practical. It should not position SentinelFlow as full autonomous remediation, production Agentforce orchestration, or a custom integration platform.

## 2. Demo Audience

Primary audience:

- Salesforce Admin.
- Operations lead.
- Support or service leader.
- Automation owner.
- Technical evaluator.

Secondary audience:

- Security stakeholder.
- Governance or audit stakeholder.
- Customer success or support manager.
- Executive sponsor.

Audience-specific emphasis:

- Salesforce Admin: installation, permissions, callouts, objects, and troubleshooting.
- Operations lead: incident flow, approval decision, Case creation, and workflow fit.
- Security/governance: human approval, replay evidence, secret handling, and privacy boundaries.
- Executive sponsor: low-risk pilot value and marketplace-readiness path.

## 3. 30-Minute Demo Agenda

Recommended agenda:

| Time | Segment | Purpose |
| --- | --- | --- |
| 0-3 min | Opening story | Frame the operational problem and pilot goal. |
| 3-6 min | Architecture overview | Explain Salesforce, hosted Zentom API, hosted DB, and approval boundary. |
| 6-12 min | Flow failure incident demo | Submit or review a standard `FLOW_FAILURE` incident. |
| 12-16 min | Approval/rejection demo | Show recommendation, runbook, approval, and rejection controls. |
| 16-20 min | Case creation demo | Show approved safe action and resulting Salesforce Case. |
| 20-24 min | Replay timeline demo | Show audit trail from intake through Case creation. |
| 24-27 min | Dashboard + Org Health Score | Show operational review surface. |
| 27-29 min | Security/privacy explanation | Reconfirm guardrails and pilot limitations. |
| 29-30 min | Closing questions | Confirm fit, next steps, and feedback path. |

Facilitator rule:

- Keep the demo moving.
- Avoid deep implementation rabbit holes during the first 30 minutes.
- Park detailed technical questions for follow-up unless they block pilot trust.

## 4. Opening Story

Suggested opening:

```text
Imagine a Salesforce automation fails during an important operational workflow. The team needs to know what happened, how risky it is, what the recommended next step is, who approved it, what action was taken, and whether there is an audit trail afterward.

SentinelFlow is designed to make that path visible and controlled. It does not skip human judgment. It helps the team move from incident signal to recommendation, approval, safe action, and replay evidence.
```

Key points to land:

- The pilot is about controlled validation in a real Salesforce environment.
- Human approval remains required before execution.
- The value is explainability, safety, and operational trust.
- The goal is not to automate everything on day one.

Transition:

```text
I will show the full path using a standard flow failure incident: intake, risk, policy, recommendation, approval, Case creation, replay, and dashboard review.
```

## 5. Product Architecture Explanation

Simple architecture explanation:

```text
Salesforce sends a controlled incident payload to the hosted Zentom API. The API stores the incident, evaluates risk and policy, generates a recommendation and runbook response, and sends the result back to Salesforce. Salesforce users review the incident, approve or reject the recommendation, and only approved actions can create follow-up records such as Cases. Replay Timeline records the major events so the team can review what happened later.
```

Components to mention:

- Salesforce package.
- Sentinel Incident object.
- Audit Log object.
- Policy Decision object.
- Error Log object.
- Hosted Zentom API.
- Hosted PostgreSQL database.
- Risk scoring.
- Policy decision.
- Recommendation and runbook selection.
- Human approval panel.
- Safe Case creation.
- Replay Timeline.
- Dashboard and Org Health Score.

Architecture guardrails:

- Hosted pilot uses the validated production-readiness path.
- Human approval is required before execution.
- API authentication and callout configuration are validated during setup.
- Secrets should not be placed in committed metadata, screenshots, replay notes, or incident text.
- Advanced AI/HYBRID hosted Ollama and Agentforce production integration are not part of this pilot demo.

## 6. Live Flow Failure Incident Demo

Demo setup:

- Use a sandbox, developer org, or approved demo org.
- Confirm hosted API health is available before the call.
- Confirm the target org has permission sets assigned.
- Confirm the standard flow failure scenario is ready.

Demo incident:

```text
Incident type: FLOW_FAILURE
Source: Salesforce Flow
Environment: sandbox or approved pilot environment
Action type: CREATE_CASE
Expected risk score: 95
Expected risk level: CRITICAL
Expected policy decision: HUMAN_APPROVAL_REQUIRED
Expected runbook: FLOW_FAILURE_BASIC_RECOVERY
```

Talk track:

- Show the incident signal or explain how the test incident is submitted.
- Show Salesforce receiving the resulting Sentinel Incident.
- Point out the hosted Zentom incident id, if visible.
- Show risk score and risk level.
- Show policy decision.
- Show recommendation and runbook.

Expected customer takeaway:

- A customer can see how a Salesforce incident becomes a structured SentinelFlow record.
- Risk and policy are visible instead of hidden.
- The workflow waits for human review before execution.

If the live callout fails:

- Do not improvise around secrets or logs.
- Show the expected record from a previous validation if available.
- Capture the issue for support follow-up.
- Explain that callout/authentication failures are pilot-blocking and must be resolved before success is claimed.

## 7. Approval/Rejection Demo

Approval demo:

- Open the Sentinel Incident.
- Show approval panel.
- Show recommendation summary.
- Show runbook key and rationale.
- Approve the incident as an authorized user.
- Confirm approval status changes to approved.
- Confirm execution readiness.

Rejection demo:

- Use a separate incident or explain the rejection path if time is limited.
- Show that a user can reject instead of approving.
- Confirm rejected items should not proceed to execution.

Permission point:

- Admin and Approver roles can approve according to configured access.
- Viewer role should remain read-only.
- Approval should be intentional and visible in replay/audit evidence.

Talk track:

```text
This is the control point. SentinelFlow can recommend, but the user decides. For this pilot, execution is not autonomous; approval is the gate.
```

## 8. Case Creation Demo

Case creation demo:

- Start from an approved incident.
- Trigger the approved execution action.
- Show execution status changing to executed.
- Show execution action as `CREATE_CASE`.
- Open the created Salesforce Case.
- Confirm Case origin is `SentinelFlow` where available.
- Confirm priority and subject reflect the critical flow failure.
- Return to the incident and show the created Case reference.

Key points:

- Case creation happens only after approval.
- The action is narrow and predictable.
- The created Case gives the customer a familiar Salesforce follow-up object.
- Duplicate execution should be blocked or handled safely.

Expected customer takeaway:

- SentinelFlow can turn approved incident intelligence into a Salesforce-native operational follow-up.
- The pilot remains low-risk because the action is controlled and visible.

## 9. Replay Timeline Demo

Replay Timeline events to show:

- `INCIDENT_RECEIVED`
- `RISK_CALCULATED`
- `ZENTOM_POLICY_EVALUATED`
- `AI_RECOMMENDATION_GENERATED`
- `RUNBOOK_SELECTED`
- `HUMAN_APPROVED`
- `RUNBOOK_ACTION_EXECUTED`
- `CASE_CREATED`

Talk track:

```text
Replay Timeline is the audit story. It helps the team answer: what happened, in what order, who approved it, and what action was created.
```

What to highlight:

- Event order.
- Approval event.
- Execution event.
- Case creation event.
- No secrets in replay evidence.
- Useful support evidence if something fails.

Customer trust question:

```text
Would this replay evidence be enough for your team to review or explain the workflow after the fact?
```

## 10. Dashboard + Org Health Score Demo

Dashboard demo:

- Open SentinelFlow dashboard.
- Show recent incidents.
- Show risk distribution or high-risk incident visibility.
- Show approval queue or status summary.
- Show recent execution/Case creation if available.
- Show Org Health Score area.

Talk track:

```text
The dashboard is the operating view. It is not the whole audit trail, but it helps teams quickly see what needs attention and whether the pilot workflow is producing useful signals.
```

Customer questions:

- Does this show the right operational summary for your team?
- Which metric would help you decide whether SentinelFlow is useful?
- Is Org Health Score understandable in this pilot context?

## 11. Security/Privacy Explanation

Security and privacy points:

- Human approval remains required before execution.
- The pilot does not include full autonomous remediation.
- The pilot does not require customers to submit secrets or credentials.
- Customers should not put regulated data or sensitive personal data in test incident descriptions.
- API keys or shared secrets should not be exposed in screenshots, replay evidence, or committed metadata.
- Error logging should help troubleshooting without storing secret values.
- Permission sets separate Admin, Approver, and Viewer responsibilities.
- Viewer access should remain read-only.
- Replay Timeline supports auditability.

Known pilot limitations:

- Hosted HYBRID Ollama is not included.
- Agentforce production integration is not included.
- Major AI architecture changes are not included.
- Large object model changes are not included.
- Custom integrations are out of scope unless separately approved.

Suggested phrasing:

```text
The pilot is intentionally conservative. We want to validate trust, workflow fit, and supportability before expanding scope.
```

## 12. Closing Questions

Pilot fit questions:

- Does this workflow match a real operational problem your team has?
- Would you prefer to start in sandbox, developer org, or production?
- Who would own the Salesforce admin setup?
- Who should act as the pilot approver?
- Is Salesforce Case creation an acceptable approved action for the pilot?
- Are outbound callouts to the hosted Zentom API allowed?
- Would Replay Timeline evidence be useful for your audit or support process?
- What would make this pilot successful for your team?
- What would block pilot success?
- What should we clarify before setup?

Close with:

```text
If this looks like a fit, the next step is a guided setup session where we validate the package, permissions, hosted API connection, test incident, approval, Case creation, replay, and dashboard together.
```

## 13. Follow-Up Checklist

After the demo:

- [ ] Send pilot outreach summary.
- [ ] Confirm customer interest.
- [ ] Confirm target org type: sandbox, developer, or production.
- [ ] Confirm Salesforce admin contact.
- [ ] Confirm pilot approver contact.
- [ ] Confirm viewer or stakeholder contact.
- [ ] Confirm outbound callout approval.
- [ ] Confirm whether Case creation is acceptable.
- [ ] Confirm preferred callout mode: Remote Site or Named Credential.
- [ ] Schedule guided setup session.
- [ ] Share onboarding checklist.
- [ ] Record any security/privacy requirements.
- [ ] Record any pilot limitations or accepted risks.
- [ ] Capture demo feedback.
- [ ] Create support or issue records for blockers.
- [ ] Route patch-worthy feedback to v1.0.1 patch planning.
- [ ] Route roadmap requests to feedback-to-roadmap review.

Milestone 27C result:

```text
27C - Pilot Demo Script: Complete
Next - 27D Pilot Feedback Review Template
Then - 27E Pilot Success Report
```
