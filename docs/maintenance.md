# Zentom Maintenance Log

## Milestone 17C: Hosted PostgreSQL / Production DB Hardening

Status: Complete

Date: 2026-05-24

Hosted API:

```text
https://zentom-api.onrender.com
```

Verification summary:

- Hosted PostgreSQL connected through Render `DATABASE_URL`.
- `/api/health/db` passed.
- Database type verified as `postgresql`.
- Required tables verified:
  - `incidents`
  - `risk_scores`
  - `policy_decisions`
  - `ai_recommendations`
  - `memory_entries`
- `pgvector` verified as enabled.
- Hosted incident persistence passed.
- Direct Render incident test returned hosted DB incident id `4`.
- Salesforce anonymous Apex created `Sentinel_Incident__c` record `SI-000010`.
- Salesforce write-back used hosted DB incident id `5`.
- Salesforce audit logs verified:
  - `INCIDENT_RECEIVED`
  - `RISK_CALCULATED`
  - `ZENTOM_POLICY_EVALUATED`
  - `AI_RECOMMENDATION_GENERATED`
  - `RUNBOOK_SELECTED`

Production mode:

```text
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_MODEL=zentom-rule-v1
```

Hosted AI/Ollama remains disabled for the online beta. Vector/RAG memory remains available at the database layer, with model-hosting strategy deferred to Milestone 17D.

## Milestone 17D: Hosted AI / Local Model Strategy Decision

Status: Complete

Date: 2026-05-24

Decision summary:

- Hosted Render beta remains `AI_MODE=RULE`.
- Local advanced demo remains `AI_MODE=HYBRID` with Ollama `phi3:mini`, `all-minilm`, PostgreSQL, and pgvector.
- Ollama is not hosted online for beta.
- Ollama must never be exposed directly to the public internet.
- Production hosted AI provider decision is deferred until after beta workflow validation.

Decision document:

```text
docs/hosted-ai-strategy.md
```

## Milestone 18: Salesforce Package Hardening

Status: Complete

Date: 2026-05-24

Hosted API:

```text
https://zentom-api.onrender.com
```

Known beta limitation:

```text
Hosted API uses RULE mode. Hosted Ollama/LLM serving is intentionally disabled.
```

18A package manifest:

```text
apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml
```

18A/18B validation:

- Beta manifest created with stable SentinelFlow Apex, LWC, object, custom metadata, app, tab, page, layout, permission set, and remote site metadata.
- Excluded experimental Agentforce metadata, old static resources, tmp files, and unstable package drift.
- Validation org: `astrosoft`.
- Deploy validation ID: `0AfdL00000ayMNVSA2`.
- Stable tests passed: 14.
- Stable tests failed: 0.

18C permission set hardening:

- `SentinelFlow_Admin` narrowed to stable beta components with full access to SentinelFlow incidents, audit logs, policy decisions, app tabs, and runtime Apex.
- `SentinelFlow_Approver` added for approve, reject, replay, dashboard, and execute workflows.
- `SentinelFlow_Viewer` narrowed to read-only incident, audit, policy, replay, and dashboard access.
- Legacy broad `SentinelFlow_Operator` remains in source but is excluded from the beta manifest.
- Hardened permission validation org: `astrosoft`.
- Hardened permission deploy validation ID: `0AfdL00000ayY5JSAU`.
- Stable tests passed: 14.
- Stable tests failed: 0.

18D remote site / named credential cleanup:

- Beta callout model remains Remote Site Setting plus `Zentom_Setting__mdt.Default.Base_URL__c`.
- `Zentom_Setting__mdt.Default.Base_URL__c` verified as `https://zentom-api.onrender.com`.
- `Zentom_API.remoteSite-meta.xml` verified as `https://zentom-api.onrender.com`.
- Remote Site Setting contains only the base URL, not `/api/incidents/receive`.
- No Cloudflare/local URL remains in beta callout metadata.
- Named Credential, External Credential, and Permission Set Mapping migration plan documented in `docs/salesforce-callout-security.md`.
- Beta manifest validation ID: `0AfdL00000ayYlFSAU`.
- Stable tests passed: 14.
- Stable tests failed: 0.

18E case origin / picklist metadata cleanup:

- `CaseOrigin` included in `package-sentinelflow-beta.xml`.
- `Case.Origin` includes `SentinelFlow`.
- `ZentomExecutionController` already uses `SentinelFlow` and falls back to `Web` if unavailable.
- `ZentomExecutionControllerTest` now asserts created Cases use `Origin = SentinelFlow`.
- `Sentinel_Incident__c.Status__c` verified: `New`, `Analyzed`, `Approval Required`, `Approved`, `Action Created`, `Closed`.
- `Approval_Status__c` verified: `Pending Approval`, `Approved`, `Rejected`, `Not Required`.
- `Execution_Status__c` verified: `Not Started`, `Ready for Execution`, `Executed`, `Failed`, `Skipped`.
- `Recommendation_Status__c` verified: `Generated`, `Needs Review`, `Approved`, `Rejected`, `Executed`.
- `Risk_Level__c` verified: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
- `Environment__c` verified for beta payloads: `sandbox`, `production`.
- Page layout and list views verified against stable beta incident, audit, and policy fields.
- Beta manifest validation ID: `0AfdL00000aya8jSAA`.
- Stable tests passed: 14.
- Stable tests failed: 0.

18F fresh org / clean install validation:

- Scratch org alias: `sentinelflow-beta-18f`.
- Scratch org username: `test-0mttjga339cr@example.com`.
- Scratch org expires: 2026-05-25.
- Beta package manifest deployed cleanly to scratch org.
- Scratch deploy ID: `0AfBi000007rTsgKAE`.
- Stable tests passed: 14.
- Stable tests failed: 0.
- Permission sets assigned: `SentinelFlow_Admin`, `SentinelFlow_Approver`, `SentinelFlow_Viewer`.
- `Zentom_Setting__mdt.Default.Base_URL__c` verified as `https://zentom-api.onrender.com`.
- Direct scratch-org callout to hosted Render API returned HTTP 200.
- Hosted incident flow created scratch-org incident `SI-000000`.
- Scratch-org hosted DB incident id: `6`.
- Incident result verified: risk `95`, level `CRITICAL`, policy `HUMAN_APPROVAL_REQUIRED`, runbook `FLOW_FAILURE_BASIC_RECOVERY`.
- SentinelFlow app verified in scratch org.
- LWC bundles verified through Tooling API: `zentomApprovalPanel`, `zentomDashboard`, `zentomReplayTimeline`.
- Approval flow verified: incident moved to `Approved`.
- Execution flow verified: Case `00001028` created with `Origin = SentinelFlow` and priority `High`.
- Replay/audit timeline verified with eight events from incident intake through case creation.

18G package hardening wrap-up:

Beta package status:

```text
SentinelFlow Salesforce Beta Package: Hardened and fresh-org validated.
```

Milestone 18 package hardening summary:

- 18A: Clean beta package manifest complete.
- 18B: Stable test validation complete.
- 18C: Permission set hardening complete.
- 18D: Remote Site / Named Credential cleanup plan complete.
- 18E: Case Origin and picklist metadata cleanup complete.
- 18F: Fresh scratch org validation complete.
- 18G: Package hardening wrap-up complete.

18F validation result:

- Scratch org: `sentinelflow-beta-18f`.
- Deploy ID: `0AfBi000007rTsgKAE`.
- Stable tests: 14 passing, 0 failing.
- Permission sets: `SentinelFlow_Admin`, `SentinelFlow_Approver`, `SentinelFlow_Viewer`.
- Hosted API: `https://zentom-api.onrender.com`.

Verified package workflows:

- SentinelFlow app opens.
- Dashboard loads.
- Approval panel works.
- Replay timeline works.
- Hosted callout works.
- Case creation works.
- Case Origin equals `SentinelFlow`.

Next milestone:

```text
Milestone 19: AgentExchange / AppExchange Readiness
```

Planned 19 scope:

- 19A: Security Review Preparation.
- 19B: Data Privacy and Retention Documentation.
- 19C: Install Guide.
- 19D: Admin Setup Wizard.
- 19E: Publisher Listing Copy.

## Milestone 19: AgentExchange / AppExchange Readiness

Status: Complete

Date: 2026-05-24

Goal:

```text
Prepare SentinelFlow for marketplace and Salesforce security-review readiness.
```

19A security review preparation:

- Status: Started.
- Document created: `docs/security-review-preparation.md`.
- Hosted beta mode documented as `AI_MODE=RULE`.
- Public Ollama exposure explicitly prohibited.
- Stable Salesforce objects, Apex classes, LWC components, permission sets, external callouts, stored data, and known beta limitations documented.
- Remote Site Setting kept for beta.
- Named Credential, External Credential, and Permission Set Mapping documented as the future marketplace/security-review path.

19B data privacy and retention documentation:

- Status: Started and completed.
- Document created: `docs/data-privacy-retention.md`.
- Data sent from Salesforce to Zentom API documented.
- Data stored in Salesforce documented.
- Data stored in hosted PostgreSQL documented.
- Hosted beta mode documented as `AI_MODE=RULE`.
- No public Ollama and no paid third-party LLM usage documented for hosted beta.
- Human approval and policy-gated execution principle documented.
- Beta retention, deletion, export, access control, security controls, limitations, and future improvements documented.

19C install guide:

- Status: Started and completed.
- Document created: `docs/install-guide.md`.
- Hosted Zentom API documented as `https://zentom-api.onrender.com`.
- Beta package deployment and validation commands documented.
- Required permission sets documented: `SentinelFlow_Admin`, `SentinelFlow_Approver`, `SentinelFlow_Viewer`.
- `Zentom_Setting__mdt.Default.Base_URL__c` and `Zentom_API` Remote Site Setting documented.
- Anonymous Apex test incident documented.
- Expected incident, approval, execution, Case, and replay timeline results documented.
- Troubleshooting documented for Render cold start, Remote Site errors, permission issues, missing incident records, and Case Origin issues.

19D admin setup wizard plan:

- Status: Complete.
- Document created: `docs/admin-setup-wizard-plan.md`.
- Beta decision documented: planning document only.
- Future implementation documented for LWC `sentinelflowSetupWizard` and Apex `SentinelFlowSetupController`.
- Wizard flow documented for package confirmation, permission checks, Zentom API URL configuration, Remote Site / future Named Credential verification, API connection test, test incident submission, SentinelFlow app verification, and next steps.
- Hosted beta mode documented as `RULE` with `https://zentom-api.onrender.com`.
- Custom Metadata update caution documented for `Zentom_Setting__mdt.Default.Base_URL__c`.
- Security guardrails documented: no public Ollama exposure, no policy bypass, no autonomous production execution, and future Named Credential / External Credential migration before marketplace security review.

19E publisher listing copy:

- Status: Complete.
- Document created: `docs/publisher-listing-copy.md`.
- Recommended product names documented: `SentinelFlow by Tomcodex` and `SentinelFlow - Powered by Zentom AI`.
- Marketplace short description and long description drafted.
- Key features, business value, target users, use cases, setup summary, support placeholder, and beta limitations documented.
- Security and governance summary documented with hosted beta `AI_MODE=RULE`, no public Ollama exposure, no direct hosted LLM execution, policy-gated actions, human approval, and replay timeline auditability.

19F support and troubleshooting guide:

- Status: Complete.
- Document created: `docs/support-troubleshooting-guide.md`.
- Installation, API callout, permission, incident processing, approval, execution, dashboard, replay, Render hosting, and Salesforce debugging issues documented.
- Render cold start, Remote Site Setting, wrong Base URL, no incident created, approval panel visibility, dashboard loading, and Case creation troubleshooting documented.
- Escalation checklist documented with Salesforce Org Id, Sentinel Incident Id, Apex debug log, Render request timestamp, error message, user permission set, incident screenshot, and replay timeline events.
- Known beta limitations documented for hosted `AI_MODE=RULE`, no public Ollama exposure, Remote Site beta usage, future Named Credential migration, and Render free-tier cold starts.

19G marketplace readiness wrap-up:

- Status: Complete.
- Document created: `docs/marketplace-readiness-wrap-up.md`.
- Milestone 19 marked complete.
- Completed 19A through 19G marketplace readiness work documented.
- Readiness status documented: SentinelFlow is marketplace-preparation ready for private beta.
- Current beta package readiness documented with fresh-org validation, hosted Zentom API, hosted PostgreSQL + pgvector, security review preparation documentation, data privacy and retention documentation, install guide, setup wizard plan, publisher listing copy, and support troubleshooting guide.
- Known beta limitations documented: hosted `AI_MODE=RULE`, local HYBRID Ollama mode for advanced demos only, Named Credential migration planned, full autonomous remediation disabled, and Render free-tier cold starts.
- Next phase documented: Milestone 20 Private Beta Release.

## Milestone 20: Private Beta Release

Status: Complete

Planned scope:

- 20A: Beta Org Setup.
- 20B: Beta User Testing.
- 20C: Feedback Capture.
- 20D: Bug Fix Sprint.
- 20E: Beta Release Notes.

20A private beta planning:

- Status: Complete.
- Document created: `docs/private-beta-plan.md`.
- Beta goal documented: validate the hosted Salesforce-to-Zentom incident intelligence workflow with selected users before public marketplace submission.
- Beta scope, org details, beta users, test scenarios, success criteria, feedback questions, known limitations, bug triage process, and exit criteria documented.
- Hosted API documented as `https://zentom-api.onrender.com`.
- Current beta limitations documented: hosted `AI_MODE=RULE`, local HYBRID Ollama mode for advanced demos only, no full autonomous remediation, planned Named Credential migration, Remote Site beta usage, Render cold starts, and setup wizard not yet implemented.

