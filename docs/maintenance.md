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

Status: Started

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
