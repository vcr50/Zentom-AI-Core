# SentinelFlow Feedback-to-Roadmap Process

## 1. Purpose

This document defines the Milestone 26E feedback-to-roadmap process for SentinelFlow v1.0.0-rc.1 and post-v1 customer rollout.

The goal is to convert customer feedback, support signals, onboarding observations, production issues, usage metrics, and product ideas into clear decisions: fix now, include in the next patch, document a workaround, defer to roadmap, or close as not planned.

This process connects:

- Customer feedback.
- Production issue tracking.
- Customer onboarding.
- Usage monitoring and adoption metrics.
- Support SLA review.
- v1.0.1 patch planning.
- Longer-term roadmap planning.

## 2. Feedback Sources

Feedback sources:

- Beta feedback form.
- Support tickets.
- Customer onboarding notes.
- Production issue tracking.
- SentinelFlow Replay Timeline findings.
- Salesforce error logs.
- Usage/adoption metrics.
- Direct customer calls.

Additional useful inputs:

- Salesforce debug logs.
- Hosted API logs.
- Hosted API error logs.
- Dashboard/Org Health Score review notes.
- Customer success weekly review notes.
- Security review findings.
- Internal QA notes.
- Release-candidate regression notes.

Every feedback item should capture:

- Source.
- Customer/org context.
- Reporter role.
- Date received.
- Related Sentinel Incident id, if applicable.
- Related Case id, if applicable.
- Related `Sentinel_Error_Log__c` id, if applicable.
- Related hosted Zentom incident id, if applicable.
- Severity/priority.
- Classification.
- Requested outcome.

## 3. Feedback Classification

Feedback classifications:

| Classification | Definition | Examples |
| --- | --- | --- |
| Bug | Product behavior does not match expected behavior. | Incident write-back fails, Case creation fails, replay event missing. |
| Usability issue | Feature works but is confusing or inefficient. | Approval panel wording unclear, dashboard layout hard to scan. |
| Documentation gap | Customer needs clearer setup, troubleshooting, or operating guidance. | Base URL verification unclear, permission assignment instructions incomplete. |
| Feature request | New capability or enhancement request. | New dashboard metric, additional runbook, export option. |
| Security concern | Potential security, privacy, authorization, secret handling, or unsafe execution issue. | Suspected approval bypass, API key exposure, data visibility concern. |
| Performance issue | Slowness, timeout, cold start, or scalability concern. | Render cold-start confusion, slow dashboard, callout timeout. |
| Integration request | Request to connect SentinelFlow to another system or workflow. | Slack alerting, Agentforce action, external ticketing integration. |
| AI recommendation quality issue | Recommendation, runbook, root cause, or confidence output does not meet customer expectation. | Wrong runbook, unclear policy rationale, low trust in recommendation. |

Classification rules:

- If a feedback item includes possible security or privacy impact, classify it as `Security concern` until reviewed.
- If a feedback item blocks customer workflow, also link it to production issue tracking.
- If a feedback item is about unclear setup, classify as `Documentation gap` or `Usability issue` before treating it as a feature request.
- If multiple customers report the same issue, mark it as recurring.

## 4. Priority Levels

Priority levels:

| Priority | Definition | Default handling |
| --- | --- | --- |
| P0 | Blocks customer usage or production safety. | Immediate fix, hotfix, or emergency mitigation. |
| P1 | Affects core workflow or trust. | Must fix before broader rollout or next critical customer milestone. |
| P2 | Improves onboarding, support, or customer adoption. | Consider for next patch, especially if repeated. |
| P3 | Enhancement for future release. | Roadmap candidate. |
| P4 | Idea/backlog only. | Backlog parking lot and periodic review. |

Priority mapping guidance:

- Security/privacy risk: P0 or P1.
- Package install blocker: P0 or P1.
- Salesforce write-back failure: P1 unless global outage makes it P0.
- Approval/execution failure: P1 or P2 depending on impact and workaround.
- Dashboard/replay confusion: P2 or P3 depending on adoption impact.
- Documentation clarity issue: P2 or P3.
- New integration request: P3 or P4 unless tied to committed customer rollout.
- Advanced AI/HYBRID hosted model request: P3/P4 unless it becomes a strategic release objective.

## 5. Roadmap Decision Rules

Decision options:

- Must fix now.
- Consider for next patch.
- Add to future roadmap.
- Document workaround.
- Accept risk.
- Close as duplicate.
- Close as not planned.

Must-fix:

- P0/P1 production blockers.
- Security/privacy risks.
- Package install blockers.
- Salesforce write-back failures.
- Approval/execution failures.

Consider for next patch:

- Repeated onboarding confusion.
- Common dashboard/replay requests.
- High-frequency support issues.
- Small improvements that reduce manual setup.
- Repeated P2 issues that slow customer adoption.
- Documentation changes that reduce support burden.
- Low-risk package improvements that can be validated quickly.

Future roadmap:

- Advanced AI/HYBRID hosted model.
- Agentforce integration.
- Setup wizard implementation.
- Named Credential default switch.
- Advanced replay search.
- Customer-facing adoption analytics.
- Tenant-level data retention controls.
- Additional integrations.

Decision criteria:

- Customer impact.
- Number of customers affected.
- Severity.
- Security/privacy relevance.
- Adoption impact.
- Support burden.
- Implementation complexity.
- Validation complexity.
- Release risk.
- Strategic fit.

## 6. Review Cadence

Review cadence:

- Immediate review for P0/P1 feedback.
- Weekly review during early customer rollout.
- Patch-planning review before v1.0.1.
- Monthly roadmap review after stabilization.
- Quarterly strategic roadmap review after broader rollout.

Weekly feedback review agenda:

1. Review new feedback items.
2. Confirm classification.
3. Confirm priority.
4. Link related production issues.
5. Identify repeated feedback patterns.
6. Decide must-fix, next-patch, future-roadmap, workaround, accepted-risk, duplicate, or not-planned.
7. Assign owner.
8. Update customer communication status.
9. Update release/patch mapping.
10. Update roadmap docs when decisions are stable.

Review outputs:

- Prioritized feedback list.
- Next-patch candidates.
- Future roadmap candidates.
- Documentation update candidates.
- Support process improvements.
- Customer communication follow-ups.

## 7. Customer Communication Rules

Customer communication rules:

- Acknowledge customer feedback.
- Confirm whether the item is being treated as bug, usability issue, documentation gap, feature request, security concern, performance issue, integration request, or AI recommendation quality issue.
- Do not promise delivery until the item is accepted into a release or patch plan.
- Explain accepted workarounds clearly.
- Explain not-planned decisions respectfully and briefly.
- Provide target release only after release owner approval.
- Communicate security/privacy issues through the agreed escalation path.

Customer-visible statuses:

```text
Received
Under Review
Accepted for Fix
Planned for Patch
Planned for Future Roadmap
Workaround Available
Not Planned
Closed
```

Customer update should include:

- What was heard.
- Current decision.
- Workaround, if available.
- Expected next review point.
- Whether customer action is needed.

## 8. Backlog Management

Backlog fields:

```text
Feedback ID:
Date received:
Source:
Customer/org:
Reporter role:
Classification:
Priority:
Summary:
Impact:
Evidence:
Related issue:
Related metric:
Decision:
Owner:
Target release:
Customer communication status:
Validation needed:
Status:
```

Backlog statuses:

- New.
- Needs evidence.
- Under review.
- Accepted.
- In progress.
- Ready for validation.
- Validated.
- Planned for patch.
- Planned for future release.
- Workaround documented.
- Accepted risk.
- Duplicate.
- Not planned.
- Closed.

Backlog hygiene rules:

- Every P0/P1 must have an owner.
- Every next-patch candidate must have validation criteria.
- Every future-roadmap item must have a short rationale.
- Duplicates should link to the primary item.
- Stale P4 ideas should be reviewed monthly or quarterly.
- Feedback that becomes a production issue should link to production issue tracking.
- Feedback that becomes a release candidate should link to patch planning.

## 9. Release Planning

Release planning paths:

| Decision | Release path |
| --- | --- |
| Must fix now | Hotfix or immediate patch branch. |
| Next patch | v1.0.1 patch planning. |
| Documentation/support improvement | Documentation update or support process update. |
| Future roadmap | Future minor/major release planning. |
| Accepted risk | Risk register and review date. |
| Not planned | Close with rationale. |

v1.0.1 patch candidates:

- P0/P1 fixes not already hotfixed.
- Repeated P2 onboarding/support blockers.
- Common dashboard/replay trust improvements.
- Small setup improvements that reduce manual support.
- Documentation updates that unblock customer rollout.
- Low-risk security review remediations.

Future release candidates:

- Advanced AI/HYBRID hosted model.
- Agentforce integration.
- Setup wizard implementation.
- Named Credential default switch.
- New integrations.
- Advanced analytics/adoption dashboard.

Release planning rules:

- Do not bundle high-risk architectural changes into a patch unless required.
- Patch items must have clear validation evidence.
- Customer-impacting fixes need communication notes.
- Security/privacy fixes need explicit validation and rollback notes.
- Roadmap items should not block v1.0.1 unless they are must-fix.

## 10. Success Metrics

Process success metrics:

- Feedback items are classified within the weekly review cycle.
- P0/P1 feedback receives immediate review.
- Repeated P2 patterns become patch candidates or documented workarounds.
- Customers receive clear status updates.
- No high-severity feedback is lost.
- Roadmap decisions are traceable to customer evidence.
- v1.0.1 patch planning has clear customer-backed inputs.

Adoption success metrics:

- Customers complete onboarding with fewer support questions.
- Customers understand policy decisions.
- Customers trust Replay Timeline evidence.
- Customers use dashboard during review.
- Customers submit actionable feedback.
- Common setup issues decline over time.

Roadmap health metrics:

- Number of feedback items by classification.
- Number of feedback items by priority.
- Number of repeated themes.
- Number of next-patch candidates.
- Number of future-roadmap candidates.
- Number of closed/not-planned items with rationale.
- Time from feedback received to decision.
- Time from accepted patch item to validation.

Success signal:

```text
Customer feedback consistently turns into either validated fixes, clear workarounds, documented roadmap items, or respectfully closed decisions.
```