20B beta testing scenarios:

- Status: Complete.
- Document created: `docs/beta-testing-scenarios.md`.
- Thirteen private beta scenarios documented with objective, user role, preconditions, steps, expected result, pass/fail, and notes fields.
- Scenarios cover install/setup verification, hosted Zentom API health, Flow failure incident intake, risk and policy verification, recommendation and runbook verification, approval, rejection, approved Case creation, replay timeline, dashboard and Org Health Score, permission sets, Render cold start retry, and support evidence capture.

20C feedback capture:

- Status: Complete.
- Document created: `docs/beta-feedback-capture.md`.
- Feedback purpose, participant roles, feedback channels, feedback form questions, bug report template, feature request template, severity levels, review cadence, beta success signals, and feedback-to-fix workflow documented.
- Severity levels documented from P0 through P4.
- Feedback questions documented for installation, app launch, hosted API connection, risk score, policy decision, recommendation, runbook, approval/rejection, Case creation, Replay Timeline, dashboard clarity, confusing areas, public-release improvements, and real-org trust.

20D bug fix sprint plan:

- Status: Complete.
- Document created: `docs/beta-bug-fix-sprint.md`.
- Sprint purpose, scope, bug intake sources, severity levels, triage rules, fix workflow, validation workflow, regression test checklist, release candidate criteria, and known beta risks documented.
- Bug intake sources documented: beta feedback form, Salesforce debug logs, SentinelFlow Replay Timeline, Render logs, hosted DB health endpoint, user screenshots, and support/troubleshooting guide.
- Triage rules documented from P0 through P4.
- Regression checklist documented for hosted API health, hosted DB health, Apex callout, incident write-back, risk/policy/recommendation, approval, rejection, Case creation, replay timeline, dashboard, Org Health Score, and permission set behavior.

20E beta release notes:

- Status: Complete.
- Document created: `docs/beta-release-notes.md`.
- Release name documented: `SentinelFlow Private Beta v0.5.0`.
- Product summary documented for hosted Salesforce-to-Zentom incident intelligence workflow.
- Included beta capabilities documented: SentinelFlow Lightning App, Dashboard, Sentinel Incident object, Audit Log object, Policy Decision object, hosted Zentom API integration, hosted PostgreSQL + pgvector backend, RULE-mode AI recommendation, Runbook Engine, human approval workflow, safe Case creation, Replay Timeline, Org Health Score, and Admin / Approver / Viewer permission sets.
- Known limitations documented: hosted `AI_MODE=RULE`, local HYBRID Ollama mode for advanced demos only, Render free-tier cold starts, planned Named Credential migration, no full autonomous remediation, and Agentforce integration planned later.
- Milestone 20 marked complete.

## Milestone 21: Production v1.0 Preparation

Status: Complete

Planned scope:

- 21A: Production Readiness Plan.
- 21B: Monitoring + Error Alerts.
- 21C: Backup + Recovery Plan.
- 21D: Named Credential Migration Plan.
- 21E: Security Review Final Checklist.
- 21F: v1.0 Documentation Freeze.

21A production readiness plan:

- Status: Complete.
- Document created: `docs/production-v1-readiness-plan.md`.
- Production goal documented: SentinelFlow Private Beta v0.5.0 is complete and Milestone 21 prepares the product for SentinelFlow v1.0 production readiness.
- Current beta status, production readiness checklist, hosted API stability requirements, Salesforce package stability requirements, database backup requirements, monitoring and alerting requirements, security review requirements, Named Credential migration requirement, and v1.0 exit criteria documented.
- Hosted API documented as `https://zentom-api.onrender.com`.
- Current hosted mode documented as `AI_MODE=RULE`.

21B monitoring and error alerts:

- Status: Complete.
- Document created: `docs/monitoring-error-alerts.md`.
- Monitoring scope documented for hosted Zentom API, hosted PostgreSQL, Salesforce callouts, incident processing, approval/execution flow, Render service health, dashboard, replay timeline, and Org Health Score.
- Health endpoints documented: `GET https://zentom-api.onrender.com/` and `GET https://zentom-api.onrender.com/api/health/db`.
- Expected health responses documented: API status `running`, DB status `ok`, `databaseType = postgresql`, `missingTables = []`, and pgvector enabled.
- Alert severity levels documented from P0 through P4.
- Manual monitoring checklist documented for hosted API health, `/docs`, `/api/health/db`, Salesforce test incident, Sentinel Incident creation, audit logs, approval panel, Case creation, and Replay Timeline.
- Future automated monitoring documented for UptimeRobot or Better Stack, Render logs, email/Slack alerts, Salesforce scheduled health check Apex, daily DB health check, and Salesforce error log object.

21C backup and recovery plan:

- Status: Complete.
- Document created: `docs/backup-recovery-plan.md`.
- Backup scope documented for hosted PostgreSQL, Zentom API configuration, Salesforce package metadata, Salesforce incident/audit data, documentation, GitHub source code, and release snapshots.
- Hosted PostgreSQL backup plan documented for `incidents`, `risk_scores`, `policy_decisions`, `ai_recommendations`, and `memory_entries`.
- Salesforce metadata and data backup expectations documented for SentinelFlow objects, audit logs, policy decisions, permission sets, custom metadata, and runbook metadata.
- Recovery scenarios documented for hosted API down, hosted database unavailable, accidental database data loss, Salesforce metadata deployment issue, wrong Zentom API URL, Render rollback, GitHub repo/branch issue, and documentation loss.
- Minimum production backup policy documented for GitHub source, hosted DB, Salesforce metadata, Salesforce customer data, documentation, and release tags.
- Recovery testing checklist documented for DB restore, scratch org deploy, hosted API health, DB health, test incident, Salesforce write-back, replay timeline, and dashboard validation.

21D Named Credential migration plan:

- Status: Complete.
- Document created: `docs/named-credential-migration-plan.md`.
- Current beta callout model documented: `ZentomIncidentClient` reads `Zentom_Setting__mdt.Default.Base_URL__c`, uses Remote Site Setting `Zentom_API`, and calls `https://zentom-api.onrender.com/api/incidents/receive`.
- Target production callout model documented: `ZentomIncidentClient` uses Named Credential endpoint `callout:Zentom_API/api/incidents/receive` with future auth through External Credential.
- Apex endpoint migration documented from `request.setEndpoint(baseUrl + '/api/incidents/receive')` to `request.setEndpoint('callout:Zentom_API/api/incidents/receive')`.
- Decision documented: do not change working beta callout code yet; document migration first.
- Required Salesforce metadata, Apex changes, permission set changes, deployment plan, rollback plan, testing checklist, and production readiness criteria documented.

21E security review final checklist:

