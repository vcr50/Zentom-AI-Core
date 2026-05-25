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
- 27B: Pilot Outreach Pack.
- 27C: Pilot Demo Script.
- 27D: Pilot Feedback Review Template.
- 27E: Pilot Success Report.

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
- Next phase documented: 27B Pilot Outreach Pack.
- Rollback note: documentation-only milestone; remove `docs/real-customer-pilot-plan.md` and this maintenance entry if the pilot selection process is replaced.

27B pilot outreach pack:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/pilot-outreach-pack.md`.
- Short product intro documented for SentinelFlow as a Salesforce incident intelligence and approval workflow pilot with hosted Zentom API, risk scoring, policy decisions, runbook recommendations, human approval, safe Salesforce actions, and Replay Timeline auditability.
- Target pilot audience documented for Salesforce admins, operations leads, support/service leaders, automation owners, governance stakeholders, and technical evaluators.
- Customer test scope documented for package validation, permission assignment, hosted API configuration, hosted health checks, `FLOW_FAILURE` test incident, write-back, risk/policy/recommendation/runbook output, approval/rejection, Case creation, Replay Timeline, dashboard, support escalation, and feedback.
- Time required documented for intro/demo, pre-onboarding, guided setup, workflow testing, observation, and pilot review.
- Pilot customer benefits documented, including early access, guided setup, real-org validation, human-approved workflow, replay evidence, v1.0.1 influence, clear support path, and low-risk validation.
- Pilot limitations documented, including controlled scope, human approval requirement, no full autonomous remediation, no Agentforce production integration, no hosted HYBRID Ollama, no major AI architecture changes, no large object model changes, and no unapproved custom integrations.
- Support process documented with support owner, customer contacts, org evidence, SLA handling, production issue tracking, feedback-to-roadmap routing, and v1.0.1 patch routing.
- Call/demo agenda documented from introductions through demo flow, pilot fit, roles/access, timeline, support, feedback, and next steps.
- Follow-up questions documented for pilot fit, pilot readiness, and post-validation feedback.
- Next phase documented: customer-facing pilot outreach message.
- Rollback note: documentation-only milestone; remove `docs/pilot-outreach-pack.md` and this maintenance entry if the outreach pack is replaced.

Customer-facing pilot outreach message:

- Date: 2026-05-25.
- Status: Drafted.
- Document created: `docs/customer-facing-pilot-outreach-message.md`.
- Primary outreach email drafted for inviting a qualified Salesforce customer into the controlled SentinelFlow real-customer pilot.
- Subject options documented.
- Short follow-up message documented.
- LinkedIn / short DM version documented.
- Call booking note documented.
- Qualification questions documented for Salesforce admin availability, target org, Salesforce Cases, safe Case creation, hosted API callouts, and stakeholder participation.
- Sender notes documented to keep the message practical, controlled, human-approved, audit-focused, and clear about pilot limitations.
- Rollback note: documentation-only draft; remove `docs/customer-facing-pilot-outreach-message.md` and this maintenance entry if the outreach message is replaced.

27C pilot demo script:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/pilot-demo-script.md`.
- Demo goal documented: show a real pilot customer how SentinelFlow turns a Salesforce operational incident into an explainable, approval-gated, auditable workflow.
- Demo audience documented for Salesforce admins, operations leads, support/service leaders, automation owners, technical evaluators, security stakeholders, governance/audit stakeholders, customer success/support managers, and executive sponsors.
- 30-minute demo agenda documented from opening story through architecture overview, flow failure incident, approval/rejection, Case creation, Replay Timeline, Dashboard + Org Health Score, security/privacy, and closing questions.
- Opening story documented around a Salesforce automation failure requiring risk, recommendation, approval, safe action, and audit trail.
- Product architecture explanation documented for Salesforce package, hosted Zentom API, hosted database, risk scoring, policy decision, recommendation/runbook selection, approval panel, Case creation, Replay Timeline, dashboard, and Org Health Score.
- Live flow failure incident demo documented with expected `FLOW_FAILURE` scenario, risk score `95`, risk level `CRITICAL`, policy `HUMAN_APPROVAL_REQUIRED`, runbook `FLOW_FAILURE_BASIC_RECOVERY`, and safe action `CREATE_CASE`.
- Approval/rejection demo documented with approval panel, recommendation, runbook, approval status, execution readiness, rejection path, and Viewer read-only expectations.
- Case creation demo documented with approved execution, `CREATE_CASE`, Case origin, priority, subject, incident reference, and duplicate execution safety.
- Replay Timeline demo documented with expected audit events from `INCIDENT_RECEIVED` through `CASE_CREATED`.
- Dashboard + Org Health Score demo documented for recent incidents, risk distribution, approval queue/status, execution visibility, and customer review questions.
- Security/privacy explanation documented with human approval, no full autonomous remediation, no secrets in incident text/logs/replay, permission set separation, safe error logging, and pilot limitations.
- Closing questions and follow-up checklist documented for pilot fit, setup ownership, callout approval, Case creation, security/privacy requirements, support issues, v1.0.1 patch routing, and roadmap routing.
- Next phase documented: 27D Pilot Feedback Review Template, followed by 27E Pilot Success Report.
- Rollback note: documentation-only milestone; remove `docs/pilot-demo-script.md` and this maintenance entry if the pilot demo script is replaced.

27D pilot feedback review template:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/pilot-feedback-review-template.md`.
- Pilot customer, pilot date, participants, and scenarios tested sections documented.
- Scenario checklist documented for package validation, permissions, hosted API/DB health, callout configuration, `FLOW_FAILURE` test incident, write-back, risk/policy/recommendation/runbook review, approval/rejection, Case creation, Replay Timeline, Dashboard, Org Health Score, and support escalation.
- What worked well section documented for setup, permissions, hosted API, incident intake, risk/policy, recommendation/runbook, approval, Case creation, Replay Timeline, dashboard, Org Health Score, and support experience.
- Issues found section documented with severity guidance, evidence, owner, status, production issue tracking, v1.0.1 patch routing, roadmap routing, and workaround capture.
- Feature requests section documented with customer value, priority, target path, and classification guidance.
- Security/privacy concerns section documented with checklist for secrets, screenshots, replay evidence, error logs, API key handling, human approval boundary, Viewer access, and data privacy constraints.
- Onboarding friction section documented for package install, permissions, callout setup, health validation, API key setup, test incident, approval panel, Case creation, Replay Timeline, dashboard, and support handoff.
- Product value score section documented with 1-5 scoring rubric and supporting value signals.
- Go/no-go recommendation section documented for go, conditional go, extend pilot, patch before expanding, and no-go outcomes.
- Action items, follow-up owner, and target fix milestone sections documented.
- Next phase documented: 27E Pilot Success Report.
- Rollback note: documentation-only milestone; remove `docs/pilot-feedback-review-template.md` and this maintenance entry if the feedback review template is replaced.

27E pilot success report:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/pilot-success-report.md`.
- Purpose documented: summarize the outcome of a real customer SentinelFlow pilot and decide whether to expand, patch, extend validation, or pause rollout.
- Pilot summary section documented with customer, org type, Salesforce Org Id, pilot dates, owner fields, objective, and scope completion checklist.
- Customer profile section documented with industry/use case, org type, workflow evaluated, Salesforce Case usage, participants, success criteria, and fit assessment.
- Scenarios completed section documented for package validation, permissions, hosted API/DB health, `FLOW_FAILURE` test incident, write-back, risk/policy/recommendation/runbook review, approval/rejection, Case creation, Replay Timeline, dashboard, Org Health Score, and support validation.
- Success criteria results section documented with pass/fail evidence table and overall success result.
- Customer feedback summary section documented for what worked well, issues, feature requests, onboarding friction, security/privacy concerns, product value score, and customer quote/summary.
- Risk and issue summary section documented with severity, type, owner, target milestone, status, and P0/P1 disposition.
- v1.0.1 patch candidates section documented with candidate rules that keep patch scope focused on blockers, onboarding/docs, stability, replay/audit, approval/execution, and hosted API fixes while excluding major AI architecture changes, hosted HYBRID Ollama, Agentforce production integration, full autonomous remediation, and large object model changes.
- Roadmap candidates section documented for Agentforce integration, advanced AI/HYBRID hosted model strategy, setup wizard, Named Credential default switch, advanced replay search, adoption analytics, and additional integrations.
- Support and follow-up plan documented with owners, cadence, customer communication checklist, and open support items.
- Go/no-go decision and final recommendation sections documented.
- Milestone 27 marked ready for customer execution and reporting.
- Rollback note: documentation-only milestone; remove `docs/pilot-success-report.md` and this maintenance entry if the pilot success report template is replaced.

