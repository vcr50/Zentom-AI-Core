# SentinelFlow Security Review Evidence Pack

## 1. Purpose

This evidence pack is the main security-review submission reference for SentinelFlow v1.0.0-rc.1.

It consolidates the release candidate tag, Salesforce package validation, clean-org validation, hosted production validation, security documentation, data privacy documentation, callout security controls, Named Credential validation, API authentication evidence, and accepted gaps with mitigations.

Prepared for:

```text
Milestone 23A - Final Security Review Evidence Pack
```

## 2. Release Candidate Tag

Release candidate:

```text
SentinelFlow v1.0.0-rc.1
```

Git tag:

```text
v1.0.0-rc.1
```

Tag target:

```text
92e344c6fc865ab339d20ee37fec888bafaae1bc
```

Target commit summary:

```text
Document production validation run
```

Annotated tag evidence:

```text
Package validation: 0AfdL00000az6W5SAI
Hardened package deploy: 0AfdL00000azAXBSA2
Hosted API: running
Hosted PostgreSQL: connected
missingTables: []
pgvector: enabled
Live incident: SI-000013, hosted incident id 9
Approval and execution: passed
Case created: 00001051
Replay events: all 8 expected events present
Error logging: SEL-000000, ZENTOM_API_NON_SUCCESS, 404
Salesforce setting restored: https://zentom-api.onrender.com, REMOTE_SITE
```

## 3. Package Validation Evidence

Latest release-candidate package validation:

```text
Validation org: astrosoft
Deploy validation ID: 0AfdL00000az6W5SAI
Tests passing: 17
Tests failing: 0
Status: Passed
```

Hardened package deploy validation:

```text
Validation org: astrosoft
Deploy ID: 0AfdL00000azAXBSA2
Tests passing: 17
Tests failing: 0
Status: Passed
```

Related prior hardening evidence:

```text
18A/18B beta manifest validation: 0AfdL00000ayMNVSA2, 14 passing, 0 failing
18C permission hardening validation: 0AfdL00000ayY5JSAU, 14 passing, 0 failing
18D Remote Site / callout cleanup validation: 0AfdL00000ayYlFSAU, 14 passing, 0 failing
18E metadata cleanup validation: 0AfdL00000aya8jSAA, 14 passing, 0 failing
22A dual callout Apex validation: 0AfdL00000az6erSAA, 15 passing, 0 failing
22B API authentication validation: 0AfdL00000az8lVSAQ, 15 passing, 0 failing
22E Salesforce error log validation: 0AfdL00000azA8zSAE, 17 passing, 0 failing
```

Stable package scope:

- Stable SentinelFlow Apex, LWC, objects, custom metadata, app, tabs, layouts, permission sets, Remote Site Setting, and Named Credential metadata.
- Experimental Agentforce metadata, old static resources, temporary files, and unstable package drift are excluded from the beta package manifest.
- Legacy broad operator metadata remains outside the stable beta manifest.

## 4. Fresh Org Validation Evidence

Clean install validation:

```text
Milestone: 18F fresh org / clean install validation
Scratch org alias: sentinelflow-beta-18f
Scratch deploy ID: 0AfBi000007rTsgKAE
Tests passing: 14
Tests failing: 0
Status: Passed
```

Fresh org validation results:

- Beta package manifest deployed cleanly to the scratch org.
- Permission sets assigned: `SentinelFlow_Admin`, `SentinelFlow_Approver`, and `SentinelFlow_Viewer`.
- `Zentom_Setting__mdt.Default.Base_URL__c` verified as `https://zentom-api.onrender.com`.
- Direct scratch-org callout to the hosted Render API returned HTTP 200.
- Hosted incident flow created scratch-org incident `SI-000000`.
- Hosted DB incident id was `6`.
- Incident result verified risk `95`, level `CRITICAL`, policy `HUMAN_APPROVAL_REQUIRED`, and runbook `FLOW_FAILURE_BASIC_RECOVERY`.
- SentinelFlow app verified in scratch org.
- LWC bundles verified through Tooling API: `zentomApprovalPanel`, `zentomDashboard`, and `zentomReplayTimeline`.
- Approval flow verified: incident moved to `Approved`.
- Execution flow verified: Case `00001028` created with `Origin = SentinelFlow` and priority `High`.
- Replay timeline verified with eight events from incident intake through case creation.

