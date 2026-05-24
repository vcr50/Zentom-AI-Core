# SentinelFlow Apex/LWC Security Scan Checklist

## 1. Purpose

This document defines the Milestone 23C Apex and Lightning Web Component security scan checklist for SentinelFlow v1.0.0-rc.1 security-review preparation.

The goal is to provide a repeatable review and remediation workflow for Apex, LWC, SOQL, DML, callouts, error handling, secrets handling, and static analysis before formal marketplace/security-review submission.

This checklist follows the 23B CRUD/FLS + sharing review finding:

```text
Stable Apex uses with sharing, but explicit CRUD/FLS enforcement still needs to be added or verified in the next implementation/security track.
```

## 2. Scope

In scope:

- Stable Apex classes included in `apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml`.
- Stable Lightning Web Components included in `apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml`.
- SOQL and DML inside stable SentinelFlow runtime classes.
- Salesforce callout code used by the hosted Zentom API integration.
- Error logging code on Salesforce and hosted API paths.
- Secrets handling in Apex, LWC, Custom Metadata, Named Credential, and environment configuration.

Stable Apex classes:

- `ZentomIncidentClient`
- `ZentomApprovalController`
- `ZentomExecutionController`
- `ZentomReplayController`
- `ZentomDashboardController`
- `ZentomRunbookService`

Stable LWCs:

- `zentomApprovalPanel`
- `zentomReplayTimeline`
- `zentomDashboard`

Out of scope:

- Legacy or experimental metadata not included in the stable beta package manifest.
- Portal/subscription/admin-console metadata not included in the SentinelFlow v1.0.0-rc.1 package scope.
- Hosted API implementation scans, except where Salesforce callout behavior and error handling depend on hosted API responses.

## 3. Apex Security Checklist

Class-level checks:

- [ ] Apex classes use `with sharing`, `inherited sharing`, or have a documented reason for another sharing mode.
- [ ] Stable runtime classes do not use `without sharing`.
- [ ] Public/global methods are limited to required package API surfaces.
- [ ] `@AuraEnabled` methods expose only the data needed by the LWC.
- [ ] Viewer roles cannot invoke mutating Apex through class access.

Secrets checks:

- [ ] No hardcoded API keys, passwords, bearer tokens, session ids, OAuth secrets, or Named Credential secrets.
- [ ] `ZENTOM_API_KEY` is handled as hosted environment configuration.
- [ ] `Zentom_Setting__mdt.Api_Key__c` remains blank in committed metadata.
- [ ] Debug logs and exceptions do not print secrets.

SOQL checks:

- [ ] No unsafe dynamic SOQL.
- [ ] If dynamic SOQL is introduced, bind variables and allowlisted field/object names are used.
- [ ] SOQL exposed to LWCs is reviewed for least data exposure.
- [ ] `WITH SECURITY_ENFORCED` is used where practical.
- [ ] When `WITH SECURITY_ENFORCED` is not practical, manual CRUD/FLS checks are documented.

DML checks:

- [ ] No unrestricted DML from user-controlled input.
- [ ] DML operations are guarded by workflow state checks.
- [ ] CRUD checks are performed before create, update, delete, or upsert operations.
- [ ] FLS checks or `Security.stripInaccessible` are used for user-sourced fields.
- [ ] Approval and execution state transitions cannot be bypassed by client input.

Workflow checks:

- [ ] Incidents must be approved before execution.
- [ ] Executed incidents cannot be executed again.
- [ ] Rejected incidents do not execute actions.
- [ ] Case creation remains policy-gated and approval-gated.
- [ ] Autonomous execution remains blocked in stable package metadata.

Error handling checks:

- [ ] User-visible Apex errors do not expose secrets.
- [ ] Exceptions are handled with safe messages.
- [ ] Error logs contain useful diagnostics without storing authorization headers or shared secrets.
- [ ] Callout failures are logged to `Sentinel_Error_Log__c` where appropriate.

## 4. LWC Security Checklist

Client-side secrets checks:

- [ ] No API keys, passwords, tokens, session ids, OAuth secrets, or Named Credential secrets in JavaScript.
- [ ] No hosted database URL or hosted API secret in JavaScript.
- [ ] No sensitive configuration stored in browser-visible constants.

Access and behavior checks:

- [ ] Buttons respect permission, Apex class access, and record state.
- [ ] Approval buttons are shown only when the incident is pending approval.
- [ ] Execution buttons are shown only when the incident is approved and not already executed.
- [ ] Viewer users cannot access approval or execution actions.
- [ ] Client-side UI gating is treated as convenience only; Apex remains the enforcement boundary.

External call checks:

- [ ] LWCs do not call external services directly.
- [ ] LWCs call Apex controllers for Salesforce and Zentom workflow actions.
- [ ] No browser-side `fetch()` calls to the hosted Zentom API.
- [ ] No CORS-dependent client integration path is introduced.

DOM and rendering checks:

- [ ] No unsafe DOM manipulation.
- [ ] No unsafe use of `innerHTML`.
- [ ] User-provided strings are rendered through standard LWC escaping.
- [ ] Toasts and inline errors do not reveal secrets, stack traces, or internal credentials.

Data exposure checks:

- [ ] LWC data objects contain only fields required by the UI.
- [ ] Replay and error log payloads are reviewed for sensitive data exposure.
- [ ] User-visible errors are concise and safe.
- [ ] Navigation targets are restricted to intended Salesforce records/pages.

## 5. SOQL / DML Review

SOQL review targets:

- `ZentomApprovalController.loadIncident`
- `ZentomExecutionController.loadApprovedIncident`
- `ZentomReplayController.getReplayTimeline`
- `ZentomDashboardController` dashboard and queue queries
- `ZentomRunbookService` runbook metadata lookups
- `ZentomIncidentClient` configuration and persistence flow

DML review targets:

- `ZentomIncidentClient` inserts `Sentinel_Incident__c`.
- `ZentomIncidentClient` inserts `Sentinel_Audit_Log__c`.
- `ZentomIncidentClient` inserts `Zentom_Policy_Decision__c`.
- `ZentomIncidentClient` inserts `Sentinel_Error_Log__c`.
- `ZentomApprovalController` updates `Sentinel_Incident__c`.
- `ZentomApprovalController` inserts `Sentinel_Audit_Log__c`.
- `ZentomExecutionController` inserts `Case`.
- `ZentomExecutionController` updates `Sentinel_Incident__c`.
- `ZentomExecutionController` inserts `Sentinel_Audit_Log__c`.

Review decisions to record:

| Area | Required decision | Status |
| --- | --- | --- |
| Read SOQL | Add `WITH SECURITY_ENFORCED` or document manual enforcement path. | Pending |
| Create DML | Add object create checks before inserts. | Pending |
| Update DML | Add object update checks before updates. | Pending |
| Field writes | Add FLS checks or `Security.stripInaccessible`. | Pending |
| Audit/error inserts | Decide system-controlled logging enforcement pattern. | Pending |
| Case creation | Confirm required fields and CRUD/FLS behavior in target org. | Pending |

Minimum remediation expectation:

- Mutating Apex methods must check object CRUD before DML.
- User-sourced field updates must enforce FLS or use `Security.stripInaccessible`.
- Read methods exposed to LWCs must either enforce field readability or intentionally return DTOs built from reviewed fields.

## 6. Callout Security Review

Current validated callout modes:

```text
REMOTE_SITE:
https://zentom-api.onrender.com/api/incidents/receive

NAMED_CREDENTIAL:
callout:Zentom_API/api/incidents/receive
```

Callout checklist:

- [ ] Callouts use HTTPS.
- [ ] Callouts target the approved hosted endpoint strategy.
- [ ] Named Credential `Zentom_API` exists and is validated.
- [ ] Remote Site Setting remains documented as fallback until final decision.
- [ ] Endpoint paths are not stored in Remote Site Setting URLs.
- [ ] Apex does not hardcode secrets.
- [ ] `X-Zentom-Api-Key` is sent only when configured.
- [ ] Shared-secret values are not logged.
- [ ] Non-2xx responses are handled and logged safely.
- [ ] Callout timeout and retry behavior are documented.