## Milestone 28: AppExchange / AgentExchange Submission Finalization

Status: Complete

Planned scope:

- 28A: Final Submission Checklist.
- 28B: Final Listing Assets.
- 28C: Screenshots + Demo Script Finalization.
- 28D: Security Review Evidence Cross-check.
- 28E: Install/Test Org Final Validation.
- 28F: Submission Readiness Wrap-up.

Current active milestone:

```text
Milestone 28 - AppExchange / AgentExchange Submission Finalization
```

28A final submission checklist:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/appexchange-submission-checklist.md`.
- Purpose documented: confirm SentinelFlow has required package, listing, demo, security, install validation, support, and rollback evidence before final marketplace submission.
- Submission scope documented for AppExchange / AgentExchange readiness, Salesforce package security review readiness, final listing and demo assets, final install/test org validation, and controlled marketplace rollout after real customer pilot preparation.
- Exclusions documented for hosted HYBRID Ollama, full autonomous remediation, Agentforce production integration, major AI architecture changes, large object model changes, and experimental/unstable metadata.
- Final package checklist documented for stable manifest, Apex, LWC, objects, custom metadata, permission sets, app/tabs/layouts/list views, Remote Site fallback, Named Credential path, no hardcoded secrets, no local-only URLs, and no public Ollama exposure.
- Install and test org checklist documented for clean org validation, permission sets, app/dashboard/approval/replay loading, API configuration, health checks, test incident, approval/rejection, Case creation, replay events, and Viewer read-only behavior.
- Security review checklist documented with evidence pack, CRUD/FLS sharing review, Apex/LWC scan checklist, callout decision, privacy documentation, API authentication, error logging, permission boundaries, human approval, known gaps, and mitigations.
- Listing asset checklist documented for product name, descriptions, features, business value, target users, setup summary, support path, privacy/security summary, limitations, screenshots, demo script, and customer-facing pilot message.
- Screenshot and demo checklist documented for dashboard, incident detail, approval panel, recommendation/policy view, created Case, Replay Timeline, Org Health Score, setup view, standard `FLOW_FAILURE` scenario, and secret-safe demo data.
- Support and operations checklist documented for SLA, troubleshooting, issue tracking, onboarding, metrics, feedback-to-roadmap, patch planning, pilot feedback, and pilot success report templates.
- Hosted API checklist documented for base URL, health endpoints, PostgreSQL, required tables, pgvector, incident receive endpoint, authentication behavior, error logging, cold-start/uptime strategy, and production hosting limitations.
- Customer pilot evidence checklist documented for pilot plan, outreach pack, customer-facing message, demo script, feedback template, success report, blocker mapping, and go/no-go decision.
- Release, rollback, submission go/no-go, no-go criteria, and final sign-off sections documented.
- Next phase documented: 28B Final Listing Assets.
- Rollback note: documentation-only milestone; remove `docs/appexchange-submission-checklist.md` and this maintenance entry if the final submission checklist is replaced.

28B final listing assets:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/final-listing-assets.md`.
- Product name documented as `SentinelFlow by Tomcodex`, with alternate `SentinelFlow - Powered by Zentom AI`.
- Recommended positioning documented: Salesforce-native incident intelligence and governed automation powered by Zentom AI.
- Tagline, short description, marketplace-safe short description, and long description documented.
- Key features documented for Salesforce incident intake, hosted Zentom API integration, risk scoring, policy governance, recommendation/runbook selection, human approval, safe Case creation, Replay Timeline, dashboard, Org Health Score, permission sets, error logging, and support documentation.
- Target users documented for Salesforce admins, developers, support operations, RevOps, sales operations, enterprise platform teams, automation owners, and governance/audit stakeholders.
- Category and keywords documented with guidance to avoid unsupported autonomous remediation, Agentforce production integration, or hosted HYBRID Ollama claims.
- Screenshot list documented for dashboard, Sentinel Incident detail, approval panel, risk/policy/recommendation, created Case, Replay Timeline, Dashboard + Org Health Score, and optional setup/support views.
- Demo video plan documented with 3-5 minute flow from incident problem through dashboard, `FLOW_FAILURE`, risk/policy/recommendation/runbook, approval, Case creation, Replay Timeline, and Org Health Score.
- Logo / brand asset checklist documented for primary logo, square icon, transparent/light/dark assets, high-resolution marketplace image, colors, naming, Zentom AI positioning, and trademark hygiene.
- Support contact placeholder documented with reminder to replace before submission.
- Privacy/security links and listing security/privacy summaries documented.
- Listing review checklist documented for final copy, assets, support, privacy/security, limitations, unsupported claims, and submission owner approval.
- Next phase documented: 28C Screenshots + Demo Script Finalization.
- Rollback note: documentation-only milestone; remove `docs/final-listing-assets.md` and this maintenance entry if the final listing assets plan is replaced.

28C screenshots + demo script finalization:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/screenshots-demo-script-finalization.md`.
- Purpose documented: create a clean, consistent, privacy-safe screenshot and demo package for the SentinelFlow Salesforce workflow from app launch through incident review, approval, Case creation, replay, and governance explanation.
- Required screenshots documented: SentinelFlow App Home / Dashboard, Sentinel Incident record, AI Recommendation section, Human Approval panel, Replay Timeline, Policy Decision record, Audit Log list, Case created from approved action, and Org Health Score card.
- Screenshot naming convention documented with stable lowercase `sentinelflow-##-*` filenames.
- Demo video flow documented: open SentinelFlow app, show dashboard and Org Health Score, trigger test `FLOW_FAILURE` incident, open created incident, explain risk/policy/recommendation/runbook, approve incident, execute approved action, show created Case, show Replay Timeline, and close with security/governance explanation.
- Demo script final version documented with marketplace-safe talk track and explicit guardrails around human approval, Viewer read-only access, secret-safe evidence, and excluded full autonomous remediation, hosted HYBRID Ollama, and production Agentforce integration.
- Visual QA checklist documented for screenshot quality, UI framing, privacy, naming, listing alignment, demo clarity, unsupported claims, and security/privacy explanation.
- Privacy/sample data rules documented for synthetic data, approved demo orgs, no customer data, no credentials, no regulated data, and standard `FLOW_FAILURE` sample data.
- Final asset checklist documented for required screenshot filenames, demo video, review, captions/transcript, listing consistency, privacy/security review, and submission owner approval.
- Next phase documented: 28D Security Review Evidence Cross-check.
- Rollback note: documentation-only milestone; remove `docs/screenshots-demo-script-finalization.md` and this maintenance entry if the screenshot/demo finalization plan is replaced.

