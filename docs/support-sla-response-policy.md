# SentinelFlow Support SLA and Response Policy

## 1. Purpose

This document defines the Milestone 26C support SLA and response policy for SentinelFlow v1.0.0-rc.1, early customer rollout, and post-v1 stabilization.

The goal is to set clear expectations for support scope, support channels, severity classification, response targets, resolution/workaround targets, escalation, customer responsibilities, Tomcodex/Zentom responsibilities, and recurring review.

This policy works with:

- `docs/production-issue-tracking.md`
- `docs/customer-onboarding-checklist.md`
- `docs/support-troubleshooting-guide.md`
- `docs/render-uptime-strategy.md`

## 2. Support Scope

In scope:

- SentinelFlow Salesforce package installation support.
- SentinelFlow permission assignment support.
- `Zentom_Setting__mdt` configuration support.
- Remote Site Setting and Named Credential mode support.
- Hosted Zentom API connectivity support.
- Hosted PostgreSQL / pgvector health triage.
- Incident processing and Salesforce write-back support.
- Approval and execution workflow support.
- Safe Case creation support.
- Replay Timeline support.
- Dashboard and Org Health Score support.
- Salesforce-side error log review.
- Hosted API error/log evidence review.
- Customer onboarding questions.
- Documentation clarification.

Security-sensitive support is also in scope:

- Suspected secret exposure.
- Suspected approval bypass.
- Suspected unauthorized execution.
- Suspected customer data exposure.
- Authentication or API key misconfiguration.

## 3. Support Channels

Supported channels during early rollout:

- Designated customer support email or shared inbox.
- Customer onboarding/support thread.
- GitHub issue or internal issue tracker, if enabled for the customer.
- Scheduled onboarding/review call.
- Emergency escalation channel for P0 issues, when agreed with the customer.

Required intake details:

- Customer name.
- Salesforce Org Id.
- Target org type: sandbox, developer, or production.
- Reporter name and role.
- Severity requested by customer.
- Business impact.
- First observed timestamp.
- Related Sentinel Incident id/name.
- Related hosted Zentom incident id.
- Related Case id/number.
- Related `Sentinel_Error_Log__c` id, if available.
- Callout mode: `REMOTE_SITE` or `NAMED_CREDENTIAL`.
- Screenshots or logs with secrets redacted.

Do not send through support channels:

- Salesforce passwords.
- Session tokens.
- OAuth secrets.
- API keys.
- `X-Zentom-Api-Key` values.
- Database credentials.
- Unredacted regulated personal data.

## 4. Severity Levels

Severity levels:

| Severity | Definition | Examples |
| --- | --- | --- |
| P0 | Production outage, install blocked, critical security issue, secret exposure, data exposure, or unsafe execution risk. | Production customer cannot install or use SentinelFlow, hosted API unavailable for production, approval bypass suspected, API key exposed. |
| P1 | Incident processing or Salesforce write-back blocked. | Salesforce callout fails, no Sentinel Incident is created, hosted API accepts request but Salesforce write-back fails, DB outage blocks processing. |
| P2 | Approval, execution, replay, dashboard, or Org Health Score issue. | Approval panel fails, Case creation fails after approval, Replay Timeline missing events, dashboard does not load, Org Health Score incorrect. |
| P3 | UI, documentation, setup clarity, minor defect, or non-blocking workflow issue. | Confusing setup step, incorrect help text, minor dashboard display issue, documentation typo. |
| P4 | Feature request, enhancement, product idea, or roadmap request. | New dashboard metric, new runbook, advanced workflow request, integration request. |

Severity escalation rules:

- Suspected secret exposure is P0 until contained.
- Suspected approval bypass or unauthorized execution is P0 until disproven.
- Customer-facing production outage is at least P1.
- Install blocked for a production customer is P0.
- Install blocked for sandbox/developer onboarding is usually P1 unless tied to go-live timing.
- Repeated P2 issues affecting multiple customers may be escalated to P1.

## 5. Response Time Targets

Response targets are measured during agreed business hours unless a separate customer agreement says otherwise.

| Severity | Initial response target |
| --- | --- |
| P0 - Production outage / install blocked | 4 business hours |
| P1 - Incident processing or Salesforce write-back blocked | 1 business day |
| P2 - Approval, execution, replay, or dashboard issue | 2 business days |
| P3 - UI/documentation/minor defect | 3 business days |
| P4 - Feature request / enhancement | Best effort |

Initial response means:

- Acknowledge the issue.
- Confirm severity or request missing evidence.
- Identify the initial owner or triage path.
- Provide next expected update timing.

Response targets do not guarantee final resolution. Resolution targets are defined separately.

## 6. Resolution Targets

Resolution/workaround targets:

| Severity | Target resolution or workaround |
| --- | --- |
| P0 - Production outage / install blocked | 1 business day |
| P1 - Incident processing or Salesforce write-back blocked | 2 business days |
| P2 - Approval, execution, replay, or dashboard issue | 5 business days |
| P3 - UI/documentation/minor defect | Next planned patch |
| P4 - Feature request / enhancement | Roadmap review |

Resolution may mean:

- Product fix.
- Configuration correction.
- Hosted service recovery.
- Documented workaround.
- Patch release.
- Accepted risk with customer approval.

Resolution targets may change when:

- Customer evidence is incomplete.
- Customer admin access is unavailable.
- Salesforce org-specific configuration blocks validation.
- Third-party infrastructure is unavailable.
- Fix requires package/security-review-significant change.
- Customer chooses to defer remediation.

## 7. Escalation Rules

Escalate immediately when:

