# SentinelFlow Package Version / Upload Preparation

## 1. Purpose

This document defines Milestone 29B for preparing the SentinelFlow package version or upload candidate for AppExchange / AgentExchange submission execution.

Goal:

```text
Confirm the package candidate, manifest, validation evidence, metadata scope, upload steps, validation org steps, rollback plan, and readiness criteria before uploading or submitting the package version.
```

This is an execution document. It should be used by the package/submission owner during actual package version preparation and upload.

## 2. Package Version Target

Package target:

```text
SentinelFlow Salesforce package submission candidate
```

Submission milestone:

```text
Milestone 29B - Package Version / Upload Preparation
```

Target package behavior:

- Deploys cleanly.
- Runs stable tests successfully.
- Connects to hosted Zentom API.
- Uses current safe callout default.
- Preserves human approval before execution.
- Supports safe Case creation after approval.
- Records Replay Timeline audit evidence.
- Includes supportable dashboard and Org Health Score behavior.

Package readiness result:

```text
Ready / Conditional / Blocked
```

## 3. Current Release Candidate

Release candidate tag:

```text
v1.0.0-rc.1
```

Current release candidate evidence:

```text
Stable tests: 17 passing / 0 failing
Hosted API: https://zentom-api.onrender.com
Default callout mode: REMOTE_SITE
Named Credential path: validated, not default
```

Production validation reference:

```text
Production validation commit: 92e344c
```

Release candidate notes:

- Hosted API is live.
- Hosted DB and pgvector have been verified.
- Shared secret authentication has been implemented.
- Error logging has been implemented.
- Human approval remains required before execution.
- Full autonomous remediation is not included.
- Hosted HYBRID Ollama is not included.
- Agentforce production integration is not included.

## 4. Package Manifest

Package manifest:

```text
apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml
```

Short manifest reference:

```text
manifest/package-sentinelflow-beta.xml
```

Manifest owner:

```text
TBD
```

Manifest validation checklist:

- [ ] Manifest path exists.
- [ ] Manifest includes stable SentinelFlow metadata.
- [ ] Manifest excludes experimental metadata.
- [ ] Manifest excludes local temporary files.
- [ ] Manifest excludes old static resources or package drift.
- [ ] Manifest aligns with final submission scope.
- [ ] Manifest aligns with final install/test validation plan.

## 5. Pre-upload Validation Checklist

Pre-upload checks:

- [ ] Working tree reviewed for unrelated changes.
- [ ] Package manifest reviewed.
- [ ] Package deploy validation run or latest evidence attached.
- [ ] Stable tests confirm 17 passing / 0 failing.
- [ ] Hosted API health passes.
- [ ] Hosted DB health passes.
- [ ] PostgreSQL verified.
- [ ] pgvector verified.
- [ ] `Zentom_Setting__mdt.Default.Base_URL__c` points to hosted API.
- [ ] Default callout mode confirmed as `REMOTE_SITE`.
- [ ] Named Credential path confirmed as validated but not default.
- [ ] Shared secret auth configuration reviewed.
- [ ] Error logging reviewed.
- [ ] No hardcoded secrets in metadata.
- [ ] No local-only URLs in metadata.
- [ ] No public Ollama endpoint in metadata.
- [ ] Package upload owner assigned.
- [ ] Rollback/re-upload plan reviewed.

Required validation result:

```text
Package deploys cleanly.
Stable tests: 17 passing / 0 failing.
Hosted API works.
Hosted DB works.
```

## 6. Package Metadata Included

Included metadata categories:

- Stable Apex classes.
- Stable Apex tests.
- Stable Lightning Web Components.
- SentinelFlow custom objects.
- SentinelFlow custom fields.
- SentinelFlow custom metadata.
- SentinelFlow app metadata.
- SentinelFlow tabs.
- Page layouts.
- List views.
- Permission sets:
  - `SentinelFlow_Admin`
  - `SentinelFlow_Approver`
  - `SentinelFlow_Viewer`
- Remote Site Setting fallback.
- Named Credential metadata where included for validated path.
- Error log object metadata.
- Policy decision metadata.
- Runbook metadata.

Included functional scope:

- Salesforce incident intake.
- Hosted Zentom API callout.
- Risk scoring result write-back.
- Policy decision write-back.
- Recommendation/runbook write-back.
- Human approval and rejection.
- Approved Case creation.
- Replay Timeline.
- Dashboard.
- Org Health Score.
- Salesforce-side error logging.

## 7. Package Metadata Excluded

Excluded metadata:

- Experimental Agentforce metadata.
- Full autonomous remediation components.
- Hosted HYBRID Ollama configuration.
- Local-only development URLs.
- Hardcoded secrets or API keys.
- Temporary files.
- Old static resources not part of stable package.
- Unstable package drift.
- Large object model changes not required for v1 submission.
- Customer-specific metadata.
- Test-only local configuration.

