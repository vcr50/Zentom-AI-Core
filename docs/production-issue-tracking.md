# SentinelFlow Production Issue Tracking

## 1. Purpose

This document defines the Milestone 26A production issue tracking process for SentinelFlow v1.0.0-rc.1 and post-v1 customer rollout.

The goal is to make every production issue traceable from intake through triage, ownership, validation, customer communication, release mapping, and weekly review.

This process applies to:

- Hosted Zentom API issues.
- Hosted PostgreSQL and pgvector issues.
- Salesforce package issues.
- Callout, Named Credential, Remote Site, and API authentication issues.
- Approval, execution, Case creation, replay timeline, dashboard, and Org Health Score issues.
- Documentation, setup, onboarding, and support workflow issues.

## 2. Issue Sources

Production issues may come from:

- Customer support requests.
- Salesforce admins and beta/customer users.
- Salesforce debug logs.
- `Sentinel_Error_Log__c` records.
- Hosted API logs.
- Hosted API error log table.
- Render service logs and deploy logs.
- Hosted PostgreSQL health checks.
- Manual production validation runs.
- Uptime or health check monitors.
- Dashboard/replay timeline discrepancies.
- GitHub issues or repository task tracking.
- Internal QA and release-candidate regression testing.

Required source capture:

- Source channel.
- Reporter name or role.
- Customer/org context.
- First observed timestamp.
- Affected environment.
- Related Salesforce record ids.
- Related hosted incident ids.
- Related logs or screenshots.

## 3. Severity Levels

Severity levels:

| Severity | Definition | Examples | Target response |
| --- | --- | --- | --- |
| P0 | Critical outage, data exposure, secret exposure, or unsafe execution risk. | Hosted API unavailable for all customers, secret leaked, approval bypass, unauthorized execution. | Immediate triage. |
| P1 | Major production workflow failure for one or more customers. | Incident callout fails, Case creation fails, approval execution blocked, DB unavailable, package deploy regression. | Same business day triage. |
| P2 | Important defect with workaround or limited blast radius. | Dashboard count mismatch, replay event missing but incident succeeded, intermittent cold-start timeout, setup confusion. | Review within weekly issue process or sooner if customer-facing. |
| P3 | Minor defect, documentation issue, usability issue, or enhancement candidate. | Copy issue, checklist improvement, non-blocking onboarding question. | Backlog review. |

Escalation rule:

- Any security, data privacy, secret handling, or approval-bypass concern is at least P1 until proven otherwise.
- Any possible secret exposure is P0 until contained.
- Any customer-facing production outage is at least P1.

## 4. Issue Status Workflow

Statuses:

```text
New
Triaged
Investigating
Fix In Progress
Fix Ready
Validation In Progress
Validated
Customer Update Sent
Closed
Accepted Risk
Duplicate
Won't Fix
```

Workflow:

1. New issue is captured with required evidence.
2. Triage owner assigns severity and owner.
3. Owner investigates and documents suspected root cause.
4. Fix owner maps issue to hotfix, patch, documentation update, configuration change, or accepted risk.
5. Fix is implemented or mitigation is documented.
6. Validation owner reruns the relevant test path.
7. Customer-facing update is sent when applicable.
8. Issue is closed with evidence, release mapping, and rollback note.

Closure requirements:

- Severity assigned.
- Owner assigned.
- Root cause or accepted unknown documented.
- Fix or mitigation documented.
- Validation evidence captured.
- Customer communication status recorded.
- Patch/release mapping recorded.

## 5. Owner / Triage Rules

Default ownership:

| Issue area | Primary owner | Backup owner |
| --- | --- | --- |
| Salesforce package metadata/Apex/LWC | Salesforce package owner | Release owner |
| Hosted Zentom API | API owner | Release owner |
| Hosted PostgreSQL/pgvector | API/database owner | Release owner |
| Render hosting/deploy | API/hosting owner | Release owner |
| Callout/Named Credential/API auth | Salesforce package owner + API owner | Release owner |
| Security/privacy | Security review owner | Release owner |
| Documentation/setup/support | Documentation owner | Release owner |
| Customer communication | Support owner | Release owner |

Triage rules:

- P0 issues require immediate owner assignment.
- P1 issues require owner assignment the same business day.
- P2 issues require owner assignment during the weekly review or sooner if customer-impacting.
- P3 issues may be grouped into backlog or roadmap review.
- Cross-system issues must have one accountable owner, even when multiple contributors help.

Ownership note:

- The accountable owner is responsible for issue movement, evidence quality, validation, and closure.
- The fix owner and validation owner may be different people.

## 6. Required Evidence

Every production issue should capture:

- Issue id.
- Severity.
- Status.
- Owner.
- Reporter.
- Customer/account/org context.
- Salesforce Org Id.
- Salesforce username or role, if relevant.
- Affected environment.
- First observed timestamp.
- Reproduction steps.
- Expected behavior.
- Actual behavior.
- Business/customer impact.
- Workaround, if available.

Salesforce evidence:

- Sentinel Incident id and name.
- Hosted Zentom incident id.
- `Sentinel_Error_Log__c` id and error type.
- Related Case number/id.
- Replay timeline event list.
- Apex debug log excerpt or log id.
- Permission set assignment details.
- Callout mode: `REMOTE_SITE` or `NAMED_CREDENTIAL`.
- `Zentom_Setting.Default.Base_URL__c` value.

Hosted API/DB evidence:

- Endpoint path.
- HTTP status code.
- Request timestamp.
- Render log timestamp.
- API error log id, if available.
- `/` health result.
- `/api/health/db` result.
- Database type and missing table list.
- pgvector status.

Do not collect:

- Salesforce passwords.
- Session tokens.
- OAuth secrets.
- API keys.
- `X-Zentom-Api-Key` values.
- Database credentials.
- Unredacted regulated personal data.

## 7. Fix Validation

Validation must match issue type:

| Issue type | Minimum validation |
| --- | --- |
| Salesforce metadata/Apex fix | Deploy validation with stable tests; targeted workflow validation. |
| LWC fix | Role-based UI validation for Admin, Approver, and Viewer where applicable. |
| Hosted API fix | Health check, DB health check, endpoint smoke test, log review. |
| DB fix | `/api/health/db`, missing table check, pgvector check, affected workflow retest. |
| Callout/auth fix | Remote Site or Named Credential mode validation, HTTP status verification, secret-not-logged check. |
| Approval/execution fix | Incident approval, execution, Case creation, and replay timeline validation. |
| Documentation/setup fix | Follow the updated steps in a clean or representative org. |

Required validation record:

- Validation date.
- Validator.
- Environment.
- Commands or manual steps.
- Pass/fail result.
- Evidence ids.
- Regression risk.
- Rollback note.

Production fix validation should reference the relevant release candidate, patch branch, commit, deploy id, or tag.

## 8. Release/Patch Mapping

Every issue must map to one of:

- No release required: configuration/support action only.
- Documentation-only update.
- Hotfix.
- v1.0.1 patch.
- Future minor release.
- Roadmap/backlog.
- Accepted risk.

Patch mapping fields:

```text
Issue id:
Severity:
Target release:
Fix commit:
Validation evidence:
Deployment evidence:
Rollback plan:
Customer communication:
```

v1.0.1 patch candidates:

- P0/P1 fixes that do not require immediate hotfix but must not wait for a minor release.
- Repeated P2 customer-impacting issues.
- Documentation/setup fixes that reduce support burden.
- Security-review remediation items accepted for first patch.

Accepted-risk requirements:

- Risk owner.
- Reason accepted.
- Customer impact.
- Mitigation.
- Review date.
- Future target milestone or release.

## 9. Customer Communication Rule

Customer-facing issues require clear communication.

Communication checkpoints:

- Initial acknowledgement.
- Severity/impact confirmation.
- Workaround or mitigation, if available.
- Fix status update.
- Validation confirmation.
- Closure summary.

Communication rules:

- Do not expose internal secrets, stack traces, credentials, or unrelated customer data.
- Do not overpromise release timing.
- Give concrete next steps and expected update windows.
- P0/P1 issues need proactive updates until mitigated or resolved.
- If customer action is required, provide exact steps and rollback guidance.

Customer closure summary should include:

- What happened.
- What was affected.
- What changed.
- How it was validated.
- Any customer action required.
- Support contact/follow-up path.

## 10. Weekly Review Process

Weekly review agenda:

1. Review open P0/P1 issues.
2. Review aging P2 issues.
3. Review customer-impacting P3 issues.
4. Confirm owner and next action for every open issue.
5. Confirm validation evidence for recently fixed issues.
6. Map fixed issues to hotfix, patch, docs update, or roadmap.
7. Identify repeated issue patterns.
8. Decide whether any item should become a v1.0.1 patch candidate.
9. Update customer communication status.
10. Update roadmap or maintenance docs when needed.

Weekly review outputs:

- Updated issue statuses.
- Updated owner assignments.
- Patch candidate list.
- Accepted-risk list.
- Documentation update list.
- Customer follow-up list.
- Roadmap input list.

Milestone 26 linkage:

- 26A owns the issue tracking process.
- 26B uses recurring onboarding issues to improve onboarding.
- 26C uses severity and communication patterns to set support SLA.
- 26D uses issue volume and workflow events as adoption/health signals.
- 26E converts repeated feedback into roadmap candidates.
- 26F maps validated fixes into v1.0.1 patch planning.