- P0 is reported or suspected.
- Secret exposure is possible.
- Customer data exposure is possible.
- Approval or execution can be bypassed.
- Hosted API is down for production customers.
- Customer production install is blocked.
- Multiple customers report the same P1/P2 pattern.

Escalation path:

1. Support owner confirms evidence and severity.
2. Release owner is notified for P0/P1.
3. Salesforce package owner is assigned for package/Apex/LWC/permission issues.
4. API/database owner is assigned for hosted API, database, Render, or pgvector issues.
5. Security review owner is assigned for security/privacy/secret issues.
6. Customer communication owner sends updates.
7. Patch or hotfix owner maps the issue to hotfix, v1.0.1, future release, or accepted risk.

Escalation evidence must include:

- Impact summary.
- Customer/org context.
- Reproduction steps.
- Relevant Salesforce ids.
- Relevant hosted API/DB evidence.
- Workaround status.
- Current customer communication status.

## 8. Customer Responsibilities

Customer responsibilities:

- Provide Salesforce admin access through an authorized customer admin.
- Confirm target org type: sandbox, developer, or production.
- Assign appropriate SentinelFlow permission sets.
- Maintain Salesforce user/profile/permission hygiene.
- Confirm Case object requirements in the target org.
- Provide accurate issue evidence and timestamps.
- Provide redacted screenshots/logs when requested.
- Avoid sending secrets or regulated personal data through support channels.
- Avoid placing sensitive personal data in free-form incident error messages.
- Approve production configuration changes.
- Validate fixes or workarounds in the customer org when required.
- Notify Tomcodex/Zentom before go-live-critical onboarding windows when possible.

Customer support evidence should not include:

- Passwords.
- Session ids.
- OAuth tokens.
- API keys.
- Database credentials.
- Full unredacted customer data exports.

## 9. Tomcodex / Zentom Responsibilities

Tomcodex/Zentom responsibilities:

- Acknowledge issues within the response targets.
- Triage severity based on evidence and customer impact.
- Assign an accountable owner.
- Protect customer-provided evidence.
- Avoid requesting unnecessary sensitive data.
- Provide troubleshooting steps or workaround guidance.
- Investigate SentinelFlow package, hosted API, hosted DB, callout, approval, execution, replay, and dashboard issues in scope.
- Keep customer communications clear and time-bound.
- Validate fixes against relevant workflow paths.
- Map fixes to hotfix, patch, future release, documentation update, or accepted risk.
- Maintain production issue records using `docs/production-issue-tracking.md`.

Tomcodex/Zentom will not:

- Ask customers to share passwords or secrets in plain text.
- Guarantee strict production SLA on beta/free-tier hosting.
- Modify customer Salesforce configuration without customer approval.
- Treat feature requests as committed delivery without roadmap review.

## 10. Out-of-Scope Support

Out of scope unless separately agreed:

- General Salesforce administration unrelated to SentinelFlow.
- Customer-specific Apex, Flow, validation rule, trigger, or automation debugging outside SentinelFlow integration points.
- Data cleanup unrelated to SentinelFlow records.
- Custom report/dashboard development outside included SentinelFlow dashboards.
- Custom runbook development beyond agreed onboarding scope.
- Third-party system outages not controlled by Tomcodex/Zentom.
- Customer network/security policy changes.
- Production hosting guarantees on free-tier infrastructure.
- Guaranteed timelines for feature requests.

Out-of-scope items may be:

- Converted to roadmap requests.
- Handled as paid/custom implementation.
- Documented as customer responsibility.
- Accepted as unsupported for the current release.

## 11. Beta / Early Customer Notes

Early customer caveats:

- Hosted beta uses Render, so cold-start delay may occur.
- First request after inactivity may be slower or may require retry.
- Critical production customers should use always-on hosting before strict SLA.
- Render free-tier behavior should be treated as beta/early rollout infrastructure, not a strict production SLA foundation.
- Named Credential mode has been validated, but Remote Site mode remains the safe fallback unless the customer is explicitly configured for `NAMED_CREDENTIAL`.
- Hosted mode uses deterministic RULE-mode behavior.
- Local Ollama/HYBRID demo mode is not part of hosted customer support unless separately agreed.

Cold-start handling:

- Wake `https://zentom-api.onrender.com/`.
- Retry `/api/health/db`.
- Retry the Salesforce test incident after 30-60 seconds.
- Record cold-start behavior separately from product logic failures.

Strict SLA readiness:

- Use paid always-on Render hosting or another always-on cloud runtime.
- Confirm monitoring and alert routing.
- Confirm backup/restore expectations.
- Confirm customer production support window.
- Confirm P0 escalation channel.

## 12. Review Cadence

Review cadence:

- Weekly review during early customer rollout.
- Immediate review after any P0.
- Same-week review after repeated P1/P2 patterns.
- Monthly review after stabilization.
- Patch-planning review before v1.0.1.

Weekly review inputs:

- Open production issues.
- SLA misses.
- P0/P1 incidents.
- Aging P2 items.
- Customer onboarding blockers.
- Repeated support questions.
- Feature requests.
- Documentation gaps.
- Patch candidates.

Weekly review outputs:

- Updated issue severity/status.
- Updated owner assignments.
- Customer communication follow-ups.
- Workaround or patch decisions.
- Documentation updates.
- Roadmap candidates.
- v1.0.1 patch candidates.

Policy review should update:

- Response targets, if support capacity changes.
- Resolution targets, if infrastructure changes.
- Escalation contacts.
- Customer communication templates.
- Support scope as the product moves from early rollout to broader production use.