Exclusion rationale:

- Keep the upload candidate stable and security-reviewable.
- Avoid unsupported marketplace claims.
- Avoid exposing secrets or local infrastructure.
- Preserve the validated v1.0.0-rc.1 behavior.
- Keep Agentforce production integration and hosted HYBRID Ollama out of current submission scope.

## 8. Upload Steps

Package upload preparation steps:

1. Confirm package owner and target upload account.
2. Confirm Partner / publisher account access.
3. Confirm package manifest path.
4. Confirm release candidate tag `v1.0.0-rc.1`.
5. Confirm target commit/reference.
6. Review included/excluded metadata.
7. Run package deploy validation, or attach current final validation evidence.
8. Confirm 17 passing / 0 failing tests.
9. Confirm hosted API and hosted DB health.
10. Confirm callout mode and Named Credential posture.
11. Create package version or upload candidate using the approved Salesforce packaging path.
12. Record package version id or upload id.
13. Attach validation evidence.
14. Record upload timestamp and owner.
15. Update maintenance log with upload evidence.

Upload evidence:

```text
Upload owner:
Upload date:
Package version id:
Upload id:
Release candidate:
Target commit/reference:
Manifest:
Validation id:
Tests passing:
Tests failing:
Notes:
```

## 9. Validation Org Steps

Validation org steps:

1. Identify clean validation org.
2. Confirm admin access.
3. Deploy or install upload candidate.
4. Assign permission sets:
   - `SentinelFlow_Admin`
   - `SentinelFlow_Approver`
   - `SentinelFlow_Viewer`
5. Confirm `Zentom_Setting__mdt.Default.Base_URL__c`.
6. Confirm default callout mode:

```text
REMOTE_SITE
```

7. Confirm Remote Site Setting points to:

```text
https://zentom-api.onrender.com
```

8. Confirm Named Credential path remains available/validated but not default.
9. Run or verify hosted API health.
10. Run or verify hosted DB health.
11. Run standard `FLOW_FAILURE` incident.
12. Confirm Sentinel Incident creation.
13. Confirm approval/execution.
14. Confirm Case creation.
15. Confirm Replay Timeline events.
16. Confirm dashboard and Org Health Score load.
17. Confirm error logging works for safe controlled failure.
18. Capture validation evidence.

Validation evidence:

```text
Validation org:
Org Id:
Deploy/install id:
Permission set assignment result:
Hosted API result:
Hosted DB result:
FLOW_FAILURE incident id:
Created Case id:
Replay result:
Dashboard result:
Error logging result:
Overall result:
```

## 10. Rollback / Re-upload Plan

Rollback triggers:

- Package upload fails.
- Package install fails.
- Stable tests fail.
- Hosted API/DB validation fails.
- Callout/authentication fails.
- Approval/execution fails.
- Case creation fails.
- Replay Timeline fails.
- Dashboard fails.
- Error logging exposes secrets.
- Incorrect metadata included.
- Required metadata missing.

Rollback plan:

1. Stop submission upload flow.
2. Do not attach failed package candidate to final listing.
3. Record failure evidence.
4. Restore or use last known good package manifest.
5. Fix metadata or configuration issue.
6. Re-run deploy validation.
7. Confirm 17 passing / 0 failing tests.
8. Re-run hosted API/DB checks.
9. Re-run standard `FLOW_FAILURE` validation.
10. Create corrected package upload candidate.
11. Record new package version/upload id.
12. Update maintenance log.

Known good fallback:

```text
Release candidate: v1.0.0-rc.1
Hosted API: https://zentom-api.onrender.com
Default callout mode: REMOTE_SITE
Named Credential path: validated, not default
```

## 11. Upload Readiness Criteria

Ready for upload when:

- [ ] Package manifest is confirmed.
- [ ] Release candidate tag is confirmed.
- [ ] Target commit/reference is confirmed.
- [ ] Included metadata matches stable submission scope.
- [ ] Excluded metadata is not present.
- [ ] Deploy validation passes.
- [ ] Stable tests are 17 passing / 0 failing.
- [ ] Hosted API health passes.
- [ ] Hosted DB health passes.
- [ ] Default callout mode is `REMOTE_SITE`.
- [ ] Named Credential path is validated but not default.
- [ ] Shared secret/auth posture is documented.
- [ ] Error logging is validated.
- [ ] No hardcoded secrets exist in metadata.
- [ ] No local-only URLs exist in metadata.
- [ ] Rollback/re-upload plan is documented.
- [ ] Upload owner approves.

Milestone 29B result:

```text
29B - Package Version / Upload Preparation: Complete
Next - 29C Security Review Submission Execution
```