28D security review evidence cross-check:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/security-review-evidence-cross-check.md`.
- Purpose documented: confirm SentinelFlow security, privacy, package validation, hosted API, callout, authentication, error logging, and known-gap evidence is complete and internally consistent before final submission.
- Evidence documents reviewed section documented with primary and supporting security, privacy, callout, install, support, submission, and demo/listing evidence references.
- Package validation evidence documented for `v1.0.0-rc.1`, production validation commit `92e344c`, package tests 17 passing / 0 failing, validation org `astrosoft`, deploy validation ID `0AfdL00000az6W5SAI`, and hardened package deploy ID `0AfdL00000azAXBSA2`.
- Fresh org validation evidence documented as passed with scratch org `sentinelflow-beta-18f`, deploy ID `0AfBi000007rTsgKAE`, 14 tests passing / 0 failing, hosted callout success, incident creation, approval, Case creation, and Replay Timeline evidence.
- Production validation evidence documented for hosted API live, hosted DB + pgvector verified, Salesforce incident write-back, risk/policy/runbook output, approval/execution, Case creation, replay events, and error logging evidence.
- Security controls evidence documented for human approval, Viewer read-only access, permission separation, `with sharing`, CRUD/FLS review, Apex/LWC security scan checklist, excluded autonomous/Agentforce/HYBRID Ollama scope, replay evidence, safe error logging, and secret-safe demo assets.
- Privacy and retention evidence documented for Salesforce-to-Zentom data, Salesforce storage, hosted PostgreSQL storage, no public Ollama exposure, human approval, customer data-entry cautions, retention/deletion/export/access controls, and final asset privacy rules.
- Callout / Named Credential evidence documented for Remote Site fallback, Named Credential path validation, External Credential / Permission Set Mapping future path, hosted API URL, and final callout mode validation requirement.
- API authentication evidence documented for shared secret auth, correct key acceptance, missing/wrong key HTTP 401 rejection, safe API key handling, hosted API error logging, `/api/health/errors`, and Salesforce `Sentinel_Error_Log__c`.
- Known gaps and mitigations documented for explicit CRUD/FLS enforcement posture, hosted RULE mode, excluded Agentforce production integration, excluded full autonomous remediation, Render cold starts, final screenshots/demo capture, and final install/test org validation.
- Missing evidence checklist documented for 28E validation, screenshots, demo video, support placeholders, security/privacy links, package evidence, callout mode, CRUD/FLS posture, unsupported claims, secret/customer data exclusion, and final sign-off.
- Final cross-check result documented as substantially complete for submission finalization planning, with required final actions before submission.
- Next phase documented: 28E Install/Test Org Final Validation.
- Rollback note: documentation-only milestone; remove `docs/security-review-evidence-cross-check.md` and this maintenance entry if the security evidence cross-check is replaced.

28E install/test org final validation:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/install-test-org-final-validation.md`.
- Purpose documented: prove the current SentinelFlow submission candidate deploys cleanly, passes tests, connects to hosted Zentom API/database, processes standard `FLOW_FAILURE`, supports approval/execution, creates a Salesforce Case, records Replay Timeline events, logs errors safely, and loads the dashboard.
- Target validation org section documented with org alias, type, Org Id, username, validation date, owner, and readiness checklist.
- Package manifest section documented for `apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml`, `v1.0.0-rc.1`, target reference, and manifest checks for stable metadata, permissions, callout metadata, no experimental Agentforce metadata, no temporary files, no local URLs, and no hardcoded secrets.
- Deployment command section documented for `sf project deploy validate` and optional `sf project deploy start` with `RunLocalTests`, deploy/validation id, status, timing, and required result of clean deploy with 17 passing / 0 failing tests.
- Test classes run section documented with expected 17 passing / 0 failing result and stable test coverage areas.
- Permission sets assigned section documented for `SentinelFlow_Admin`, `SentinelFlow_Approver`, and `SentinelFlow_Viewer`, including Admin, Approver, and Viewer behavior checks.
- Hosted API verification documented for `https://zentom-api.onrender.com`, root health, `/api/health/db`, PostgreSQL, required tables, `missingTables = []`, pgvector, incident receive endpoint, and shared secret behavior.
- Salesforce incident test documented for standard `FLOW_FAILURE`, expected risk `95`, level `CRITICAL`, policy `HUMAN_APPROVAL_REQUIRED`, runbook `FLOW_FAILURE_BASIC_RECOVERY`, and Sentinel Incident write-back evidence.
- Approval + execution test documented for approval panel, recommendation/runbook visibility, approval status, execution action `CREATE_CASE`, execution status, incident status, created Case reference, Case subject, priority, and origin.
- Replay Timeline test documented with expected events from `INCIDENT_RECEIVED` through `CASE_CREATED`, ordering, secret-safe evidence, and demo suitability.
- Dashboard test documented for app launch, dashboard load, recent incident visibility, status/risk summary, approval queue/status, execution activity, Org Health Score, and role-specific access.
- Error logging test documented for controlled failure, `Sentinel_Error_Log__c`, status code, endpoint, sanitized payloads, API key exclusion, hosted API error logging, and no secret exposure.
- Pass/fail summary and final submission readiness result sections documented with required proof points and blocker tracking.
- Next phase documented: 28F Submission Readiness Wrap-up.
- Rollback note: documentation-only milestone; remove `docs/install-test-org-final-validation.md` and this maintenance entry if the final validation plan is replaced.