Decision dependency:

```text
23D - External Callout + Named Credential Final Decision
```

23D should decide whether v1.0 submission uses:

- `NAMED_CREDENTIAL` as the default package mode.
- `REMOTE_SITE` as a documented fallback only.
- Future External Credential and Permission Set Mapping as a required marketplace hardening step.

## 7. Error Handling Review

Apex error handling checks:

- [ ] `AuraHandledException` messages are user-safe.
- [ ] Low-level exception messages are not exposed when they could contain secrets.
- [ ] Callout failures create sanitized `Sentinel_Error_Log__c` records.
- [ ] Failed Case creation updates incident execution state safely.
- [ ] Approval/rejection errors do not leave partial unsafe state.
- [ ] Replay timeline records safe operational context.

Salesforce error log checks:

- [ ] `Sentinel_Error_Log__c` stores source class, error type, status code, endpoint, org id, incident type, request payload, response payload, and system-created marker where appropriate.
- [ ] API headers are not stored.
- [ ] `X-Zentom-Api-Key` is not stored.
- [ ] Request and response payloads are sanitized.
- [ ] Payload field visibility is reviewed for Viewer access.

Hosted API error handling checks:

- [ ] Unauthorized requests return HTTP 401.
- [ ] Unauthorized failures are logged server-side without storing secret values.
- [ ] Unexpected processing exceptions are logged safely.
- [ ] Health endpoints do not reveal credentials.

## 8. Secrets Handling Review

Secrets inventory:

| Secret/configuration | Expected location | Source-control status |
| --- | --- | --- |
| `ZENTOM_API_KEY` | Hosted Render environment variable | Not committed |
| `DATABASE_URL` | Hosted Render environment variable | Not committed |
| `Zentom_Setting__mdt.Api_Key__c` | Org-specific Salesforce configuration if used | Blank in Git |
| Named Credential secret/auth | Future Salesforce External Credential or Named Credential configuration | Not committed |
| Hosted API URL | `Zentom_Setting__mdt.Base_URL__c`, Remote Site, Named Credential endpoint | Public endpoint only |

Secrets checks:

- [ ] No secret values in Apex.
- [ ] No secret values in LWC JavaScript.
- [ ] No secret values in Custom Metadata committed to Git.
- [ ] No secret values in documentation examples.
- [ ] No secret values in debug output.
- [ ] No secret values in `Sentinel_Audit_Log__c`.
- [ ] No secret values in `Sentinel_Error_Log__c`.
- [ ] No secret values in hosted API error logs.

Review commands:

```text
rg -n "api[_-]?key|secret|token|password|bearer|DATABASE_URL|ZENTOM_API_KEY" apps/sentinelflow-salesforce docs services
rg -n "fetch\\(|XMLHttpRequest|innerHTML|lwc:dom=\"manual\"" apps/sentinelflow-salesforce/force-app/main/default/lwc
rg -n "Database.query|query\\(|insert |update |delete |upsert |without sharing" apps/sentinelflow-salesforce/force-app/main/default/classes
```

## 9. Static Analysis Tools

Required tools:

- Salesforce Code Analyzer.
- PMD rules.
- ESLint for LWC.
- Manual CRUD/FLS review.

Recommended Salesforce Code Analyzer commands:

```text
sf scanner run --target apps/sentinelflow-salesforce/force-app/main/default/classes --format table
sf scanner run --target apps/sentinelflow-salesforce/force-app/main/default/lwc --format table
sf scanner run --target apps/sentinelflow-salesforce/force-app/main/default --format csv --outfile security-scan-results.csv
```

Recommended PMD focus:

- Apex CRUD violation rules.
- Apex sharing violation rules.
- Apex SOQL injection rules.
- Apex XSS and unsafe escaping rules.
- Apex hardcoded credential rules.

Recommended ESLint focus:

- LWC security rules.
- Unsafe DOM access.
- Unsafe HTML injection.
- Direct browser network calls.
- Unused privileged imports or dead code.

Manual review focus:

- Permission-set class access.
- Object CRUD matrix.
- Field-level edit/read access.
- User-mode behavior for Admin, Approver, and Viewer.
- Apex mutating methods callable from LWC.
- Error messages and logs.

## 10. Findings Log Template

Use this template for each security scan finding:

```text
Finding ID:
Date:
Reviewer:
Source:
Tool/manual:
Severity: P0 / P1 / P2 / P3
Area: Apex / LWC / SOQL / DML / Callout / Error handling / Secrets / Permissions
File:
Line:
Description:
Impact:
Evidence:
Recommended fix:
Owner:
Status: Open / In Progress / Fixed / Accepted Risk / False Positive
Validation:
Rollback note:
```

Severity guidance:

- P0: secret exposure, direct unauthorized execution, or severe data exposure.
- P1: missing enforcement that could allow unauthorized data modification or sensitive data access.
- P2: security-review concern with available mitigation or low exploitability.
- P3: documentation, cleanup, or defense-in-depth improvement.

## 11. Remediation Workflow

Workflow:

1. Run Salesforce Code Analyzer on stable Apex and LWC package scope.
2. Run PMD rules for Apex security findings.
3. Run ESLint for LWC security findings.
4. Run manual CRUD/FLS review against the 23B matrix.
5. Log every finding using the template in this document.
6. Fix P0/P1 findings before submission.
7. Fix P2 findings or document accepted risk with mitigation.
8. Re-run scans after fixes.
9. Validate Salesforce package deploy and Apex tests.
10. Update `docs/maintenance.md` with affected files, validation evidence, and rollback note.

Remediation standards:

- Prefer explicit Apex CRUD/FLS checks for mutating paths.
- Prefer `Security.stripInaccessible` for user-sourced DML field protection.
- Prefer DTOs for LWC responses to avoid overexposing sObjects.
- Prefer server-side enforcement over client-side UI-only restrictions.
- Keep secrets in environment variables or Salesforce credential configuration, not source.

Exit criteria:

- No open P0 findings.
- No open P1 findings.
- P2 findings are fixed or accepted with documented mitigation.
- Static analysis output is archived or summarized.
- Manual CRUD/FLS review is complete.
- Package validation passes after remediation.

## 12. Final Security Scan Checklist

Preparation:

- [ ] Stable package scope confirmed.
- [ ] 23B CRUD/FLS + sharing review available.
- [ ] Salesforce org/test context selected.
- [ ] Scanner tools installed or available.

Apex:

- [ ] `with sharing` reviewed.
- [ ] No hardcoded secrets.
- [ ] No unsafe dynamic SOQL.
- [ ] No unrestricted DML.
- [ ] CRUD enforcement reviewed.
- [ ] FLS enforcement reviewed.
- [ ] Callouts use approved endpoint strategy.
- [ ] Errors logged safely.
- [ ] User-visible errors are safe.
- [ ] Tests cover approval and execution gates.

LWC:

- [ ] No secrets in JavaScript.
- [ ] Buttons respect permission/record state.
- [ ] No unsafe DOM manipulation.
- [ ] No direct external calls from client.
- [ ] User-visible errors do not expose secrets.
- [ ] Viewer cannot invoke approval/execution actions.

SOQL/DML:

- [ ] SOQL field exposure reviewed.
- [ ] DML object permissions reviewed.
- [ ] User-sourced field updates reviewed.
- [ ] Audit/error logging DML reviewed.
- [ ] Case creation DML reviewed.

Callouts and secrets:

- [ ] Named Credential path reviewed.
- [ ] Remote Site fallback reviewed.
- [ ] Shared-secret header reviewed.
- [ ] Secrets not committed.
- [ ] Secrets not logged.

Tools:

- [ ] Salesforce Code Analyzer run.
- [ ] PMD rules run.
- [ ] ESLint for LWC run.
- [ ] Manual CRUD/FLS review completed.

Final disposition:

- [ ] Findings log complete.
- [ ] P0/P1 findings closed.
- [ ] P2 findings fixed or accepted with mitigation.
- [ ] Package validation rerun if code changes were made.
- [ ] Maintenance doc updated.
- [ ] Ready for 23D External Callout + Named Credential Final Decision.
