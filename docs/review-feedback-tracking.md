# SentinelFlow Review Feedback Tracking

## 1. Purpose

This document defines Milestone 29E for tracking AppExchange / AgentExchange and Salesforce security review feedback after submission.

Goal:

```text
Track every marketplace, listing, package, and security review response from receipt through triage, remediation, validation, re-submission, and closure.
```

This is an execution tracker. It should be updated as actual review feedback is received.

## 2. Feedback Sources

Feedback sources:

- Salesforce security review feedback.
- AppExchange listing review feedback.
- AgentExchange listing review feedback.
- Package upload/package version feedback.
- Partner/publisher account feedback.
- Demo video or screenshot review feedback.
- Privacy/security documentation review feedback.
- Support/contact review feedback.
- Customer pilot or implementation evidence feedback.
- Internal submission owner review notes.

Feedback intake checklist:

- [ ] Feedback source recorded.
- [ ] Date received recorded.
- [ ] Reviewer/contact recorded, if available.
- [ ] Submission id or listing id linked.
- [ ] Package/version linked, if applicable.
- [ ] Evidence or screenshot captured.
- [ ] Severity/priority assigned.
- [ ] Owner assigned.
- [ ] Status assigned.

## 3. Feedback Statuses

Allowed statuses:

```text
Received
Under Review
Accepted
Rejected
Fix In Progress
Fix Validated
Re-submitted
Closed
```

Status definitions:

| Status | Definition |
| --- | --- |
| Received | Feedback has been received but not yet triaged. |
| Under Review | Feedback is being reviewed for validity, scope, severity, and owner. |
| Accepted | Feedback is accepted as requiring action, response, fix, documentation update, or resubmission. |
| Rejected | Feedback is not accepted, with rationale documented. Use carefully for reviewer-facing items. |
| Fix In Progress | Code, metadata, listing, asset, documentation, or evidence fix is underway. |
| Fix Validated | Fix has been validated with appropriate evidence. |
| Re-submitted | Response, package, listing, or evidence has been re-submitted. |
| Closed | Reviewer accepted the response, or item is otherwise fully resolved. |

Status transition guidance:

- `Received` -> `Under Review`.
- `Under Review` -> `Accepted` or `Rejected`.
- `Accepted` -> `Fix In Progress`.
- `Fix In Progress` -> `Fix Validated`.
- `Fix Validated` -> `Re-submitted`.
- `Re-submitted` -> `Closed` or back to `Under Review` if additional reviewer feedback is received.

## 4. Severity / Priority Levels

Severity levels:

| Severity | Meaning | Default response |
| --- | --- | --- |
| P0 | Submission-blocking security, privacy, package install, test, secret exposure, approval bypass, unsafe execution, or critical listing issue. | Immediate owner assignment and remediation. |
| P1 | Required reviewer change that blocks approval but has a clear remediation path. | Fix before next re-submission. |
| P2 | Important issue that may not block approval but affects trust, clarity, supportability, or documentation quality. | Fix or respond before final approval where practical. |
| P3 | Suggested improvement, wording clarification, or non-blocking asset change. | Address if low-risk or track for later. |
| P4 | Backlog idea or post-approval improvement. | Track outside submission unless reviewer requires action. |

Priority rules:

- Treat security/privacy issues as P0/P1 until reviewed.
- Treat package deploy/test failures as P0.
- Treat unsupported listing claims as P1 unless they create security/privacy risk, then P0.
- Treat screenshot/demo secret exposure as P0.
- Treat missing support/privacy links as P1.
- Treat cosmetic listing changes as P2/P3 unless reviewer blocks approval.

## 5. Review Owner

Required owners:

| Area | Owner | Backup | Notes |
| --- | --- | --- | --- |
| Security review | TBD | TBD | Owns security reviewer responses and evidence. |
| Package/version | TBD | TBD | Owns package fixes, uploads, and validation. |
| Listing copy/assets | TBD | TBD | Owns listing text, screenshots, demo, and brand assets. |
| Privacy/legal | TBD | TBD | Owns privacy/security language and data handling responses. |
| Support/contact | TBD | TBD | Owns support URL/contact and SLA references. |
| Maintenance log | TBD | TBD | Owns documentation of decisions and evidence. |

Owner responsibilities:

- Triage assigned feedback.
- Confirm severity.
- Define response or fix.
- Gather evidence.
- Coordinate validation.
- Update status.
- Prepare reviewer response.
- Update maintenance log when the item affects submission state.

## 6. Response Timeline

Recommended response targets:

| Severity | Initial triage | Response/fix target |
| --- | --- | --- |
| P0 | Same business day | As soon as possible before any re-submission. |
| P1 | 1 business day | 2-3 business days or next approved re-submission window. |
| P2 | 2 business days | 5 business days where practical. |
| P3 | 3 business days | Next planned listing/evidence update. |
| P4 | Best effort | Backlog or future roadmap. |