28F submission readiness wrap-up:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/submission-readiness-wrap-up.md`.
- Purpose documented: summarize final submission readiness assets, evidence, validation plans, known gaps, and go/no-go posture before moving into actual marketplace submission execution.
- Milestone 28 summary documented with 28A through 28F completed.
- Submission assets completed section documented for final checklist, listing assets, screenshots/demo finalization, security evidence cross-check, install/test validation, and wrap-up.
- Security evidence completed section documented for security review evidence pack, final checklist, security prep, CRUD/FLS review, Apex/LWC scan checklist, privacy/retention, callout security, Named Credential evidence, shared-secret auth, error logging, and evidence cross-check.
- Listing assets completed section documented for `SentinelFlow by Tomcodex`, positioning, tagline, descriptions, features, target users, categories/keywords, screenshots, demo video plan, brand checklist, support placeholder, privacy/security links, and listing review checklist.
- Install/test validation completed section documented for target org fields, manifest, deployment commands, 17 passing / 0 failing expectation, permissions, hosted API/DB, `FLOW_FAILURE`, approval/execution, Replay Timeline, dashboard, error logging, pass/fail summary, and readiness result.
- Known submission gaps documented for actual screenshot capture, demo video recording/approval, support/contact placeholder replacement, final validation evidence execution/attachment, explicit CRUD/FLS enforcement posture, and final marketplace form submission.
- Final go/no-go status documented as go for Submission Execution, with conditional go pending final execution evidence.
- Next phase documented as Milestone 29 Submission Execution.
- Milestone 28 marked complete.
- Rollback note: documentation-only milestone; remove `docs/submission-readiness-wrap-up.md` and this maintenance entry if the submission wrap-up is replaced.

Milestone 28 wrap-up:

- Status: Complete.
- Completed scope: 28A final submission checklist, 28B final listing assets, 28C screenshots + demo script finalization, 28D security review evidence cross-check, 28E install/test org final validation, and 28F submission readiness wrap-up.
- Milestone 28 result: AppExchange / AgentExchange submission finalization planning is complete.
- Final readiness posture: go for Submission Execution, conditional on final execution evidence.
- Next milestone: Milestone 29 Submission Execution.

## Milestone 29: Submission Execution

Status: Complete

Planned scope:

- 29A: Submission Account / Partner Setup Verification.
- 29B: Package Version / Upload Preparation.
- 29C: Security Review Submission Execution.
- 29D: Listing Submission Execution.
- 29E: Review Feedback Tracking.
- 29F: Submission Wrap-up.

Current active milestone:

```text
Milestone 29 - Submission Execution
```

29A submission account / partner setup verification:

- Date: 2026-05-25.
- Status: Started.
- Document created: `docs/submission-execution-plan.md`.
- Purpose documented: move from submission planning to actual AppExchange / AgentExchange submission execution by verifying publisher account readiness, package/version readiness, evidence readiness, listing/demo assets, blockers, and submission status tracking.
- Submission target documented for AppExchange / AgentExchange marketplace submission for `SentinelFlow by Tomcodex`.
- Partner / publisher account readiness documented for Salesforce Partner Community access, publisher account, publisher profile, submission owner, security review submitter, listing editor, technical contact, support contact, agreements, submission workspace, package upload access, listing asset upload access, and security review submission access.
- Package version readiness documented for final manifest, package version/upload candidate, `v1.0.0-rc.1`, target reference, validation evidence, 17 passing / 0 failing tests, fresh org validation, and exclusion of experimental metadata, temporary files, hardcoded secrets, local-only URLs, and public Ollama exposure.
- Security review evidence readiness documented for evidence pack, final checklist, security prep, CRUD/FLS review, Apex/LWC scan checklist, privacy/retention, callout security, Named Credential evidence, shared secret auth, error logging, hosted API/DB evidence, known gaps, and cross-check.
- Listing asset readiness documented for product name, tagline, descriptions, features, users, categories/keywords, screenshots, logo/brand assets, support contact, documentation URL, privacy/security links, review checklist, and unsupported claim removal.
- Demo asset readiness documented for screenshot capture, naming, visual QA, secret/customer-data exclusion, demo video, demo script, transcript/captions, validated claims, and governance explanation.
- Submission steps documented from account access through package/evidence/listing/demo uploads, review, security submission, listing submission, status recording, feedback tracking, remediation routing, and maintenance update.
- Submission blockers documented for account access, package upload, validation, tests, hosted API/DB, screenshots/demo, support placeholders, security evidence gaps, unsupported claims, and secret/customer-data exposure.
- Submission status tracker documented for 29A through 29F.
- Next phase documented: 29B Package Version / Upload Preparation.
- Rollback note: documentation-only milestone; remove `docs/submission-execution-plan.md` and this maintenance entry if the submission execution plan is replaced.

29B package version / upload preparation:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/package-version-upload-preparation.md`.
- Purpose documented: confirm package candidate, manifest, validation evidence, metadata scope, upload steps, validation org steps, rollback plan, and readiness criteria before uploading or submitting the package version.
- Package version target documented for SentinelFlow Salesforce package submission candidate with clean deploy, stable tests, hosted Zentom API, safe callout default, human approval, safe Case creation, Replay Timeline, dashboard, and Org Health Score.
- Current release candidate documented as `v1.0.0-rc.1`, with stable tests 17 passing / 0 failing, hosted API `https://zentom-api.onrender.com`, default callout mode `REMOTE_SITE`, and Named Credential path validated but not default.
- Package manifest documented as `apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml` with short reference `manifest/package-sentinelflow-beta.xml`.
- Pre-upload validation checklist documented for manifest review, deploy validation, tests, hosted API/DB, PostgreSQL, pgvector, Base URL, callout mode, Named Credential posture, shared secret auth, error logging, no hardcoded secrets, no local-only URLs, no public Ollama endpoint, upload owner, and rollback plan.
- Package metadata included section documented for stable Apex, tests, LWCs, objects, fields, custom metadata, app, tabs, layouts, list views, permission sets, Remote Site fallback, Named Credential metadata, error log object, policy decision metadata, and runbook metadata.
- Package metadata excluded section documented for experimental Agentforce metadata, full autonomous remediation, hosted HYBRID Ollama config, local-only URLs, hardcoded secrets/API keys, temporary files, old static resources, package drift, large object model changes, customer-specific metadata, and local test configuration.
- Upload steps documented from owner/access confirmation through manifest/release/commit review, metadata review, validation, hosted API/DB checks, callout mode confirmation, package upload/version creation, evidence capture, and maintenance update.
- Validation org steps documented for clean org, permission sets, Base URL, `REMOTE_SITE`, hosted API, hosted DB, `FLOW_FAILURE`, Sentinel Incident, approval/execution, Case creation, Replay Timeline, dashboard, Org Health Score, and error logging.
- Rollback / re-upload plan documented for upload/install/test/API/callout/approval/execution/replay/dashboard/error logging/metadata failures.
- Upload readiness criteria documented.
- Next phase documented: 29C Security Review Submission Execution.
- Rollback note: documentation-only milestone; remove `docs/package-version-upload-preparation.md` and this maintenance entry if the package upload preparation plan is replaced.

29C security review submission execution:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/security-review-submission-execution.md`.
- Purpose documented: submit the SentinelFlow security review package with complete evidence, accurate scope, known gaps disclosed, and a clear post-submission tracking and remediation workflow.
- Submission scope documented for Salesforce package, hosted Zentom API integration, incident intake, risk/policy/recommendation/runbook write-back, human approval/rejection, approved Case creation, Replay Timeline, dashboard, Org Health Score, error logging, Remote Site default, validated Named Credential path, and shared-secret API authentication.
- Out-of-scope items documented: full autonomous remediation, hosted HYBRID Ollama, Agentforce production integration, major AI architecture changes, large object model changes, and customer-specific integrations.
- Security review package contents documented with package validation, fresh org validation, production validation, security review evidence pack, CRUD/FLS + sharing review, Apex/LWC security checklist, privacy/retention, callout documentation, Named Credential validation, shared-secret auth, error logging, known gaps, install guide, and troubleshooting guide.
- Evidence documents submitted section documented with primary and supporting evidence references.
- Code / metadata evidence documented for stable Apex, tests, LWC, objects, policy/audit/error objects, custom metadata, permission sets, app/tabs/layouts/list views, Remote Site fallback, Named Credential metadata, validation evidence, and excluded metadata.
- External callout evidence documented for hosted API `https://zentom-api.onrender.com`, default `REMOTE_SITE`, Named Credential path validated but not default, Remote Site, Named Credential migration/implementation, hosted health, callout failure logging, and no local/public Ollama endpoint.
- Data privacy evidence documented for Salesforce-to-Zentom data, Salesforce storage, hosted PostgreSQL storage, replay/audit evidence, error logging, retention/deletion/export/access controls, and customer data-entry cautions.
- AI governance evidence documented for governed recommendation workflow, human approval, policy decisions, safe Case creation, Replay Timeline, and excluded autonomous/HYBRID Ollama/Agentforce scope.
- Known gaps disclosed section documented for explicit CRUD/FLS enforcement posture, hosted HYBRID Ollama exclusion, Agentforce production integration exclusion, full autonomous remediation exclusion, Render cold-start behavior, and final asset secret-safe review.
- Submission steps, post-submission tracking, and response/remediation workflow documented.
- Next phase documented: 29D Listing Submission Execution.
- Rollback note: documentation-only milestone; remove `docs/security-review-submission-execution.md` and this maintenance entry if the security review submission execution plan is replaced.