- Status: Complete.
- Document created: `docs/security-review-final-checklist.md`.
- Package readiness, Apex security, LWC security, Salesforce Object/FLS/CRUD, external callout, data privacy, AI governance, hosted API security, database security, documentation, known gaps, and final go/no-go criteria documented.
- Key package checks documented: beta manifest validates, fresh scratch org deploy passed, stable tests pass, and no experimental metadata included.
- Key Apex checks documented: `with sharing` where appropriate, callout test coverage, no hardcoded secrets, no unsafe dynamic SOQL, and no direct autonomous execution without approval.
- AI governance checks documented: hosted `AI_MODE=RULE`, local Ollama not public, AI cannot directly execute high-risk actions, and risk/policy/approval/replay are enforced.
- Known gaps documented: Named Credential not implemented yet, Render free-tier cold start, and full security scan not yet submitted.

21F v1.0 documentation freeze:

- Status: Complete.
- Document created: `docs/v1-documentation-freeze.md`.
- Freeze version documented: `SentinelFlow Production Readiness Documentation Freeze v0.9`.
- Frozen documentation list documented, including maintenance, production readiness, monitoring, backup/recovery, Named Credential migration, security checklist, security review preparation, privacy/retention, install guide, support troubleshooting, private beta plan, and beta release notes.
- Current product status documented: SentinelFlow Private Beta v0.5.0 is complete and Milestone 21 prepares the product for production v1.0 readiness.
- Current hosted architecture documented: Render-hosted Zentom API, hosted PostgreSQL + pgvector, Salesforce beta package, RULE-mode recommendation, human approval, Case creation, replay timeline, dashboard, and Org Health Score.
- Current known gaps documented: Named Credential migration planned but not implemented, hosted beta uses `AI_MODE=RULE`, local HYBRID Ollama mode is not hosted, Render free-tier cold starts, and full marketplace/security review submission not complete.
- Change control rule documented: after freeze, all production-readiness changes must be recorded in `docs/maintenance.md` with date, milestone, affected files, validation evidence, and rollback note.
- Milestone 21 marked complete.

## Milestone 22: Production Implementation Sprint

Status: Started

Planned scope:

- 22A: Named Credential Implementation.
- 22B: API Authentication / Shared Secret Header.
- 22C: Render Cold Start / Uptime Strategy.
- 22D: Hosted API Error Logging.
- 22E: Salesforce Error Log Object.
- 22F: Production Validation Run.
- 22G: v1.0 Release Candidate Tag.

22A Named Credential implementation:

- Date: 2026-05-24.
- Status: Complete.
- Branch: `milestone-22a-named-credential`.
- Document created: `docs/named-credential-implementation-22a.md`.
- Goal documented: replace the Remote Site Setting callout model with a Named Credential based callout while preserving Remote Site fallback until validation is complete.
- Safe rollout documented: add Named Credential metadata, add Custom Metadata feature flag, update Apex to support both modes, validate Named Credential callout, and keep Remote Site fallback until stable.
- Affected files planned: `ZentomIncidentClient.cls`, `ZentomIncidentClientTest.cls`, `Zentom_Setting__mdt` metadata fields, `Zentom_Setting.Default` custom metadata, `Zentom_API` Named Credential metadata, beta/package manifest, and production readiness docs.
- Validation evidence required before completion: stable Apex tests, scratch/beta org deploy validation, Named Credential endpoint evidence, test incident creation, Salesforce write-back, replay timeline, and rollback verification.
- Rollback note: set callout mode back to `REMOTE_SITE`, confirm `Base_URL__c = https://zentom-api.onrender.com`, confirm Remote Site Setting `Zentom_API` is active, and re-run the test incident.

22A-1 Callout mode feature flag:

- Date: 2026-05-24.
- Status: Complete.
- Affected files: `apps/sentinelflow-salesforce/force-app/main/default/objects/Zentom_Setting__mdt/fields/Callout_Mode__c.field-meta.xml`, `apps/sentinelflow-salesforce/force-app/main/default/customMetadata/Zentom_Setting.Default.md-meta.xml`, and `docs/maintenance.md`.
- Change: added `Callout_Mode__c` picklist to `Zentom_Setting__mdt` with values `REMOTE_SITE` and `NAMED_CREDENTIAL`.
- Default beta setting: `Zentom_Setting.Default.Callout_Mode__c = REMOTE_SITE`.
- Validation evidence: XML metadata added and scoped diff reviewed before commit.
- Rollback note: remove `Callout_Mode__c` field metadata and the `Callout_Mode__c` value from `Zentom_Setting.Default`; existing `Base_URL__c` and Remote Site Setting `Zentom_API` remain unchanged.

22A-2 Named Credential metadata:

- Date: 2026-05-24.
- Status: Complete.
- Affected files: `apps/sentinelflow-salesforce/force-app/main/default/namedCredentials/Zentom_API.namedCredential-meta.xml`, `apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml`, and `docs/maintenance.md`.
- Change: added Named Credential metadata `Zentom_API` pointing to `https://zentom-api.onrender.com` with `NoAuthentication` and anonymous principal.
- Beta manifest updated to include `NamedCredential:Zentom_API`.
- Existing `RemoteSiteSetting:Zentom_API` remains in the beta manifest as fallback.
- Validation evidence: Named Credential XML added using existing repo metadata pattern and parsed successfully before commit.
- Rollback note: remove `Zentom_API.namedCredential-meta.xml` and the `NamedCredential:Zentom_API` manifest entry; Remote Site fallback remains unchanged.

22A-3 Dual callout mode Apex support:

- Date: 2026-05-24.
- Status: Complete.
- Affected files: `apps/sentinelflow-salesforce/force-app/main/default/classes/ZentomIncidentClient.cls`, `apps/sentinelflow-salesforce/force-app/main/default/classes/ZentomIncidentClientTest.cls`, and `docs/maintenance.md`.
- Change: `ZentomIncidentClient` now reads `Zentom_Setting__mdt.Callout_Mode__c` and supports both `REMOTE_SITE` and `NAMED_CREDENTIAL` endpoint modes.
- Default/fallback behavior: blank callout mode defaults to `REMOTE_SITE`, preserving the current beta path through `Base_URL__c` and Remote Site Setting `Zentom_API`.
- Named Credential behavior: `NAMED_CREDENTIAL` uses endpoint `callout:Zentom_API/api/incidents/receive`.
- Test coverage added for both Remote Site endpoint construction and Named Credential endpoint construction.
- Validation evidence: scoped diff reviewed; Salesforce validation succeeded against target org `astrosoft` with deploy ID `0AfdL00000az6erSAA`, 15 tests passing, 0 failing.
- Rollback note: revert `ZentomIncidentClient.cls` and `ZentomIncidentClientTest.cls` to the previous Base URL only implementation, or set `Callout_Mode__c = REMOTE_SITE` to keep using the existing fallback path.

22A-4 Remote Site mode validation:

- Date: 2026-05-24.
- Status: Complete.
- Target org: `astrosoft`.
- Deployment evidence: beta manifest deployed successfully with deploy ID `0AfdL00000az7FxSAI`, 15 tests passing, 0 failing.
- Hosted API health evidence: `GET https://zentom-api.onrender.com/` returned `status = running`.
- Hosted DB health evidence: `GET https://zentom-api.onrender.com/api/health/db` returned `status = ok`, `databaseType = postgresql`, `missingTables = []`, and pgvector enabled.
- Execution evidence: anonymous Apex `ZentomIncidentClient.sendIncident(...)` completed successfully with `Callout_Mode__c = REMOTE_SITE`.
- Result evidence: new Sentinel Incident `SI-000011` created with `Risk_Score__c = 95`, `Risk_Level__c = CRITICAL`, `Policy_Decision__c = HUMAN_APPROVAL_REQUIRED`, `Runbook_Key__c = FLOW_FAILURE_BASIC_RECOVERY`, `Approval_Status__c = Pending Approval`, `Status__c = Approval Required`, and hosted `Zentom_Incident_Id__c = 7`.
- Rollback note: no rollback required; Remote Site remains the default repo setting and fallback path.

22A-5 Named Credential mode validation:

- Date: 2026-05-24.
- Status: Complete.
- Target org: `astrosoft`.
- Metadata switch evidence: `Zentom_Setting.Default.Callout_Mode__c` temporarily deployed as `NAMED_CREDENTIAL` with deploy ID `0AfdL00000az7XhSAI`.
- Verification evidence: SOQL confirmed `Callout_Mode__c = NAMED_CREDENTIAL`, `Base_URL__c = https://zentom-api.onrender.com`, and `Is_Active__c = true`.
- Execution evidence: anonymous Apex `ZentomIncidentClient.sendIncident(...)` completed successfully through `callout:Zentom_API/api/incidents/receive`.
- Result evidence: new Sentinel Incident `SI-000012` created with `Risk_Score__c = 95`, `Risk_Level__c = CRITICAL`, `Policy_Decision__c = HUMAN_APPROVAL_REQUIRED`, `Runbook_Key__c = FLOW_FAILURE_BASIC_RECOVERY`, `Approval_Status__c = Pending Approval`, `Status__c = Approval Required`, and hosted `Zentom_Incident_Id__c = 8`.
- Repo default restored: local `Zentom_Setting.Default.Callout_Mode__c` remains `REMOTE_SITE` for safe beta fallback.
- Rollback note: set `Callout_Mode__c = REMOTE_SITE`; no code rollback is required because dual mode support is already implemented.

22A-6 Named Credential implementation wrap-up:

- Date: 2026-05-24.
- Status: Complete.
- Branch: `milestone-22a-named-credential`.
- Summary: SentinelFlow now supports both Remote Site and Named Credential callout modes through `Zentom_Setting__mdt.Callout_Mode__c`.
- REMOTE_SITE validation passed with Sentinel Incident `SI-000011`.
- NAMED_CREDENTIAL validation passed with Sentinel Incident `SI-000012`.
- Salesforce validation passed with deploy ID `0AfdL00000az7FxSAI`, 15 tests passing, 0 failing.
- Repo default restored and kept as `REMOTE_SITE` until the v1 production switch.
- Remote Site Setting `Zentom_API` and `Base_URL__c` remain available as fallback.
- Rollback note: switch `Zentom_Setting.Default.Callout_Mode__c` back to `REMOTE_SITE`; no code rollback required.

22B API authentication / shared secret header:

- Date: 2026-05-24.
- Status: Complete.
- Goal: Salesforce sends `X-Zentom-Api-Key`, Zentom API validates it, unauthorized callers are rejected, and no secret is committed to Git.
- API change: `POST /api/incidents/receive` validates `X-Zentom-Api-Key` when `ZENTOM_API_KEY` is configured in the hosted environment.
- Salesforce change: `ZentomIncidentClient` sends `X-Zentom-Api-Key` when `Zentom_Setting__mdt.Api_Key__c` is populated.
- Secret handling: `ZENTOM_API_KEY` and `Api_Key__c` values remain blank in Git and must be configured in Render/Salesforce environment-specific setup.
- Backward compatibility: if `ZENTOM_API_KEY` is not configured, the API keeps current beta behavior for safe rollout.
- Validation evidence: Salesforce validation succeeded against target org `astrosoft` with deploy ID `0AfdL00000az8lVSAQ`, 15 tests passing, 0 failing.
- API validation evidence: direct auth helper smoke test passed in `services/zentom-api/venv`; correct key accepted, missing/wrong key rejected with HTTP 401.
- Rollback note: clear `ZENTOM_API_KEY` in the hosted environment and clear `Zentom_Setting__mdt.Api_Key__c`; incident callouts continue without shared-secret enforcement.

22C Render cold start / uptime strategy:

- Date: 2026-05-24.
- Status: Complete.
- Document created: `docs/render-uptime-strategy.md`.
- Cold start risk documented: first Salesforce Apex call may timeout if Render free-tier service is sleeping.
- Beta mitigation documented: wake `https://zentom-api.onrender.com/`, verify `/api/health/db`, retry after 30-60 seconds, and record cold-start behavior separately from product failures.
- Production strategy documented: use paid always-on hosting or another always-on cloud runtime before v1.0 production.
- Options documented: keep Render free for beta only, upgrade Render to always-on paid plan, move to AWS/Azure/GCP, or add uptime monitor/keep-alive ping.
- Monitoring plan documented for API health, DB health, Salesforce callout failures, incident creation gaps, Render logs, and future uptime tooling.
- Go/no-go criteria documented: free-tier sleeping infrastructure is acceptable for beta only, not production.

22D hosted API error logging:

- Date: 2026-05-24.
- Status: Complete.
- Goal: record hosted API incident/auth failures server-side without exposing secrets.
- API change: added `api_error_logs` table for path, method, status code, error type, sanitized error message, org id, incident type, source, client host, and timestamp.
- Endpoint change: `POST /api/incidents/receive` logs unauthorized shared-secret failures and unexpected processing exceptions.
- Health check added: `GET /api/health/errors` returns error log table status and count.
- DB health updated: `/api/health/db` now includes `api_error_logs` in the required table list.
- Secret handling: `X-Zentom-Api-Key` values are never stored in the error log.
- Validation evidence: hosted API error logging smoke test passed in `services/zentom-api/venv` with in-memory SQLite; missing API key returned HTTP 401 and inserted one `api_error_logs` row.
- Rollback note: remove `ApiErrorLog`, `log_api_error`, the `/api/health/errors` endpoint, and the incident endpoint logging wrapper; incident processing can continue without error persistence.

22E Salesforce error log object:

- Date: 2026-05-24.
- Status: Complete.
- Goal: persist Salesforce-side callout failures so beta admins can diagnose failed Zentom API requests without relying only on debug logs.
- Metadata added: `Sentinel_Error_Log__c` with source class, error type, error message, status code, endpoint, org id, incident type, request payload, response payload, and system-created marker fields.
- Apex change: `ZentomIncidentClient` now logs non-2xx Zentom API responses and callout/configuration exceptions to `Sentinel_Error_Log__c`.
- Secret handling: API headers and `X-Zentom-Api-Key` are not stored in Salesforce error logs.
- Permission update: `SentinelFlow_Admin` has full error log access; `SentinelFlow_Approver` and `SentinelFlow_Viewer` have read-only access.
- Test coverage added for failed HTTP response logging and configuration exception logging.
- Validation evidence: beta manifest validation succeeded against target org `astrosoft` with deploy ID `0AfdL00000azA8zSAE`, 17 tests passing, 0 failing.
- Rollback note: remove `Sentinel_Error_Log__c` metadata and revert `ZentomIncidentClient` failure logging helper; successful incident processing is unaffected.

22F production validation run:

- Date: 2026-05-24.
- Status: Complete.
- Goal: run an end-to-end production-readiness validation using the hardened Salesforce package and hosted Zentom API.
- Package validation evidence: beta manifest validation succeeded against target org `astrosoft` with deploy ID `0AfdL00000az6W5SAI`, 17 tests passing, 0 failing.
- Hardened package deploy evidence: beta manifest deploy succeeded against target org `astrosoft` with deploy ID `0AfdL00000azAXBSA2`, 17 tests passing, 0 failing.
- Hosted API evidence: `GET https://zentom-api.onrender.com/` returned `status = running`, `service = zentom-api`, and `message = Zentom API is ready`.
- Hosted DB evidence: first `/api/health/db` request returned a transient HTTP 500, retry passed with `status = ok`, `databaseType = postgresql`, `databaseConfigured = true`, `missingTables = []`, and pgvector `enabled = true`.
- Incident write-back evidence: anonymous Apex `ZentomIncidentClient.sendIncident(...)` created Sentinel Incident `SI-000013` (`a0VdL00000R11lhUAB`) with hosted `Zentom_Incident_Id__c = 9`.
- Incident result evidence: `SI-000013` had `Risk_Score__c = 95`, `Risk_Level__c = CRITICAL`, `Policy_Decision__c = HUMAN_APPROVAL_REQUIRED`, `Runbook_Key__c = FLOW_FAILURE_BASIC_RECOVERY`, `Status__c = Approval Required`, and `Approval_Status__c = Pending Approval`.
- Approval/execution evidence: `ZentomApprovalController.approveIncident(...)` and `ZentomExecutionController.executeApprovedAction(...)` completed successfully for `SI-000013`.
- Execution result evidence: `SI-000013` moved to `Status__c = Action Created`, `Approval_Status__c = Approved`, `Recommendation_Status__c = Approved`, `Execution_Status__c = Executed`, and `Execution_Action__c = CREATE_CASE`.
- Case creation evidence: Case `00001051` (`500dL00003F2muRQAR`) was created with `Origin = SentinelFlow`, `Priority = High`, and subject `[SentinelFlow] FLOW_FAILURE - CRITICAL`.
- Replay timeline evidence: audit events were present in order: `INCIDENT_RECEIVED`, `RISK_CALCULATED`, `ZENTOM_POLICY_EVALUATED`, `AI_RECOMMENDATION_GENERATED`, `RUNBOOK_SELECTED`, `HUMAN_APPROVED`, `RUNBOOK_ACTION_EXECUTED`, and `CASE_CREATED`.
- Error logging evidence: temporary same-host bad path `https://zentom-api.onrender.com/invalid-22f` produced `Sentinel_Error_Log__c` record `SEL-000000` (`a0XdL00000VW1C1UAL`) with `Error_Type__c = ZENTOM_API_NON_SUCCESS`, `Status_Code__c = 404`, and endpoint `https://zentom-api.onrender.com/invalid-22f/api/incidents/receive`.
- Restore evidence: `Zentom_Setting.Default.Base_URL__c` restored to `https://zentom-api.onrender.com`, `Callout_Mode__c = REMOTE_SITE`, and `Is_Active__c = true` with deploy ID `0AfdL00000azAiTSAU`.
- Rollback note: no rollback required. If any issue appears after this validation, set `Zentom_Setting.Default.Base_URL__c` to `https://zentom-api.onrender.com`, keep `Callout_Mode__c = REMOTE_SITE`, and redeploy the last known good beta manifest.

## Milestone 23: Security Review Submission Preparation

Status: Complete

Planned scope:

- 23A: Final Security Review Evidence Pack.
- 23B: CRUD/FLS + Sharing Review.
- 23C: Apex/LWC Security Scan Checklist.
- 23D: External Callout + Named Credential Final Decision.

23A final security review evidence pack:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/security-review-evidence-pack.md`.
- Release candidate evidence documented for tag `v1.0.0-rc.1`, target commit `92e344c6fc865ab339d20ee37fec888bafaae1bc`, package validation, fresh-org validation, production validation, security-review preparation docs, data privacy docs, callout security docs, Named Credential validation, API authentication evidence, known gaps, and mitigations.
- Rollback note: documentation-only milestone; no runtime rollback required.

23B CRUD/FLS + sharing review:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/crud-fls-sharing-review.md`.
- Key objects reviewed: `Sentinel_Incident__c`, `Sentinel_Audit_Log__c`, `Zentom_Policy_Decision__c`, `Sentinel_Error_Log__c`, and `Case`.
- Key permission sets reviewed: `SentinelFlow_Admin`, `SentinelFlow_Approver`, and `SentinelFlow_Viewer`.
- Important gap captured: stable Apex uses `with sharing`, but explicit CRUD/FLS enforcement still needs to be added or verified in the next implementation/security track.
- Rollback note: documentation-only milestone; no runtime rollback required.