Timeline rules:

- Do not re-submit with unresolved P0/P1 blockers unless explicitly accepted by submission owner and reviewer process allows it.
- Security/privacy findings should receive immediate visibility.
- Package fixes require validation before response.
- Listing copy fixes require unsupported-claim review before response.
- Screenshot/demo fixes require privacy review before response.

## 7. Evidence Required

Evidence required by feedback type:

| Feedback type | Required evidence |
| --- | --- |
| Package/test issue | Deploy id, test result, changed files, validation org, pass/fail summary. |
| Security issue | Finding, affected code/metadata, remediation, validation, updated evidence doc. |
| CRUD/FLS/sharing issue | Code review, fix evidence, test result, updated CRUD/FLS documentation. |
| Callout/auth issue | Endpoint/config evidence, Named Credential/Remote Site evidence, auth test result. |
| Privacy issue | Data handling explanation, screenshot/log review, updated privacy documentation. |
| Error logging issue | Log record evidence, secret-exposure check, test result. |
| Listing copy issue | Updated copy, reviewer note, unsupported-claim check. |
| Screenshot/demo issue | New asset, privacy check, visual QA checklist. |
| Support/contact issue | Updated email/URL, support docs, escalation path. |

Evidence capture template:

```text
Feedback id:
Submission id:
Source:
Severity:
Owner:
Evidence files/links:
Validation command/result:
Reviewer response:
Maintenance entry:
```

## 8. Remediation Workflow

Remediation workflow:

1. Receive feedback.
2. Record source, date, submission id, and evidence.
3. Set status to `Received`.
4. Assign review owner.
5. Move status to `Under Review`.
6. Classify severity/priority.
7. Accept or reject with rationale.
8. If accepted, define fix or response.
9. Move status to `Fix In Progress`.
10. Implement code, metadata, asset, listing, or documentation fix.
11. Run required validation.
12. Move status to `Fix Validated`.
13. Prepare reviewer response.
14. Re-submit package/listing/evidence/response.
15. Move status to `Re-submitted`.
16. Close when reviewer accepts or submission status is updated.
17. Update maintenance log.

Remediation tracker:

| Feedback id | Source | Summary | Severity | Owner | Status | Target fix | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | Security / Listing / Package / Demo | TBD | P0/P1/P2/P3/P4 | TBD | Received | TBD | TBD |

## 9. Re-submission Checklist

Before re-submission:

- [ ] All P0 issues are resolved.
- [ ] All P1 reviewer blockers are resolved or explicitly accepted with rationale.
- [ ] Package changes have validation evidence.
- [ ] Tests pass where code/metadata changed.
- [ ] Install/test org validation rerun where required.
- [ ] Security evidence updated.
- [ ] Listing copy updated.
- [ ] Screenshots/demo assets updated and privacy-reviewed.
- [ ] Support/privacy links updated.
- [ ] Known limitations still accurate.
- [ ] No unsupported autonomous remediation claim.
- [ ] No unsupported hosted HYBRID Ollama claim.
- [ ] No unsupported Agentforce production integration claim.
- [ ] Submission owner approves re-submission.
- [ ] Maintenance log updated.

Re-submission record:

```text
Re-submission date:
Submission id:
Feedback ids addressed:
Package/version:
Listing version:
Evidence bundle:
Owner:
Status:
Notes:
```

## 10. Final Approval Tracking

Final approval tracker:

| Area | Status | Approval evidence | Owner | Notes |
| --- | --- | --- | --- | --- |
| Security review | Not submitted / In review / Approved / Rejected | TBD | TBD | TBD |
| Package/version | Not submitted / In review / Approved / Rejected | TBD | TBD | TBD |
| Listing | Not submitted / In review / Approved / Rejected | TBD | TBD | TBD |
| Screenshots/demo | Not submitted / In review / Approved / Rejected | TBD | TBD | TBD |
| Support/privacy links | Not submitted / In review / Approved / Rejected | TBD | TBD | TBD |

Final approval criteria:

- [ ] Security review approved or cleared for next step.
- [ ] Package/version approved.
- [ ] Listing approved.
- [ ] Required screenshots/demo approved.
- [ ] Support/privacy links accepted.
- [ ] No open P0/P1 feedback remains.
- [ ] Final approval evidence captured.
- [ ] Maintenance log updated.
- [ ] Submission owner confirms readiness for 29F wrap-up.

Milestone 29E result:

```text
29E - Review Feedback Tracking: Complete when feedback tracker is ready and active for submitted review items.
Next - 29F Submission Wrap-up
```