29D listing submission execution:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/listing-submission-execution.md`.
- Purpose documented: submit the SentinelFlow marketplace listing with approved product positioning, listing copy, screenshots, demo assets, support contact, privacy/security links, beta/production notes, and post-submission tracking.
- Listing target documented for AppExchange / AgentExchange listing for `SentinelFlow by Tomcodex`.
- Product positioning documented: Salesforce-native incident intelligence and governed automation powered by Zentom AI.
- Product name section documented with primary product name, alternate name, publisher, and name review checklist.
- Short and long descriptions documented with marketplace-safe wording and unsupported-claim checks.
- Category / keywords documented for Salesforce incident management, automation governance, AI incident intelligence, approval workflow, Case creation, replay timeline, audit trail, Org Health Score, Zentom AI, operations, runbook automation, policy governance, and AppExchange / AgentExchange readiness.
- Screenshots submitted section documented with required screenshot list, recommended filenames, visual/privacy review, and upload checklist.
- Demo video / demo script section documented with final demo flow and review checklist.
- Support contact section documented with placeholders for support email, support URL, documentation URL, and support references.
- Privacy / security links section documented with security/privacy references, listing security summary, and review checklist.
- Beta / production notes documented for hosted API, default `REMOTE_SITE`, Named Credential validated but not default, current limitations, hosting posture, and data-entry cautions.
- Submission steps, post-submission tracking, and listing approval criteria documented.
- Next phase documented: 29E Review Feedback Tracking.
- Rollback note: documentation-only milestone; remove `docs/listing-submission-execution.md` and this maintenance entry if the listing submission execution plan is replaced.

29E review feedback tracking:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/review-feedback-tracking.md`.
- Purpose documented: track every marketplace, listing, package, and security review response from receipt through triage, remediation, validation, re-submission, and closure.
- Feedback sources documented for Salesforce security review, AppExchange/AgentExchange listing review, package upload/version feedback, partner/publisher account feedback, demo/screenshot review, privacy/security documentation review, support/contact review, customer pilot evidence feedback, and internal submission owner notes.
- Feedback statuses documented: Received, Under Review, Accepted, Rejected, Fix In Progress, Fix Validated, Re-submitted, and Closed.
- Severity / priority levels documented from P0 through P4 with response expectations for submission blockers, reviewer-required changes, trust/supportability issues, clarifications, and backlog ideas.
- Review owner section documented for security review, package/version, listing copy/assets, privacy/legal, support/contact, and maintenance log ownership.
- Response timeline documented by severity with triage and response/fix targets.
- Evidence required section documented by feedback type, including package/test, security, CRUD/FLS/sharing, callout/auth, privacy, error logging, listing copy, screenshot/demo, and support/contact issues.
- Remediation workflow documented from feedback receipt through status tracking, ownership, severity, fix/response, validation, re-submission, closure, and maintenance update.
- Re-submission checklist documented for P0/P1 resolution, validation evidence, tests, install/test validation, security evidence, listing copy, assets, support/privacy links, limitation accuracy, unsupported claim checks, submission owner approval, and maintenance update.
- Final approval tracking documented for security review, package/version, listing, screenshots/demo, support/privacy links, final approval evidence, and readiness for 29F.
- Next phase documented: 29F Submission Wrap-up.
- Rollback note: documentation-only milestone; remove `docs/review-feedback-tracking.md` and this maintenance entry if the feedback tracking process is replaced.

29F submission wrap-up:

- Date: 2026-05-25.
- Status: Complete.
- Document created: `docs/submission-execution-wrap-up.md`.
- Purpose documented: summarize submission execution assets, package/security/listing readiness, review tracking process, remaining execution gaps, and next customer-first beta pilot phase.
- Milestone 29 summary documented with 29A through 29F completed.
- Submission execution assets completed section documented for `docs/submission-execution-plan.md`, `docs/package-version-upload-preparation.md`, `docs/security-review-submission-execution.md`, `docs/listing-submission-execution.md`, `docs/review-feedback-tracking.md`, and `docs/submission-execution-wrap-up.md`.
- Package upload readiness documented for `v1.0.0-rc.1`, package manifest `apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml`, 17 passing / 0 failing tests, hosted API, default `REMOTE_SITE`, and Named Credential path validated but not default.
- Security review submission readiness documented for evidence pack, CRUD/FLS + sharing review, Apex/LWC checklist, privacy/retention, Named Credential evidence, shared-secret auth, production validation, submission execution plan, and feedback tracking.
- Listing submission readiness documented for `SentinelFlow by Tomcodex`, positioning, listing execution plan, final listing assets, screenshot/demo plan, support/privacy/security links, and unsupported claim guardrails.
- Feedback tracking readiness documented for statuses, severity/priority model, review ownership, timelines, evidence requirements, remediation workflow, re-submission checklist, and final approval tracking.
- Known remaining gaps documented for actual partner/publisher account verification, package upload/version evidence, security review submission id, listing submission id, screenshot/demo upload, support/contact placeholder replacement, and explicit CRUD/FLS enforcement posture.
- Product rule documented: no new features now; release beta, run pilot, collect feedback, fix only P0/P1/P2 issues.
- Final submission status documented as prepared for execution, with external marketplace evidence dependent on actual account/package/listing/security review actions.
- Next phase documented as Milestone 30 Beta Customer Pilot Execution.
- Milestone 29 marked complete.
- Rollback note: documentation-only milestone; remove `docs/submission-execution-wrap-up.md` and this maintenance entry if the submission execution wrap-up is replaced.

Milestone 29 wrap-up:

- Status: Complete.
- Completed scope: 29A submission account / partner setup verification, 29B package version / upload preparation, 29C security review submission execution, 29D listing submission execution, 29E review feedback tracking, and 29F submission wrap-up.
- Milestone 29 result: submission execution planning and tracking assets are complete.
- Product rule: no new features now; release beta, run pilot, collect feedback, fix only P0/P1/P2 issues.
- Next milestone: Milestone 30 Beta Customer Pilot Execution.

## Milestone 30: Beta Customer Pilot Execution

Status: Complete

Planned scope:

- 30A: Select pilot customer/org.
- 30B: Schedule pilot demo.
- 30C: Install/validate package.
- 30D: Run pilot scenarios.
- 30E: Capture feedback.
- 30F: Go/No-Go decision.
- 30G: Pilot success report.

Current next milestone:

```text
Milestone 30 - Beta Customer Pilot Execution
```

Beta rule:

```text
No new features now.
Run pilot.
Collect feedback.
Fix only P0/P1/P2 issues.
```

30A select pilot customer/org:

- Date: 2026-05-25.
- Status: Started.
- Document created: `docs/beta-customer-pilot-selection.md`.
- Purpose documented: select a real beta customer and Salesforce org for a controlled SentinelFlow pilot before any new feature expansion.
- Pilot objective documented for real Salesforce validation, install/configuration, hosted API/DB, `FLOW_FAILURE`, human approval, Case creation, Replay Timeline, dashboard value, feedback capture, and P0/P1/P2 issue identification.
- Ideal pilot customer documented with Salesforce admin availability, sandbox/developer org, Case validation, operational workflow fit, guided demo/setup participation, feedback availability, and controlled beta expectations.
- Org selection criteria documented for sandbox/developer preference, Case access, outbound callouts, permission assignment, hosted API, default `REMOTE_SITE`, Named Credential path validated but not default, contacts, support escalation, beta limitations, and no sensitive data in test incident text.
- Candidate evaluation tracker and scoring documented.
- Pilot scope confirmation documented with included validation activities and excluded new feature/AI/Agentforce scope.
- Pilot readiness decision options and no-go criteria documented.
- Next phase documented: 30B Schedule pilot demo.
- Rollback note: documentation-only milestone; remove `docs/beta-customer-pilot-selection.md` and this maintenance entry if the pilot selection process is replaced.

30B schedule pilot demo:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/beta-pilot-demo-schedule.md`.
- Pilot customer/org placeholders documented for customer name, Salesforce org, org type, org id, customer contacts, internal owner, and selected 30A source.
- Demo date/time placeholders documented for date, time, time zone, duration, meeting link, recording approval, scheduling requirements, and readiness timing.
- Participants documented for customer admin, operations/support owner, security/privacy stakeholder, sponsor, demo lead, pilot owner, support owner, and feedback owner.
- Demo objective documented for real customer environment validation, governed automation explanation, customer feedback capture, and P0/P1/P2 issue identification.
- Demo agenda documented from introductions through dashboard, `FLOW_FAILURE`, Sentinel Incident, risk/policy/recommendation, approval/rejection, Case creation, Replay Timeline, security/privacy explanation, and questions.
- Required preparation documented for customer admin access, Case object access, permission assignment, outbound callouts, no sensitive production data, package/version target, hosted API/DB, scenario readiness, support owner, and feedback notes.
- Salesforce org access documented for admin access, SentinelFlow app/records, Case object, setup items, sandbox/developer preference, production-data caution, and minimal org detail capture.
- Package/API readiness check documented for `v1.0.0-rc.1`, package manifest, 17 passing / 0 failing tests, hosted API, hosted DB, `REMOTE_SITE`, Named Credential path validated but not default, shared secret auth, and error logging.
- Test scenario list documented for app/dashboard, Org Health Score, `FLOW_FAILURE`, incident, AI recommendation, policy decision, approval, execution, Case creation, Replay Timeline, audit logs, and controlled error logging.
- Feedback capture plan documented for onboarding, trust, approval clarity, Case value, replay/audit confidence, dashboard value, security/privacy concerns, P0/P1/P2 issues, deferred feature requests, and severity triage.
- Follow-up actions documented for recap, owners, P0/P1/P2 logging, deferred feature request separation, and readiness for install/validation.
- Locked beta rule reaffirmed: no new features now; run pilot; collect feedback; fix only P0/P1/P2 issues.
- Next phase documented: 30C Install/validate package.
- Rollback note: documentation-only milestone; remove `docs/beta-pilot-demo-schedule.md` and this maintenance entry if the demo scheduling process is replaced.

30C install/validate package:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/beta-pilot-install-validation.md`.
- Pilot org placeholders documented for customer name, Salesforce org, org type, org id, admin, validation owner, and validation date.
- Package/version section documented for `v1.0.0-rc.1`, package manifest, 17 passing / 0 failing baseline, selected beta pilot org, and install evidence.
- Permission set assignment section documented for SentinelFlow admin/user access, Case access, Sentinel Incident access, Policy Decision access, Replay/audit access, assigned users, evidence, and result.
- Hosted API URL documented as `https://zentom-api.onrender.com`.
- Callout mode documented as default `REMOTE_SITE`, with Named Credential path validated but not default.
- API health check documented with expected successful hosted API response, actual result, status, evidence, and failure severity guidance.
- DB health check documented with hosted DB status, vector/search dependency status where applicable, expected pilot workflow support, actual result, status, and evidence.
- Test incident command documented as `FLOW_FAILURE` with non-sensitive sample payload guidance.
- Expected validation result documented: hosted API `https://zentom-api.onrender.com`, Risk `95 / CRITICAL`, Policy `HUMAN_APPROVAL_REQUIRED`, Runbook `FLOW_FAILURE_BASIC_RECOVERY`, Status `Approval Required`.
- Validation evidence checklist documented for package install, permission set assignment, API/DB health, callout configuration, test command/payload, Sentinel Incident record, expected values, and error log result.
- Pass/fail result section documented for package install, permission sets, hosted API, hosted DB, callout mode, test incident, expected result, error logging, overall status, blockers, P0/P1/P2 issues, and readiness for 30D.
- Locked beta rule reaffirmed: no new features now; run pilot; collect feedback; fix only P0/P1/P2 issues.
- Next phase documented: 30D Run pilot scenarios.
- Rollback note: documentation-only milestone; remove `docs/beta-pilot-install-validation.md` and this maintenance entry if the install validation template is replaced.

30D run pilot scenarios:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/beta-pilot-scenario-run.md`.
- Pilot org section documented for customer name, Salesforce org, org type, org id, pilot run date, scenario owner, customer admin/contact, locked beta rule, and prerequisites.
- Scenario list documented for app/dashboard access, Org Health Score, `FLOW_FAILURE`, risk/policy, AI recommendation/runbook, approval, rejection, approved execution, Case creation, Replay Timeline, audit/error logging, and pass/fail capture.
- `FLOW_FAILURE` incident test documented with expected incident creation, `Approval Required` status, non-sensitive payload guidance, execution details, evidence, and pass criteria.
- Risk + policy verification documented with expected risk `95 / CRITICAL` and expected policy `HUMAN_APPROVAL_REQUIRED`.
- AI recommendation + runbook check documented with expected runbook `FLOW_FAILURE_BASIC_RECOVERY`, customer clarity, unsupported-claim guardrail, and human approval governance.
- Approval workflow test documented for reviewing the test incident, approving action, state capture, execution availability only after approval, and replay/audit evidence.
- Rejection workflow test documented for rejecting recommended action, state capture, execution blocking, and no Case/remediation after rejection.
- Case creation execution test documented for approved `FLOW_FAILURE` action, Salesforce Case creation, field/context validation, link/reference capture, and replay/audit evidence.
- Replay Timeline verification documented for incident creation, risk/policy/recommendation, approval/rejection, execution, Case creation, timestamps, missing events, and evidence.
- Dashboard + Org Health Score check documented for dashboard load, card visibility, recent pilot activity, UI clarity, and customer value confirmation.
- Error logging check documented for successful run log review, controlled failure handling, sensitive-data avoidance, diagnosability, and P0/P1/P2 issue creation.
- Pass/fail summary documented with scenario result table, evidence, issue ids, final status, P0/P1/P2 counts, backlog separation, and readiness for 30E.
- Locked beta rule reaffirmed: no new features now; run pilot; collect feedback; fix only P0/P1/P2 issues.
- Next phase documented: 30E Capture feedback.
- Rollback note: documentation-only milestone; remove `docs/beta-pilot-scenario-run.md` and this maintenance entry if the scenario run template is replaced.

30E capture feedback:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/beta-pilot-feedback-capture.md`.
- Purpose documented: capture pilot feedback structurally, separate active P0/P1/P2 fixes from future backlog ideas, and prepare inputs for go/no-go.
- Pilot customer/org placeholders documented for customer, org, pilot date, feedback date, participants, and feedback owner.
- Feedback sources documented for live demo discussion, scenario notes, admin feedback, operations/support feedback, security/privacy feedback, customer-approved media, logs, evidence, and follow-up notes.
- Feedback categories documented across onboarding, install, permissions, hosted API/callout reliability, `FLOW_FAILURE`, risk/policy, AI recommendation, runbook, approval/rejection, Case creation, Replay Timeline, dashboard, error logging, security/privacy, documentation gaps, and deferred features.
- Severity levels documented from P0 through P4 with active beta fix rule limiting immediate fixes to P0/P1/P2.
- Customer value signals and value score documented for triage value, approval trust, AI recommendation usefulness, runbook fit, Case creation fit, Replay Timeline auditability, Org Health Score value, pilot continuation, and expansion readiness.
- Feedback log documented with source, category, feedback, severity, owner, status, and target fix milestone.
- Security/privacy feedback section documented with hosted API, shared secret auth, customer data, logs/audit, AI content, documentation evidence, and escalation rule.
- Onboarding friction section documented for install, permission set, Remote Site/callout setup, API health check, test incident setup, user navigation, and documentation gaps.
- Action item tracker documented with severity, owner, due date, evidence, status, P0/P1/P2 ownership requirements, and P3/P4 backlog separation.
- Go/no-go inputs documented for completed scenarios, open P0/P1/P2 items, value signal, security/privacy blockers, customer continuation, and readiness for another beta org.
- Follow-up plan documented for customer recap, issue severity confirmation, owner/target fix milestone, backlog separation, fix validation session, and 30F inputs.
- Locked beta rule reaffirmed: no new features now; run pilot; collect feedback; fix only P0/P1/P2 issues.
- Next phase documented: 30F Go/No-Go decision.
- Rollback note: documentation-only milestone; remove `docs/beta-pilot-feedback-capture.md` and this maintenance entry if the feedback capture template is replaced.