23C Apex/LWC security scan checklist:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/apex-lwc-security-scan-checklist.md`.
- Scope documented for stable Apex classes, stable LWCs, SOQL/DML review, Salesforce callouts, error handling, secrets handling, static analysis tools, findings log template, remediation workflow, and final security scan checklist.
- Key Apex checks documented: `with sharing`, no hardcoded secrets, no unsafe dynamic SOQL, no unrestricted DML, CRUD/FLS enforcement review, approved endpoint strategy, and safe error logging.
- Key LWC checks documented: no secrets in JavaScript, permission/record-state aware buttons, no unsafe DOM manipulation, no direct external client calls, and safe user-visible errors.
- Static analysis tools documented: Salesforce Code Analyzer, PMD rules, ESLint for LWC, and manual CRUD/FLS review.
- Next phase documented: 23D External Callout + Named Credential Final Decision.
- Rollback note: documentation-only milestone; remove `docs/apex-lwc-security-scan-checklist.md` and this maintenance entry if the checklist needs to be replaced.

23D external callout + Named Credential final decision:

- Date: 2026-05-25.
- Status: Complete.
- Final decision: keep the validated Remote Site path as the safe fallback while treating the validated `Zentom_API` Named Credential path as the production/security-review target.
- Current repo default remains `Callout_Mode__c = REMOTE_SITE` for safe fallback after production validation.
- Named Credential evidence remains captured in 22A and `docs/security-review-evidence-pack.md`.
- External Credential and Permission Set Mapping remain documented as the future marketplace-ready authentication model.
- Rollback note: no runtime rollback required; this was a decision/documentation milestone.

Milestone 23 wrap-up:

- Status: Complete.
- Completed scope: 23A final security review evidence pack, 23B CRUD/FLS + sharing review, 23C Apex/LWC security scan checklist, and 23D external callout + Named Credential final decision.
- Important carried-forward gap: stable Apex uses `with sharing`, but explicit CRUD/FLS enforcement still needs to be added or verified in the next implementation/security track.

## Milestone 24: Merged

Status: Merged

Milestone 24 was merged into Milestone 23/25 documentation and release preparation work.

Reconciliation note:

- No standalone Milestone 24 execution track remains active.
- Security-review evidence, release preparation, callout decisioning, and roadmap cleanup were handled through Milestone 23 and Milestone 25 workstreams.
- Future references should treat Milestone 24 as intentionally merged, not skipped by accident.

## Milestone 25: v1 Release Preparation Closure

Status: Complete

Reconciliation note:

- Milestone 25 is complete.
- Milestone 25 closed the v1 release preparation path after the v1.0.0-rc.1 tag, production validation evidence, security-review documentation, and release-readiness cleanup.
- Current release candidate remains `v1.0.0-rc.1`.
- Current active milestone after 25Z is Milestone 26.

## Milestone 25Z: Roadmap Reconciliation

Status: Complete

Goal:

- Update roadmap and maintenance documentation so official project status clearly reflects completed release-preparation milestones and the next active rollout phase.

Changes:

- Milestone 23 marked complete.
- Milestone 25 marked complete.
- Milestone 24 documented as merged into Milestone 23/25 documentation and release preparation work.
- Current active milestone documented as Milestone 26.
- Milestone 26 post-v1 stabilization and customer rollout scope documented.

Rollback note: documentation-only milestone; restore the prior roadmap/maintenance wording if the milestone numbering plan changes.

## Milestone 26: Post-v1 Stabilization and Customer Rollout

Status: Complete

Planned scope:

- 26A: Production Issue Tracking.
- 26B: Customer Onboarding Checklist.
- 26C: Support SLA / Response Policy.
- 26D: Usage Monitoring + Adoption Metrics.
- 26E: Feedback-to-Roadmap Process.
- 26F: v1.0.1 Patch Planning.

Current active milestone:

```text
Milestone 26 - Post-v1 Stabilization and Customer Rollout
```

26A production issue tracking:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/production-issue-tracking.md`.
- Goal documented: make every production issue traceable from intake through triage, ownership, validation, customer communication, release mapping, and weekly review.
- Issue sources documented: customer support, Salesforce admins/users, Salesforce debug logs, `Sentinel_Error_Log__c`, hosted API logs, hosted API error logs, Render logs, hosted DB health checks, production validation, uptime/health monitors, dashboard/replay discrepancies, GitHub issues, internal QA, and release-candidate regression testing.
- Severity levels documented: P0, P1, P2, and P3 with escalation rules for security, data privacy, secret handling, approval bypass, and customer-facing outages.
- Workflow documented from New through Closed, Accepted Risk, Duplicate, and Won't Fix.
- Required evidence documented for Salesforce records, hosted API/DB health, callout mode, error logs, replay events, and secret-safe collection rules.
- Fix validation, release/patch mapping, customer communication, and weekly review process documented.
- Next phase documented: 26B Customer Onboarding Checklist.
- Rollback note: documentation-only milestone; remove `docs/production-issue-tracking.md` and this maintenance entry if the tracking process is replaced.

26B customer onboarding checklist:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/customer-onboarding-checklist.md`.
- Goal documented: provide a repeatable customer go-live path covering Salesforce access, package installation, permissions, Zentom API configuration, test incident processing, approval, execution, replay, dashboard, Org Health Score, and support handoff.
- Target customer profile and pre-onboarding requirements documented, including Salesforce admin access, org type, Org Id, customer contacts, hosted API target, and release candidate.
- Salesforce org readiness, package installation, permission assignment, Zentom API configuration, test incident, approval/execution, replay/dashboard, support handoff, and go-live criteria documented.
- Required validation expectations documented: `FLOW_FAILURE` test incident, risk `95`, level `CRITICAL`, policy `HUMAN_APPROVAL_REQUIRED`, runbook `FLOW_FAILURE_BASIC_RECOVERY`, approved Case creation, Replay Timeline, Dashboard, and Org Health Score.
- Customer feedback capture documented for installation clarity, permission roles, test incident result, approval/execution workflow, replay timeline, dashboard, go-live blockers, and rollout improvements.
- Next phase documented: 26C Support SLA / Response Policy.
- Rollback note: documentation-only milestone; remove `docs/customer-onboarding-checklist.md` and this maintenance entry if the onboarding checklist is replaced.

26C support SLA / response policy:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/support-sla-response-policy.md`.
- Goal documented: set expectations for support scope, channels, severity classification, response targets, resolution/workaround targets, escalation, customer responsibilities, Tomcodex/Zentom responsibilities, out-of-scope support, beta/early customer notes, and review cadence.
- Severity levels documented from P0 through P4 with initial response targets and resolution/workaround targets.
- Response targets documented: P0 within 4 business hours, P1 within 1 business day, P2 within 2 business days, P3 within 3 business days, and P4 best effort.
- Resolution/workaround targets documented: P0 within 1 business day, P1 within 2 business days, P2 within 5 business days, P3 in the next planned patch, and P4 through roadmap review.
- Render cold-start caveat documented: hosted beta uses Render, cold-start delay may occur, and critical production customers should use always-on hosting before strict SLA.
- Escalation, customer responsibility, Tomcodex/Zentom responsibility, out-of-scope support, and review cadence documented.
- Next phase documented: 26D Usage Monitoring + Adoption Metrics.
- Rollback note: documentation-only milestone; remove `docs/support-sla-response-policy.md` and this maintenance entry if the SLA policy is replaced.

