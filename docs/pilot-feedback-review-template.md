# SentinelFlow Pilot Feedback Review Template

## 1. Pilot Customer

Customer name:

```text
TBD
```

Customer context:

- Salesforce org type:
- Salesforce Org Id:
- Industry/use case:
- Primary workflow evaluated:
- Pilot support owner:
- Customer admin contact:
- Customer approver contact:

## 2. Pilot Date

Pilot dates:

```text
Start date:
End date:
Review date:
```

Pilot phase reviewed:

- Intro/demo.
- Guided setup.
- Workflow validation.
- Observation period.
- Final pilot review.

## 3. Participants

Customer participants:

| Name | Role | Responsibility | Attended |
| --- | --- | --- | --- |
| TBD | Salesforce Admin | Package setup and configuration | TBD |
| TBD | Approver | Approval and execution validation | TBD |
| TBD | Viewer/stakeholder | Dashboard and replay review | TBD |

SentinelFlow participants:

| Name | Role | Responsibility | Attended |
| --- | --- | --- | --- |
| TBD | Support owner | Setup and issue triage | TBD |
| TBD | Product owner | Feedback and roadmap review | TBD |

## 4. Scenarios Tested

Scenario checklist:

- [ ] Package installation or deployment validation.
- [ ] Permission assignment for Admin, Approver, and Viewer.
- [ ] Hosted API health check.
- [ ] Hosted DB health check.
- [ ] Callout configuration validation.
- [ ] Standard `FLOW_FAILURE` test incident.
- [ ] Sentinel Incident write-back.
- [ ] Risk score and risk level review.
- [ ] Policy decision review.
- [ ] Recommendation and runbook review.
- [ ] Approval workflow.
- [ ] Rejection workflow.
- [ ] Approved Case creation.
- [ ] Replay Timeline review.
- [ ] Dashboard review.
- [ ] Org Health Score review.
- [ ] Support escalation test or discussion.

Scenario notes:

| Scenario | Result | Evidence | Notes |
| --- | --- | --- | --- |
| `FLOW_FAILURE` test incident | TBD | Sentinel Incident id: TBD | TBD |
| Approval workflow | TBD | Audit/replay event: TBD | TBD |
| Case creation | TBD | Case id: TBD | TBD |
| Replay Timeline | TBD | Event list: TBD | TBD |
| Dashboard + Org Health Score | TBD | Screenshot/notes: TBD | TBD |

## 5. What Worked Well

Capture strengths:

- Installation/setup:
- Permission model:
- Hosted API connection:
- Incident intake:
- Risk and policy output:
- Recommendation/runbook usefulness:
- Approval workflow:
- Case creation:
- Replay Timeline:
- Dashboard and Org Health Score:
- Support experience:

Customer quotes or paraphrased feedback:

```text
TBD
```

## 6. Issues Found

Issue summary:

| Issue | Severity | Area | Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TBD | P0/P1/P2/P3/P4 | TBD | TBD | TBD | TBD |

Severity guidance:

- P0: pilot-blocking outage, security/privacy issue, unsafe execution, or approval bypass.
- P1: core workflow blocker with no reasonable workaround.
- P2: onboarding, documentation, replay, dashboard, or support issue that slows adoption.
- P3: enhancement or future roadmap request.
- P4: backlog idea or non-blocking preference.

Issue handling notes:

- Link production-impacting issues to production issue tracking.
- Link patch-worthy issues to v1.0.1 patch planning.
- Link roadmap requests to feedback-to-roadmap review.
- Capture workarounds when available.

## 7. Feature Requests

Feature request summary:

| Request | Customer value | Priority | Target path | Notes |
| --- | --- | --- | --- | --- |
| TBD | TBD | P2/P3/P4 | v1.0.1 / future roadmap / backlog | TBD |

Classification guidance:

- v1.0.1 candidate: low-risk onboarding, documentation, stability, or trust improvement.
- Future roadmap: larger feature, integration, AI architecture change, Agentforce work, or analytics improvement.
- Backlog: useful idea without near-term pilot impact.