30F go/no-go decision:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/beta-pilot-go-no-go-decision.md`.
- Purpose documented: make a clear beta pilot decision based on install validation, scenario execution, customer feedback, value signals, and open P0/P1/P2 risk.
- Decision summary documented with go, conditional go, no-go, decision date, decision owner, customer pilot owner, internal approver, and decision statement.
- Pilot scope reviewed section documented for 30A through 30E and evidence reviewed from org selection through open issue list.
- Required evidence section documented for pilot org, package install, hosted API/DB, callout mode, `FLOW_FAILURE`, risk/policy/runbook/status, approval, rejection, Case creation, Replay Timeline, dashboard, error logging, and feedback capture.
- P0/P1/P2 issue review documented with decision rules: open P0 is no-go, open P1 is no-go unless explicitly mitigated and accepted, open P2 is conditional go only with mitigation, and P3/P4 remain backlog only.
- Customer value review documented for 30E value score, triage value, human approval trust, AI recommendation, runbook, Case creation, Replay Timeline, Org Health Score, and customer continuation.
- Security/privacy review documented for hosted API, shared secret auth, customer data handling, logs/audit, AI output, documentation/evidence, and blocker rules.
- Go, conditional go, and no-go criteria documented with required status, mitigations, customer acceptance, blockers, and fix milestone expectations.
- Decision record documented for final decision, rationale, accepted limitations, required fixes, deferred backlog, customer confirmation, and internal approval.
- Next actions documented for go, conditional go, and no-go outcomes.
- Locked beta rule reaffirmed: no new features now; run pilot; collect feedback; fix only P0/P1/P2 issues.
- Next phase documented: 30G Pilot success report.
- Rollback note: documentation-only milestone; remove `docs/beta-pilot-go-no-go-decision.md` and this maintenance entry if the go/no-go template is replaced.

30G pilot success report:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/beta-pilot-success-report.md`.
- Pilot summary documented for customer, org, dates, package/version, hosted API, pilot owner, report owner, report date, and locked beta rule.
- Pilot org/user section documented for Salesforce org, org type, org id, customer admin, business user/operator, validation owner, support owner, package install, permission sets, hosted API, hosted DB, and callout mode.
- Scenarios completed section documented for pilot org selection, demo schedule, package validation, hosted API/DB, `FLOW_FAILURE`, risk/policy, AI recommendation/runbook, approval, rejection, Case creation, Replay Timeline, dashboard/Org Health Score, error logging, feedback capture, and go/no-go decision.
- What worked section documented for setup, API/DB, incident creation, risk/policy, recommendation/runbook, approval/rejection, Case creation, replay/audit, dashboard, error logging, onboarding, and observed customer value.
- Issues found section documented with issue tracker and categories across install, permissions, API/callout/auth, DB, incident creation, risk/policy/recommendation, approval/rejection, Case creation, replay/audit, dashboard, error logging, security/privacy, and documentation/onboarding.
- Customer feedback summary documented for value score, most useful capability, least clear capability, recommendation trust, approval trust, security/privacy comfort, onboarding friction, support expectations, willingness to continue, notes, and deferred feature requests.
- P0/P1/P2 issues section documented for active beta fix candidates, required fixes, target milestone, owner, validation evidence, and no-new-feature rule.
- Go/no-go decision documented with final result options: `GO - Ready for controlled rollout`, `CONDITIONAL GO - Fix listed items first`, and `NO-GO - Pilot blockers found`.
- Patch items section documented for v1.0.1 handoff, patch scope, and excluded major/new feature work.
- Final beta result section documented with GO / CONDITIONAL GO / NO-GO, readiness areas, and Milestone 30 complete marker.
- Next milestone documented: Milestone 31 v1.0.1 Patch / Pilot Feedback Fixes.
- Locked beta rule reaffirmed: no new features now; run pilot; collect feedback; fix only P0/P1/P2 issues.
- Milestone 30 marked complete.
- Rollback note: documentation-only milestone; remove `docs/beta-pilot-success-report.md` and this maintenance entry if the success report template is replaced.

Milestone 30 wrap-up:

- Status: Complete.
- Completed scope: 30A select pilot customer/org, 30B schedule pilot demo, 30C install/validate package, 30D run pilot scenarios, 30E capture feedback, 30F go/no-go decision, and 30G pilot success report.
- Milestone 30 result: beta customer pilot execution documentation is complete and ready for real pilot evidence population.
- Product rule: no new features now; run pilot; collect feedback; fix only P0/P1/P2 issues.
- Next milestone: Milestone 31 v1.0.1 Patch / Pilot Feedback Fixes.

## Milestone 31: v1.0.1 Patch / Pilot Feedback Fixes

Status: Active

Planned scope:

- Review beta pilot success report.
- Triage P0/P1/P2 pilot issues.
- Fix only approved P0/P1/P2 issues.
- Validate fixes against pilot evidence.
- Prepare v1.0.1 patch notes and release readiness.

Current next milestone:

```text
Milestone 31 - v1.0.1 Patch / Pilot Feedback Fixes
```

Beta rule:

```text
No new features now.
Run pilot.
Collect feedback.
Fix only P0/P1/P2 issues.
```