26D usage monitoring + adoption metrics:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/usage-monitoring-adoption-metrics.md`.
- Goal documented: track whether customers can install, configure, validate, use, trust, and repeatedly operate SentinelFlow after onboarding.
- Monitoring scope documented for Salesforce package usage, Sentinel Incident volume/status, approval/execution workflow, Case creation, Replay Timeline, Dashboard, Org Health Score, hosted API health, hosted DB health, API intake outcomes, error logs, Render cold-start incidents, onboarding, and feedback activity.
- Product usage metrics documented: Sentinel Incidents created, critical incidents, pending approvals, approved incidents, rejected incidents, executed actions, Cases created, and future Replay Timeline usage.
- Hosted API metrics documented: API health, `/api/health/db`, intake success/failure count, 401 unauthorized count, 5xx error count, and future average response time.
- Customer adoption and operational health metrics documented, including active admins/approvers, beta scenarios completed, feedback submitted, customers completing onboarding, Org Health Score, open critical incidents, error log count, and Render cold-start incidents.
- Weekly review dashboard, success signals, risk signals, and future automation plan documented.
- Next phase documented: 26E Feedback-to-Roadmap Process.
- Rollback note: documentation-only milestone; remove `docs/usage-monitoring-adoption-metrics.md` and this maintenance entry if the metrics plan is replaced.

26E feedback-to-roadmap process:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/feedback-to-roadmap-process.md`.
- Goal documented: convert customer feedback, support signals, onboarding observations, production issues, usage metrics, and product ideas into clear decisions for immediate fixes, next patch, workaround, accepted risk, future roadmap, duplicate, or not planned.
- Feedback sources documented: beta feedback form, support tickets, customer onboarding notes, production issue tracking, SentinelFlow Replay Timeline findings, Salesforce error logs, usage/adoption metrics, and direct customer calls.
- Feedback classifications documented: bug, usability issue, documentation gap, feature request, security concern, performance issue, integration request, and AI recommendation quality issue.
- Priority levels documented from P0 through P4, including production safety blockers, core workflow/trust issues, onboarding/adoption improvements, future enhancements, and backlog ideas.
- Roadmap decision rules documented for must-fix, next-patch, and future-roadmap items, including advanced AI/HYBRID hosted model, Agentforce integration, setup wizard implementation, and Named Credential default switch.
- Review cadence, customer communication rules, backlog management, release planning, and success metrics documented.
- Next phase documented: 26F v1.0.1 Patch Planning.
- Rollback note: documentation-only milestone; remove `docs/feedback-to-roadmap-process.md` and this maintenance entry if the roadmap process is replaced.

26F v1.0.1 patch planning:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/v1.0.1-patch-planning.md`.
- Core decision documented: v1.0.1 should focus on bug fixes, onboarding improvements, documentation corrections, and low-risk stability changes.
- Patch scope documented for bug fixes, onboarding improvements, documentation corrections, low-risk Salesforce package stability changes, low-risk hosted API stability changes, monitoring/logging improvements, approval/execution/replay/audit regressions, and security or privacy fixes.
- Patch candidate sources documented: production issue tracking, customer onboarding findings, support SLA escalations, usage/adoption metrics, feedback-to-roadmap review, Salesforce debug logs, `Sentinel_Error_Log__c`, hosted API logs, hosted API error logs, hosted DB health checks, Render observations, security review findings, install validation, regression testing, and customer-reported documentation gaps.
- Must-fix criteria documented: P0/P1 customer blockers, hosted API failures, Salesforce package install blockers, callout/authentication failures, approval/execution defects, replay/audit defects, and data privacy or security issues.
- Candidate improvements documented for install/onboarding documentation, hosted API and DB validation clarity, callout/authentication troubleshooting, admin-facing error messages, low-risk audit/replay/logging corrections, package metadata corrections, support workflow improvements, and release documentation corrections.
- Excluded changes documented: major AI architecture change, hosted HYBRID Ollama, Agentforce production integration, full autonomous remediation, and large object model changes.
- Validation requirements documented for hosted API health, hosted DB health, Salesforce package validation, clean install checks, test incident submission, write-back, risk/policy/recommendation/runbook output, approval/rejection, execution, replay timeline, dashboard, Org Health Score, error logging, security/privacy evidence, and documentation consistency.
- Release notes requirements documented for version/date, fixed blockers, hosted API fixes, package/install fixes, callout/authentication fixes, approval/execution fixes, replay/audit fixes, security/privacy fixes, onboarding/documentation improvements, known limitations, upgrade instructions, validation summary, rollback guidance, and support escalation.
- Rollback plan documented for documentation-only issues, Salesforce metadata issues, hosted API issues, authentication issues, approval/execution issues, and replay/audit issues.
- Patch exit criteria documented with owner assignment, P0/P1 disposition, low-risk scope, validation requirements, rollback notes, release notes ownership, customer communication needs, package validation plan, hosted API validation plan, and maintenance log update.
- Milestone 26 marked complete.
- Next phase documented: Milestone 27 Real Customer Pilot.
- Rollback note: documentation-only milestone; remove `docs/v1.0.1-patch-planning.md` and this maintenance entry if the patch planning process is replaced.

Milestone 26 wrap-up:

- Status: Complete.
- Completed scope: 26A production issue tracking, 26B customer onboarding checklist, 26C support SLA / response policy, 26D usage monitoring + adoption metrics, 26E feedback-to-roadmap process, and 26F v1.0.1 patch planning.
- Milestone 26 result: post-v1 stabilization and customer rollout planning is complete.
- Next milestone: Milestone 27 Real Customer Pilot.

## Milestone 27: Real Customer Pilot

Status: Active

Planned scope:

- 27A: Pilot Customer Selection Criteria.

Current active milestone:

```text
Milestone 27 - Real Customer Pilot
```

27A pilot customer selection criteria:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/real-customer-pilot-plan.md`.
- Core goal documented: validate SentinelFlow in a real Salesforce customer environment with a controlled, low-risk pilot before wider marketplace rollout.
- Pilot goal documented for end-to-end Salesforce-to-Zentom validation, customer admin onboarding, approver trust, hosted API/database stability, blocker discovery, and feedback capture for v1.0.1 and future roadmap decisions.
- Ideal pilot customer profile documented, including Salesforce admin access, sandbox/developer org preference, Case validation readiness, operational incident workflow fit, guided onboarding participation, and evidence-sharing expectations.
- Customer selection criteria documented with required, preferred, and exclusion criteria.
- Pilot scope documented for package installation, permissions, hosted API configuration, callout validation, standard test incident, write-back, risk/policy/recommendation/runbook validation, approval/rejection, Case creation, replay timeline, dashboard, support escalation, and feedback capture.
- Excluded pilot scope documented for major AI architecture changes, hosted HYBRID Ollama, Agentforce production integration, full autonomous remediation, large object model changes, broad marketplace rollout, custom integrations, and production rollout without explicit customer approval.
- Pilot timeline documented from customer selection through pre-onboarding, guided onboarding, workflow validation, observation, and pilot review.
- Success criteria documented for onboarding, package validation, permissions, hosted API/DB health, test incident, write-back, approval, execution, replay, dashboard, secret-safe evidence, feedback triage, and P0/P1 closure.
- Support process documented with support owner, escalation contacts, SLA handling, issue tracking, feedback-to-roadmap routing, v1.0.1 patch routing, and required support evidence.
- Feedback process documented with sources, categories, review rules, and feedback record template.
- Pilot exit criteria documented with close, no-go, patch-candidate, roadmap, and rollout decision requirements.
- Next phase documented: 27B Pilot Onboarding Runbook.
- Rollback note: documentation-only milestone; remove `docs/real-customer-pilot-plan.md` and this maintenance entry if the pilot selection process is replaced.
