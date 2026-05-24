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

Status: Next