31A pilot feedback triage:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/pilot-feedback-triage.md`.
- Purpose documented: review beta pilot feedback, identify only P0/P1/P2 issues eligible for v1.0.1 patch work, and defer all feature requests or low-priority improvements.
- Patch rule documented: no new features; only pilot feedback fixes P0/P1/P2.
- Triage inputs documented from beta pilot success report, feedback capture, go/no-go decision, scenario run, install validation, customer notes, logs, and screenshots.
- Triage scope documented for pilot blockers, hosted API failures, install/package blockers, callout/authentication failures, approval/execution defects, Case creation defects, replay/audit defects, dashboard/Org Health Score defects, error logging defects, security/privacy issues, and onboarding/documentation corrections.
- Exclusions documented for new features, major AI architecture changes, Hosted HYBRID Ollama, Agentforce production integration, full autonomous remediation, large object model changes, and P3/P4 enhancements.
- Severity rules documented for P0/P1/P2/P3/P4 and patch eligibility limited to P0/P1/P2.
- Triage workflow documented from feedback collection through duplicate removal, severity assignment, evidence confirmation, ownership, validation definition, backlog deferral, and 31B handoff.
- Triage table documented with source, summary, area, severity, patch eligibility, owner, evidence, and decision.
- Evidence requirements documented for customer/org context, scenario, expected result, actual result, severity rationale, sanitized proof, and validation step.
- Decision outcomes documented: accept for v1.0.1 patch, needs more evidence, duplicate, defer to backlog, or reject as out of scope.
- Approved patch candidate list and deferred backlog list documented.
- Next phase documented: 31B P0/P1/P2 Fix Plan.
- Rollback note: documentation-only milestone; remove `docs/pilot-feedback-triage.md` and this maintenance entry if the triage template is replaced.

31B P0/P1/P2 fix plan:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/p0-p1-p2-fix-plan.md`.
- Purpose documented: convert approved pilot feedback triage items into a controlled v1.0.1 fix plan with owners, validation evidence, rollback paths, and patch readiness criteria.
- Patch rule documented: no new features; only pilot feedback fixes P0/P1/P2.
- Fix scope documented for accepted P0/P1/P2 pilot feedback, pilot blockers, hosted API failures, package install blockers, callout/authentication failures, approval/execution defects, Case creation defects, replay/audit defects, dashboard/Org Health Score defects, error logging defects, security/privacy issues, and onboarding/documentation corrections.
- P0 issues section documented with definition, fix table, source evidence, owner, required fix, validation, status, and no-readiness rule while P0 remains open.
- P1 issues section documented with definition, fix table, source evidence, owner, required fix, validation, status, and no-readiness rule while unmitigated P1 remains open.
- P2 issues section documented with definition, fix table, source evidence, owner, required fix, validation, status, and mitigation/acceptance rule.
- Out-of-scope items documented for new features, P3/P4 improvements, major AI architecture changes, Hosted HYBRID Ollama, Agentforce production integration, full autonomous remediation, large object model changes, marketplace expansion, broad UI redesign, and non-pilot roadmap ideas.
- Fix owner section documented for patch owner, technical owner, QA/validation owner, customer follow-up owner, security/privacy reviewer, release notes owner, and ownership rules.
- Validation requirements documented by issue type, including package/install, hosted API, hosted DB, callout/authentication, incident creation, risk/policy, approval/execution, replay/audit, dashboard, error logging, and documentation/onboarding.
- Rollback plan documented for scoped file changes, clean commits, individual fix rollback, hosted API artifact/commit reference, Salesforce metadata/package state, rollback triggers, and validation after rollback.
- Patch readiness criteria documented for fixed/validated P0, fixed or mitigated P1, fixed/mitigated/deferred P2, no new features, no out-of-scope architecture changes, validation evidence, security/privacy signoff, rollback plan, release notes input, and 31C readiness.
- Next phase documented: 31C Patch Scope Freeze.
- Rollback note: documentation-only milestone; remove `docs/p0-p1-p2-fix-plan.md` and this maintenance entry if the fix plan template is replaced.

31C patch scope freeze:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/patch-scope-freeze.md`.
- Purpose documented: freeze v1.0.1 patch scope before implementation so only approved P0/P1/P2 pilot feedback fixes enter the patch.
- Patch rule documented: no new features; only pilot feedback fixes P0/P1/P2.
- Freeze decision section documented for freeze date, freeze owner, patch owner, technical owner, validation owner, release owner, freeze status, and decision statement.
- Approved scope documented from 31A triage, 31B fix plan, beta pilot success report, go/no-go decision, and validated pilot evidence.
- Approved fix categories documented for P0 blockers, P1 workflow defects, P2 material pilot issues, security/privacy corrections, hosted API, callout/authentication, package/install, approval/execution, Case creation, replay/audit, dashboard, error logging, and documentation fixes tied to pilot evidence.
- Frozen out-of-scope items documented for new features, P3/P4 improvements, major AI architecture changes, Hosted HYBRID Ollama, Agentforce production integration, full autonomous remediation, large object model changes, marketplace expansion, broad UI redesign, non-pilot roadmap ideas, unrelated performance optimization, and unnecessary refactors.
- Entry criteria documented for completed 31A/31B, approved candidates, owner/evidence/validation requirements, P3/P4 separation, security/privacy reviewer path, and rollback approach.
- Change control documented for adding only confirmed P0/P1/P2 items after freeze, evidence requirements, patch/validation owner approval, security/privacy reopen path, and deferred feature requests.
- Implementation guardrails documented for small fixes, no unrelated refactors, no object model expansion unless required, preserving callout behavior unless required, no AI architecture changes, no Agentforce production integration, no autonomous remediation, and validation evidence capture.
- Validation gate documented for package tests, hosted API, hosted DB, affected pilot scenario, error logging, Replay Timeline/audit, dashboard/Org Health Score, and documentation/onboarding validation.
- Exit criteria documented for finalized approved/out-of-scope lists, accepted change control, accepted guardrails, accepted validation gate, confirmed rollback expectations, and readiness for 31D.
- Next phase documented: 31D Patch Implementation.
- Rollback note: documentation-only milestone; remove `docs/patch-scope-freeze.md` and this maintenance entry if the scope freeze template is replaced.

31D patch implementation:

- Date: 2026-05-25.
- Status: Complete at documentation level.
- Document created: `docs/patch-implementation.md`.
- Purpose documented: track implementation of frozen, approved P0/P1/P2 pilot feedback fixes for v1.0.1 without adding new features or unrelated refactors.
- Patch rule documented: no new features; only pilot feedback fixes P0/P1/P2.
- Implementation preconditions documented for completed 31A/31B/31C, frozen approved fix list, severity, owner, evidence, validation requirement, and rollback expectation.
- Approved fix implementation tracker documented with fix id, severity, summary, owner, files changed, commit, status, and validation status.
- P0, P1, and P2 implementation sections documented with implementation notes, commits, validation evidence, result, and severity-specific readiness rules.
- Implementation guardrails documented for approved fixes only, small reviewable changes, no unrelated refactors, no broad UI redesign, no object model changes unless required, no AI architecture changes, no Hosted HYBRID Ollama, no Agentforce production integration, no autonomous remediation, and no P3/P4 backlog items.
- Validation tracking documented for package deploy/install, Apex tests, hosted API, hosted DB, callout/authentication, `FLOW_FAILURE`, risk/policy/runbook, approval/rejection, Case creation, Replay Timeline/audit, dashboard/Org Health Score, error logging, and documentation/onboarding.
- Regression check documented for package tests, hosted API, default callout mode, approval/execution, Case creation, replay/audit, dashboard, and no committed secrets/sensitive data.
- Rollback tracking documented with trigger, method, rollback commit/reference, result, rollback rules, and re-validation requirement.
- Exit criteria documented for implemented/validated/mitigated/deferred P0/P1/P2 fixes, no new features, no out-of-scope architecture changes, validation evidence, regression check, rollback tracking, and readiness for 31E.
- Next phase documented: 31E Patch Validation.
- Rollback note: documentation-only milestone; remove `docs/patch-implementation.md` and this maintenance entry if the implementation tracker is replaced.