## 8. Security/Privacy Concerns

Security/privacy review:

- [ ] No secrets or credentials were entered in incident text.
- [ ] No secrets were visible in screenshots.
- [ ] No secrets were visible in Replay Timeline.
- [ ] No secrets were visible in Salesforce error logs.
- [ ] API key/shared-secret handling was explained.
- [ ] Human approval boundary was understood.
- [ ] Viewer read-only expectations were discussed.
- [ ] Data privacy constraints were discussed.

Concerns:

| Concern | Severity | Evidence | Decision | Owner |
| --- | --- | --- | --- | --- |
| TBD | P0/P1/P2/P3/P4 | TBD | TBD | TBD |

Escalation rule:

- Treat possible security, privacy, secret exposure, unsafe execution, approval bypass, or inappropriate data visibility as P0/P1 until reviewed.

## 9. Onboarding Friction

Onboarding friction areas:

- Package installation:
- Permission assignment:
- Remote Site or Named Credential setup:
- Hosted API health validation:
- Hosted DB health validation:
- API key/shared-secret setup:
- Test incident execution:
- Approval panel discovery:
- Case creation validation:
- Replay Timeline discovery:
- Dashboard discovery:
- Support handoff:

Friction summary:

| Friction point | Impact | Suggested fix | Target milestone |
| --- | --- | --- | --- |
| TBD | Low/Medium/High | TBD | v1.0.1 / future roadmap |

## 10. Product Value Score

Score the pilot value from 1 to 5:

| Score | Meaning |
| --- | --- |
| 1 | Not valuable for current workflow. |
| 2 | Some value, but significant blockers or unclear fit. |
| 3 | Useful with improvements. |
| 4 | Valuable and likely to continue after fixes. |
| 5 | Strong value and clear rollout candidate. |

Product value score:

```text
Score:
Reason:
```

Supporting signals:

- Customer understood the workflow.
- Customer trusted approval and replay evidence.
- Customer saw a real use case.
- Customer wants a follow-up pilot phase.
- Customer identified concrete improvements.

## 11. Go/No-Go Recommendation

Recommendation:

- [ ] Go: proceed to broader pilot or next customer.
- [ ] Conditional go: proceed after listed fixes or workarounds.
- [ ] Extend pilot: more validation needed.
- [ ] Patch before expanding: resolve v1.0.1 candidates first.
- [ ] No-go: pause rollout for this customer or workflow.

Recommendation rationale:

```text
TBD
```

Go/no-go blockers:

| Blocker | Severity | Required action | Owner | Target date |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## 12. Action Items

Action item tracker:

| Action item | Owner | Due date | Target milestone | Status |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | 27D / 27E / v1.0.1 / roadmap | TBD |

Action item categories:

- Customer follow-up.
- Support issue.
- Documentation update.
- v1.0.1 patch candidate.
- Security/privacy review.
- Product roadmap item.
- Demo/onboarding improvement.

## 13. Follow-Up Owner

Primary follow-up owner:

```text
Name:
Role:
Contact:
```

Customer follow-up owner:

```text
Name:
Role:
Contact:
```

Follow-up cadence:

- Immediate for P0/P1 issues.
- Within 1 business day for setup or validation blockers.
- Weekly during pilot observation.
- Final follow-up after pilot success report.

## 14. Target Fix Milestone

Target fix milestone options:

- Immediate hotfix.
- v1.0.1 patch.
- Milestone 27E Pilot Success Report.
- Future roadmap.
- Accepted risk.
- Not planned.

Fix mapping:

| Item | Type | Severity | Target fix milestone | Validation needed |
| --- | --- | --- | --- | --- |
| TBD | Bug / docs / onboarding / feature / security | TBD | TBD | TBD |

Milestone 27D result:

```text
27D - Pilot Feedback Review Template: Complete
Next - 27E Pilot Success Report
```