## 5. Production Validation Evidence

Production validation run:

```text
Milestone: 22F production validation run
Date: 2026-05-24
Status: Passed
```

Hosted API evidence:

```text
GET https://zentom-api.onrender.com/
status: running
service: zentom-api
message: Zentom API is ready
```

Hosted DB evidence:

```text
GET https://zentom-api.onrender.com/api/health/db
status: ok
databaseType: postgresql
databaseConfigured: true
missingTables: []
pgvector: enabled
```

The first DB health request returned a transient HTTP 500. Retry passed. This is documented as operational evidence and covered by the Render cold-start/uptime mitigation plan.

Salesforce incident evidence:

```text
Sentinel Incident: SI-000013
Salesforce record id: a0VdL00000R11lhUAB
Hosted Zentom incident id: 9
Risk score: 95
Risk level: CRITICAL
Policy decision: HUMAN_APPROVAL_REQUIRED
Runbook key: FLOW_FAILURE_BASIC_RECOVERY
Status: Approval Required
Approval status: Pending Approval
```

Approval and execution evidence:

```text
ZentomApprovalController.approveIncident(...): passed
ZentomExecutionController.executeApprovedAction(...): passed
Final status: Action Created
Approval_Status__c: Approved
Recommendation_Status__c: Approved
Execution_Status__c: Executed
Execution_Action__c: CREATE_CASE
```

Case creation evidence:

```text
Case number: 00001051
Case id: 500dL00003F2muRQAR
Origin: SentinelFlow
Priority: High
Subject: [SentinelFlow] FLOW_FAILURE - CRITICAL
```

Replay timeline evidence:

```text
INCIDENT_RECEIVED
RISK_CALCULATED
ZENTOM_POLICY_EVALUATED
AI_RECOMMENDATION_GENERATED
RUNBOOK_SELECTED
HUMAN_APPROVED
RUNBOOK_ACTION_EXECUTED
CASE_CREATED
```

Error logging evidence:

```text
Temporary bad path: https://zentom-api.onrender.com/invalid-22f
Sentinel_Error_Log__c: SEL-000000
Record id: a0XdL00000VW1C1UAL
Error_Type__c: ZENTOM_API_NON_SUCCESS
Status_Code__c: 404
Endpoint: https://zentom-api.onrender.com/invalid-22f/api/incidents/receive
```

Restore evidence:

```text
Zentom_Setting.Default.Base_URL__c: https://zentom-api.onrender.com
Callout_Mode__c: REMOTE_SITE
Is_Active__c: true
Restore deploy ID: 0AfdL00000azAiTSAU
```

## 6. Security Review Preparation Docs

Primary security-review documents:

- `docs/security-review-preparation.md`
- `docs/security-review-final-checklist.md`
- `docs/security-model.md`
- `docs/production-v1-readiness-plan.md`
- `docs/v1-documentation-freeze.md`
- `docs/maintenance.md`

Supporting operational documents:

- `docs/install-guide.md`
- `docs/setup-guide.md`
- `docs/support-troubleshooting-guide.md`
- `docs/monitoring-error-alerts.md`
- `docs/backup-recovery-plan.md`
- `docs/render-uptime-strategy.md`
- `docs/marketplace-readiness-wrap-up.md`

Security controls documented:

- Hosted beta and release-candidate mode uses `AI_MODE=RULE`.
- No public Ollama endpoint is exposed.
- No direct LLM execution occurs in the hosted release-candidate flow.
- Policy decisions control execution behavior.
- Production/high-risk actions require human approval.
- Case creation is only available through the approved execution path.
- Replay timeline records incident intake, risk scoring, policy evaluation, recommendation, approval, execution, and Case creation.
- Permission sets separate admin, approver, and viewer roles.
- Secrets are not committed to source control.

## 7. Data Privacy Docs

Primary data privacy document:

```text
docs/data-privacy-retention.md
```

Data sent from Salesforce to Zentom API:

- Org Id.
- Incident type.
- Source.
- Environment.
- Error message.
- Confidence.
- Action type.

Data not sent:

- Salesforce password.
- Salesforce session token.
- OAuth secret.
- API secret.
- Named Credential secret.

Salesforce data storage:

- `Sentinel_Incident__c`
- `Sentinel_Audit_Log__c`
- `Zentom_Policy_Decision__c`
- `Case`

Hosted DB storage:

- `incidents`
- `risk_scores`
- `policy_decisions`
- `ai_recommendations`
- `memory_entries`
- API error logs for sanitized hosted API failure evidence.

Privacy controls and guidance:

- Customers should avoid sending sensitive personal data or regulated data in free-form error messages.
- Hosted beta and release-candidate mode does not use a paid third-party LLM.
- Hosted beta and release-candidate mode does not expose Ollama publicly.
- Dataset exports are manual and are not shared externally by default.
- Hosted DB deletion and export are operational/manual during beta and release-candidate preparation.

## 8. Callout Security Docs

Primary callout security documents:

- `docs/salesforce-callout-security.md`
- `docs/named-credential-migration-plan.md`
- `docs/named-credential-implementation-22a.md`

Current validated fallback:

```text
Remote Site Setting: Zentom_API
Base URL: https://zentom-api.onrender.com
Endpoint path appended by Apex: /api/incidents/receive
```

Validated Named Credential path:

```text
Named Credential: Zentom_API
Endpoint: https://zentom-api.onrender.com
Apex endpoint: callout:Zentom_API/api/incidents/receive
```

Callout security rules:

- Use HTTPS for the hosted API.
- Do not store API keys or secrets in Custom Metadata.
- Do not hardcode secrets in Apex.
- Do not include endpoint paths in Remote Site URLs.
- Keep Remote Site fallback available until the Named Credential path is fully adopted.
- Use Named Credential for the production/security-review callout path.
- Future External Credential and Permission Set Mapping remain the preferred marketplace-ready authentication model.

## 9. Named Credential Validation Evidence

Named Credential implementation status:

```text
Milestone: 22A
Status: Complete
Named Credential metadata: Zentom_API
Default repo callout mode: REMOTE_SITE
Validated Named Credential mode: NAMED_CREDENTIAL
```

Metadata evidence:

- `Zentom_API.namedCredential-meta.xml` exists and points to `https://zentom-api.onrender.com`.
- Beta manifest includes `NamedCredential:Zentom_API`.
- Remote Site Setting remains in the beta manifest as fallback.
- `Zentom_Setting__mdt.Callout_Mode__c` supports `REMOTE_SITE` and `NAMED_CREDENTIAL`.
- `ZentomIncidentClient` supports both endpoint modes.

Remote Site validation:

```text
Deploy ID: 0AfdL00000az7FxSAI
Tests passing: 15
Tests failing: 0
Sentinel Incident: SI-000011
Hosted Zentom incident id: 7
Status: Passed
```

Named Credential validation:

```text
Metadata switch deploy ID: 0AfdL00000az7XhSAI
Callout_Mode__c: NAMED_CREDENTIAL
Apex endpoint: callout:Zentom_API/api/incidents/receive
Sentinel Incident: SI-000012
Hosted Zentom incident id: 8
Status: Passed
```

Named Credential validation result:

- Anonymous Apex `ZentomIncidentClient.sendIncident(...)` completed successfully through the Named Credential endpoint.
- Hosted API received the request.
- Salesforce write-back created a Sentinel Incident.
- Risk, policy, recommendation, runbook, approval status, and incident status were populated correctly.
- Repo default was restored to `REMOTE_SITE` for safe fallback.

## 10. API Authentication Evidence

API authentication milestone:

```text
Milestone: 22B
Status: Complete
Validation deploy ID: 0AfdL00000az8lVSAQ
Tests passing: 15
Tests failing: 0
```

Security behavior:

- Salesforce sends `X-Zentom-Api-Key` when `Zentom_Setting__mdt.Api_Key__c` is populated.
- Hosted API validates `X-Zentom-Api-Key` when `ZENTOM_API_KEY` is configured in the hosted environment.
- If `ZENTOM_API_KEY` is not configured, the API keeps beta-compatible behavior for safe rollout.
- API keys are not committed to Git.
- `ZENTOM_API_KEY` is managed as a hosted environment variable.
- `Api_Key__c` remains blank in committed Custom Metadata.

API smoke test evidence:

```text
Correct key: accepted
Missing key: rejected with HTTP 401
Wrong key: rejected with HTTP 401
Status: Passed
```

Hosted API error logging:

```text
Milestone: 22D
Missing API key smoke test: HTTP 401
api_error_logs row inserted: yes
Secret logging: X-Zentom-Api-Key values are never stored
```

Salesforce-side error logging:

```text
Milestone: 22E
Validation ID: 0AfdL00000azA8zSAE
Tests passing: 17
Tests failing: 0
Failure object: Sentinel_Error_Log__c
Secret logging: API headers and X-Zentom-Api-Key are not stored
```

## 11. Known Gaps And Mitigations

Known gap: External Credential and Permission Set Mapping are not finalized.

Mitigation:

- Named Credential metadata exists and has been validated.
- Dual-mode Apex supports both Remote Site and Named Credential paths.
- Secrets are not stored in Custom Metadata or Apex.
- External Credential and Permission Set Mapping remain documented as the marketplace-ready next step before public listing.

Known gap: Repo default remains `REMOTE_SITE` after validation.

Mitigation:

- Named Credential mode was validated end to end.
- Remote Site fallback remains intentionally available for safe recovery.
- `Callout_Mode__c` can switch the package to `NAMED_CREDENTIAL` after final customer-org configuration is approved.

Known gap: Render/free-tier cold-start or transient hosted DB health behavior may occur.

Mitigation:

- Cold-start behavior is documented in `docs/render-uptime-strategy.md`.
- Production strategy recommends always-on hosting before full production launch.
- Health checks are documented for `/` and `/api/health/db`.
- 22F retry confirmed hosted PostgreSQL connected, `missingTables = []`, and pgvector enabled.

Known gap: Full marketplace/security-review submission has not yet been completed.

Mitigation:

- Security-review preparation, final checklist, data privacy, callout security, install, support, monitoring, backup/recovery, and release evidence documents now exist.
- v1.0.0-rc.1 is tagged and production validation passed.
- Final submission can use this evidence pack as the main reference.

Known gap: Hosted DB deletion/export workflows are operational/manual.

Mitigation:

- Data privacy and retention documentation describes current manual deletion/export handling.
- Future production improvements include tenant-scoped deletion safeguards, customer-facing export/delete tooling, and configurable retention windows.

Known gap: Customers could include sensitive data in free-form incident error messages.

Mitigation:

- Data minimization guidance is documented.
- Standard payload is limited to operational incident context.
- Future improvements include PII detection or masking before hosted API submission.

Known gap: Hosted mode is deterministic `AI_MODE=RULE`, not hosted LLM reasoning.

Mitigation:

- This is an intentional safety posture for beta and release-candidate review.
- No public Ollama endpoint is exposed.
- AI cannot directly execute actions.
- Risk, policy, human approval, and replayable audit history remain enforced.

## 12. Submission Summary

SentinelFlow v1.0.0-rc.1 is ready for security-review submission preparation.

Release-candidate evidence shows:

- The Salesforce package validates with 17 passing tests and 0 failing tests.
- Hardened package deploy validates with 17 passing tests and 0 failing tests.
- Fresh org installation passed.
- Hosted API is live.
- Hosted PostgreSQL is connected with required tables present and pgvector enabled.
- End-to-end Salesforce incident processing passed.
- Human approval and approved execution passed.
- Case creation passed.
- Replay timeline passed with all eight expected events.
- Hosted API and Salesforce-side error logging were verified.
- Named Credential mode was implemented and validated.
- API shared-secret authentication was implemented and smoke tested.
- Known gaps are documented with mitigations.
