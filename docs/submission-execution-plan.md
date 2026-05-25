# SentinelFlow Submission Execution Plan

## 1. Purpose

This document starts Milestone 29 Submission Execution and defines 29A Submission Account / Partner Setup Verification.

Goal:

```text
Move from submission planning to actual AppExchange / AgentExchange submission execution by verifying publisher account readiness, package/version readiness, evidence readiness, listing/demo assets, blockers, and submission status tracking.
```

Milestone 29 should focus on executing the marketplace submission workflow, uploading/attaching required assets, submitting review materials, and tracking review feedback.

## 2. Submission Target

Primary target:

```text
AppExchange / AgentExchange marketplace submission for SentinelFlow.
```

Product positioning:

```text
SentinelFlow
Salesforce-native incident intelligence and governed automation powered by the Zentom AI OS.
```

Submission type:

- Salesforce package listing.
- Security review submission.
- Marketplace listing assets submission.
- Demo/screenshot asset submission.
- Support/privacy/security reference submission.

Current submission scope:

- Salesforce-native SentinelFlow package.
- Hosted Zentom API integration.
- Risk scoring.
- Policy decisions.
- Recommendation/runbook output.
- Human approval.
- Safe Case creation.
- Replay Timeline.
- Dashboard and Org Health Score.
- Support and security evidence.

Out of current submission scope:

- Full autonomous remediation.
- Hosted HYBRID Ollama.
- Agentforce production integration.
- Major AI architecture changes.
- Large object model changes.

## 3. Partner / Publisher Account Readiness

Partner / publisher account checklist:

- [ ] Salesforce Partner Community access confirmed.
- [ ] AppExchange / AgentExchange publisher account confirmed.
- [ ] Publisher profile name confirmed:

```text
Tomcodex
```

- [ ] Authorized submission owner identified.
- [ ] Security review submitter identified.
- [ ] Listing editor identified.
- [ ] Technical contact identified.
- [ ] Support contact identified.
- [ ] Billing/tax/business account requirements confirmed, if applicable.
- [ ] Required publisher agreements accepted.
- [ ] Submission workspace/project created, if applicable.
- [ ] Access to package upload or package version area confirmed.
- [ ] Access to listing asset upload area confirmed.
- [ ] Access to security review submission area confirmed.

Evidence to capture:

```text
Publisher account:
Submission owner:
Security review owner:
Listing owner:
Technical contact:
Support contact:
Account readiness result:
Open account blockers:
```

29A pass criteria:

```text
Partner/publisher account can access the required submission, package, listing, and security review workflows.
```

## 4. Package Version Readiness

Package/version readiness checklist:

- [ ] Final package manifest confirmed.
- [ ] Package version or deployable submission candidate identified.
- [ ] Release candidate reference confirmed:

```text
v1.0.0-rc.1
```

- [ ] Target commit/reference confirmed.
- [ ] Package deploy validation evidence attached.
- [ ] 17 passing / 0 failing tests evidence attached.
- [ ] Fresh org validation evidence attached.
- [ ] Final install/test org validation executed or scheduled.
- [ ] No experimental Agentforce metadata included.
- [ ] No temporary files included.
- [ ] No hardcoded secrets included.
- [ ] No local-only URLs included.
- [ ] No public Ollama endpoint included.

Package evidence references:

- `docs/install-test-org-final-validation.md`
- `docs/security-review-evidence-cross-check.md`
- `docs/security-review-evidence-pack.md`
- `docs/appexchange-submission-checklist.md`

Package readiness result:

```text
Ready / Conditional / Blocked
```

## 5. Security Review Evidence Readiness

Security review evidence checklist:

- [ ] Security review evidence pack ready.
- [ ] Security review final checklist ready.
- [ ] Security review preparation doc ready.
- [ ] CRUD/FLS + sharing review ready.
- [ ] Apex/LWC security scan checklist ready.
- [ ] Data privacy and retention doc ready.
- [ ] Salesforce callout security doc ready.
- [ ] Named Credential evidence ready.
- [ ] API authentication evidence ready.
- [ ] Shared secret auth evidence ready.
- [ ] Error logging evidence ready.
- [ ] Hosted API and DB evidence ready.
- [ ] Known gaps and mitigations ready.
- [ ] Security review evidence cross-check complete.

Key evidence:

- `v1.0.0-rc.1` tag.
- Production validation commit `92e344c`.
- Package tests: 17 passing / 0 failing.
- Fresh org validation passed.
- Hosted API live.
- Hosted DB + pgvector verified.
- Named Credential path validated.
- Shared secret auth implemented.
- Error logging implemented.

Security review evidence references:

- `docs/security-review-evidence-pack.md`
- `docs/security-review-final-checklist.md`
- `docs/security-review-preparation.md`
- `docs/security-review-evidence-cross-check.md`
- `docs/data-privacy-retention.md`
- `docs/salesforce-callout-security.md`
- `docs/apex-lwc-security-scan-checklist.md`
- `docs/crud-fls-sharing-review.md`

Security readiness result:

```text
Ready / Conditional / Blocked
```

## 6. Listing Asset Readiness

Listing asset checklist:

- [ ] Product name finalized.
- [ ] Tagline finalized.
- [ ] Short description finalized.
- [ ] Long description finalized.
- [ ] Key features finalized.
- [ ] Target users finalized.
- [ ] Category / keywords finalized.
- [ ] Screenshot list finalized.
- [ ] Logo / brand assets prepared.
- [ ] Support contact placeholder replaced.
- [ ] Documentation URL finalized.
- [ ] Privacy/security links finalized.
- [ ] Listing review checklist complete.
- [ ] No unsupported claims remain.

Listing references:

- `docs/final-listing-assets.md`
- `docs/publisher-listing-copy.md`
- `docs/appexchange-submission-checklist.md`

Listing readiness result:

```text
Ready / Conditional / Blocked
```

## 7. Demo Asset Readiness

Demo asset checklist:

- [ ] Final screenshot list approved.
- [ ] Required screenshots captured.
- [ ] Screenshot filenames follow convention.
- [ ] Screenshots pass visual QA.
- [ ] Screenshots contain no customer data.
- [ ] Screenshots contain no secrets.
- [ ] Demo video flow approved.
- [ ] Demo video recorded or approved.
- [ ] Demo script approved.
- [ ] Demo transcript/captions prepared if required.
- [ ] Demo claims match validated product behavior.
- [ ] Security/governance explanation included.

Required screenshots:

- SentinelFlow App Home / Dashboard.
- Sentinel Incident record.
- AI Recommendation section.
- Human Approval panel.
- Replay Timeline.
- Policy Decision record.
- Audit Log list.
- Case created from approved action.
- Org Health Score card.

Demo references:

- `docs/screenshots-demo-script-finalization.md`
- `docs/pilot-demo-script.md`

Demo readiness result:

```text
Ready / Conditional / Blocked
```

## 8. Submission Steps

Submission execution steps:

1. Confirm publisher account access.
2. Confirm submission owner and contacts.
3. Confirm package version or upload candidate.
4. Run or attach final install/test org validation evidence.
5. Attach package validation evidence.
6. Attach security review evidence.
7. Finalize listing copy fields.
8. Upload logo and brand assets.
9. Upload screenshots.
10. Upload or link demo video.
11. Add support contact and documentation links.
12. Add privacy/security links.
13. Review listing claims against validated scope.
14. Submit security review package/materials.
15. Submit listing for marketplace review.
16. Record submission ids, dates, owners, and status.
17. Track Salesforce review feedback.
18. Route blockers to remediation owner.
19. Update maintenance log with execution evidence.

Submission evidence to capture:

```text
Submission date:
Submission owner:
Package/version submitted:
Security review submission id:
Listing submission id:
Uploaded screenshot set:
Demo asset:
Support URL:
Privacy/security links:
Initial status:
```

## 9. Submission Blockers

Potential blockers:

| Blocker | Severity | Owner | Required action | Status |
| --- | --- | --- | --- | --- |
| Publisher account access missing | P0 | TBD | Restore/obtain access. | TBD |
| Package/version upload unavailable | P0 | TBD | Resolve packaging blocker. | TBD |
| Final validation not executed | P1 | TBD | Run 28E validation. | TBD |
| Apex tests fail | P0 | TBD | Fix and revalidate. | TBD |
| Hosted API/DB unavailable | P0/P1 | TBD | Restore service or document accepted workaround. | TBD |
| Screenshots/demo missing | P1 | TBD | Capture and review final assets. | TBD |
| Support placeholders remain | P1 | TBD | Replace with real contacts/URLs. | TBD |
| Security evidence gap | P0/P1 | TBD | Complete evidence or remediate. | TBD |
| Unsupported listing claim | P1 | TBD | Revise copy/demo. | TBD |
| Secret/customer data in assets | P0 | TBD | Remove and regenerate assets. | TBD |

No-go blockers:

- Package deploy/test failure.
- Missing security review evidence.
- Unresolved security/privacy issue.
- Secret exposure in docs, screenshots, demo, logs, or listing assets.
- Unsupported autonomous remediation claim.
- Unsupported Agentforce production integration claim.
- Unsupported hosted HYBRID Ollama claim.
- Missing submission owner or account access.

## 10. Submission Status Tracker

Status tracker:

| Area | Owner | Status | Evidence / link | Notes |
| --- | --- | --- | --- | --- |
| Partner/publisher account | TBD | Not started | TBD | 29A |
| Package version/upload | TBD | Not started | TBD | 29B |
| Security review submission | TBD | Not started | TBD | 29C |
| Listing submission | TBD | Not started | TBD | 29D |
| Review feedback tracking | TBD | Not started | TBD | 29E |
| Submission wrap-up | TBD | Not started | TBD | 29F |

Recommended Milestone 29 breakdown:

- 29A: Submission Account / Partner Setup Verification.
- 29B: Package Version / Upload Preparation.
- 29C: Security Review Submission Execution.
- 29D: Listing Submission Execution.
- 29E: Review Feedback Tracking.
- 29F: Submission Wrap-up.

Milestone 29A result:

```text
29A - Submission Account / Partner Setup Verification: Complete when publisher account access, owners, and submission workspaces are verified.
Next - 29B Package Version / Upload Preparation
```
