# SentinelFlow CRUD/FLS + Sharing Review

## 1. Purpose

This document records the Milestone 23B CRUD, field-level security, sharing, Apex access, and LWC access review for the SentinelFlow v1.0.0-rc.1 security-review preparation track.

The goal is to show the current access model for stable SentinelFlow package objects, identify where permissions are intentionally broad or constrained, and capture gaps that should be addressed before formal marketplace/security-review submission.

Review scope:

- Stable Salesforce objects used by the release-candidate workflow.
- Stable SentinelFlow permission sets.
- Stable Apex controllers and runtime classes included in the beta package manifest.
- Stable Lightning Web Components included in the beta package manifest.

Out of scope:

- Legacy or experimental metadata not included in `apps/sentinelflow-salesforce/manifest/package-sentinelflow-beta.xml`.
- Subscription portal metadata and non-SentinelFlow legacy objects.
- Hosted Zentom API authorization, which is covered separately in `docs/security-review-evidence-pack.md`.

## 2. Salesforce Objects Reviewed

Reviewed objects:

- `Sentinel_Incident__c`
- `Sentinel_Audit_Log__c`
- `Zentom_Policy_Decision__c`
- `Sentinel_Error_Log__c`
- `Case`

Object purposes:

- `Sentinel_Incident__c`: stores incident summary, risk, policy, AI recommendation, approval, runbook, and execution state.
- `Sentinel_Audit_Log__c`: stores replay timeline events for incident intake, risk scoring, policy evaluation, recommendation, approval, execution, and Case creation.
- `Zentom_Policy_Decision__c`: stores policy decision context for a SentinelFlow incident.
- `Sentinel_Error_Log__c`: stores sanitized Salesforce-side callout/configuration failure evidence.
- `Case`: standard Salesforce object created only through the approved execution path.

Current custom object sharing models:

| Object | Sharing model | Notes |
| --- | --- | --- |
| `Sentinel_Incident__c` | `ReadWrite` | Package workflow state object. Permission sets constrain role operations. |
| `Sentinel_Audit_Log__c` | `ReadWrite` | Replay/audit log object. Approver and Viewer are read-only. |
| `Zentom_Policy_Decision__c` | `ReadWrite` | Policy decision object. Approver and Viewer are read-only. |
| `Sentinel_Error_Log__c` | `ReadWrite` | Diagnostic error log object. Approver and Viewer are read-only. |
| `Case` | Standard Salesforce sharing | Used for approved Case creation only. |

## 3. Permission Sets Reviewed

Reviewed permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

Role intent:

- `SentinelFlow_Admin`: package administrator role for SentinelFlow incident, audit, policy, error log, and runtime configuration visibility.
- `SentinelFlow_Approver`: workflow operator role that can review incidents, approve/reject recommendations, and execute approved Case creation.
- `SentinelFlow_Viewer`: read-only role for dashboard, incident, audit, policy, error log, replay, and runbook visibility.

Stable Apex class access:

| Apex class | Admin | Approver | Viewer | Notes |
| --- | --- | --- | --- | --- |
| `ZentomIncidentClient` | Yes | No | No | Admin-only runtime/test incident callout path. |
| `ZentomApprovalController` | Yes | Yes | No | Approval and rejection workflow controller. |
| `ZentomExecutionController` | Yes | Yes | No | Approved execution and Case creation controller. |
| `ZentomReplayController` | Yes | Yes | Yes | Replay timeline read access. |
| `ZentomDashboardController` | Yes | Yes | Yes | Dashboard/read model access; includes approval queue helpers for privileged roles. |
| `ZentomRunbookService` | Yes | Yes | Yes | Runbook read/lookup support. |

## 4. CRUD Access Matrix

Legend:

```text
C = Create
R = Read
U = Update/Edit
D = Delete
VA = View All Records
MA = Modify All Records
```

Current object-level access:

| Object | Admin | Approver | Viewer | Review note |
| --- | --- | --- | --- | --- |
| `Sentinel_Incident__c` | C/R/U/D + VA/MA | R/U | R | Approver can update workflow fields needed for approval/execution. Viewer is read-only. Admin has full object administration. |
| `Sentinel_Audit_Log__c` | C/R/U/D + VA/MA | R | R | Audit records are read-only for non-admin roles. Runtime Apex creates replay events. |
| `Zentom_Policy_Decision__c` | C/R/U/D + VA/MA | R | R | Policy records are read-only for non-admin roles. Runtime Apex creates policy decisions. |
| `Sentinel_Error_Log__c` | C/R/U/D + VA/MA | R | R | Error logs are read-only for non-admin roles. Runtime Apex creates sanitized error logs. |
| `Case` | C/R/U | C/R/U | No explicit package permission | Case creation is exposed to Admin and Approver because approved execution creates Salesforce Cases. Viewer has no package Case CRUD grant. |

Additional CRUD observations:

- `SentinelFlow_Admin` has `viewAllRecords` and `modifyAllRecords` on the four custom SentinelFlow data objects.
- `SentinelFlow_Approver` does not have delete access on reviewed objects.
- `SentinelFlow_Viewer` has read-only access to the four custom SentinelFlow data objects.
- `SentinelFlow_Viewer` has no explicit `Case` object permission in the reviewed permission set.
- `Case` delete is not granted by the reviewed package permission sets.

## 5. Field-Level Security Review

FLS review basis:

- Reviewed field permissions in `SentinelFlow_Admin.permissionset-meta.xml`.
- Reviewed field permissions in `SentinelFlow_Approver.permissionset-meta.xml`.
- Reviewed field permissions in `SentinelFlow_Viewer.permissionset-meta.xml`.

Field-level access summary:

| Object | Admin FLS | Approver FLS | Viewer FLS | Review note |
| --- | --- | --- | --- | --- |
| `Sentinel_Incident__c` | Read/write on reviewed package fields | Read on package fields; edit only workflow fields needed for approval/execution | Read-only on package fields | Approver edit scope includes approval, rejection, execution, created Case, status, and next action fields. |
| `Sentinel_Audit_Log__c` | Read/write on reviewed package fields | Read-only | Read-only | Replay payload fields are visible to Approver and Viewer. Confirm payloads stay sanitized before submission. |
| `Zentom_Policy_Decision__c` | Read/write on reviewed package fields | Read-only | Read-only | Policy decision details are visible across all roles. |
| `Sentinel_Error_Log__c` | Read/write on reviewed package fields | Read-only | Read-only | Error log payload and endpoint fields are visible to Approver and Viewer. Secrets are not stored by design. |
| `Case` | Standard object field access not explicitly enumerated in package permission set | Standard object field access not explicitly enumerated in package permission set | No package Case CRUD grant | Final review should confirm target org Case field requirements and profile/permission interactions. |

Approver editable `Sentinel_Incident__c` fields:

- `Approval_Status__c`
- `Approved_At__c`
- `Approved_By__c`
- `Created_Case__c`
- `Executed_At__c`
- `Execution_Action__c`
- `Execution_Result__c`
- `Execution_Status__c`
- `Next_Action__c`
- `Rejection_Reason__c`
- `Status__c`

Approver read-only `Sentinel_Incident__c` fields include:

- `AI_Confidence__c`
- `AI_Summary__c`
- `Environment__c`
- `Error_Message__c`
- `Incident_Type__c`
- `Policy_Decision__c`
- `Policy_Reason__c`
- `Recommendation_Status__c`
- `Recommended_Action__c`
- `Risk_Level__c`
- `Risk_Score__c`
- `Root_Cause__c`
- `Runbook_Description__c`
- `Runbook_Key__c`
- `Runbook_Steps__c`
- `Runbook_Title__c`
- `Source__c`
- `Zentom_Incident_Id__c`

Viewer access:

- Viewer has read-only field access for reviewed `Sentinel_Incident__c`, `Sentinel_Audit_Log__c`, `Sentinel_Error_Log__c`, and `Zentom_Policy_Decision__c` fields.
- Viewer does not have Apex class access to approval or execution controllers.

FLS notes:

- No Salesforce password, session token, OAuth secret, API secret, or Named Credential secret is stored in the reviewed SentinelFlow fields.
- `Sentinel_Audit_Log__c.Request_Payload__c`, `Sentinel_Audit_Log__c.Response_Payload__c`, `Sentinel_Error_Log__c.Request_Payload__c`, and `Sentinel_Error_Log__c.Response_Payload__c` must remain sanitized because they are readable by Approver and Viewer.
- `Zentom_Setting__mdt.Api_Key__c` is not part of this key-object review, but it must remain blank in Git and should not be exposed in user-facing LWCs.

## 6. Apex Sharing Review

Stable Apex classes reviewed:

- `ZentomIncidentClient`
- `ZentomApprovalController`
- `ZentomExecutionController`
- `ZentomReplayController`
- `ZentomDashboardController`
- `ZentomRunbookService`

Sharing declarations:

| Class | Sharing mode | Main operations |
| --- | --- | --- |
| `ZentomIncidentClient` | `with sharing` | Hosted API callout, incident persistence, audit log creation, policy decision creation, error log creation. |
| `ZentomApprovalController` | `with sharing` | Incident read, approval update, rejection update, audit log creation. |
| `ZentomExecutionController` | `with sharing` | Approved incident read, Case creation, incident execution update, audit log creation. |
| `ZentomReplayController` | `with sharing` | Replay timeline read. |
| `ZentomDashboardController` | `with sharing` | Dashboard queries, approval queue reads, lightweight approval/rejection helpers. |
| `ZentomRunbookService` | `with sharing` | Runbook metadata lookup. |

Positive findings:

- Stable Apex runtime classes use `with sharing`.
- Viewer permission set does not grant Apex access to approval or execution controllers.
- `ZentomExecutionController` requires `Approval_Status__c = Approved` before creating a Case.
- `ZentomExecutionController` blocks repeat execution when `Execution_Status__c = Executed`.
- Autonomous Agentforce-style execution remains blocked in the stable execution controller.
- `ZentomIncidentClient` sanitizes Salesforce-side error logging by not storing API headers or `X-Zentom-Api-Key`.

Review concerns:

- Stable Apex controllers do not currently use `WITH SECURITY_ENFORCED`, `Security.stripInaccessible`, or explicit `Schema.sObjectType` CRUD/FLS checks before all SOQL and DML operations.
- Existing security relies primarily on permission-set assignment, `with sharing`, class access, UI gating, and workflow state checks.
- `ZentomDashboardController` includes read methods and approval/rejection helper methods; final security review should confirm only Admin/Approver can invoke mutating methods through Apex class access and permissions.

Recommended pre-submission remediation:

- Add explicit object CRUD checks before DML in `ZentomIncidentClient`, `ZentomApprovalController`, and `ZentomExecutionController`.
- Add explicit field update checks or use `Security.stripInaccessible` for user-sourced updates.
- Add read access checks or `WITH SECURITY_ENFORCED` for SOQL exposed to LWCs where practical.
- Add tests that run as users with `SentinelFlow_Admin`, `SentinelFlow_Approver`, and `SentinelFlow_Viewer` permissions and assert expected allow/deny behavior.

## 7. LWC Access Review

Stable LWCs reviewed:

- `zentomApprovalPanel`
- `zentomReplayTimeline`
- `zentomDashboard`

LWC access model:

| LWC | Apex dependencies | Access behavior |
| --- | --- | --- |
| `zentomApprovalPanel` | `ZentomApprovalController`, `ZentomExecutionController` | Reads incident approval context, approves/rejects incidents, and executes approved Case creation through Apex. |
| `zentomReplayTimeline` | `ZentomReplayController` | Reads replay timeline events for the current incident. |
| `zentomDashboard` | `ZentomDashboardController` | Reads dashboard data and navigates to SentinelFlow records. |

Positive findings:

- Stable LWCs call Apex controllers rather than calling external services directly.
- Stable LWCs do not contain API keys, Named Credential secrets, or hosted database credentials.
- `zentomReplayTimeline` and `zentomDashboard` are read-oriented UI surfaces.
- `zentomApprovalPanel` depends on server-side workflow checks before approval, rejection, or execution state changes.
- Viewer permission set lacks Apex access to `ZentomApprovalController` and `ZentomExecutionController`, which prevents Viewer users from invoking approval/execution controller methods through the packaged class-access model.

Review concerns:

- LWC button visibility is not a complete security boundary; Apex must remain the final enforcement layer.
- Final security testing should verify the Viewer role cannot call mutating Apex methods directly.
- Final security testing should verify an Approver cannot bypass workflow state requirements and create a Case without an approved incident.

## 8. Known Gaps

Known gap: explicit CRUD/FLS enforcement is not consistently implemented in stable Apex.

Mitigation:

- Permission sets are role-scoped.
- Stable classes use `with sharing`.
- Apex class access prevents Viewer from calling approval/execution controllers.
- Workflow state checks gate approved execution.
- Add explicit CRUD/FLS checks in the 23C Apex/LWC Security Scan Checklist remediation track.

Known gap: custom object sharing model is `ReadWrite`.

Mitigation:

- Permission sets constrain object and field-level operations by role.
- Approver and Viewer do not receive View All or Modify All.
- Viewer is read-only.
- Final review should decide whether private sharing is required for customer production orgs.

Known gap: Admin has View All and Modify All on reviewed custom objects.

Mitigation:

- Admin role is intended for package administration and support operations.
- Delete and Modify All access should be explicitly accepted or reduced before formal marketplace submission if least-privilege review requires it.

Known gap: Approver can edit execution-state fields on `Sentinel_Incident__c`.

Mitigation:

- Approver needs these fields for approval and execution flow.
- Apex state checks require approved state before Case creation.
- Future hardening can move more field mutation into system-controlled Apex with narrower direct FLS edit grants.

Known gap: audit/error payload fields are readable by Approver and Viewer.

Mitigation:

- Error logging intentionally avoids storing API headers and shared-secret values.
- Customers are instructed not to put sensitive personal data in free-form error messages.
- Future hardening should add masking/minimization for payload fields and consider restricting payload field visibility to Admin/Approver only.

Known gap: `Case` field-level requirements are dependent on target org configuration.

Mitigation:

- Stable execution creates only Subject, Description, Priority, and Origin.
- Origin fallback uses `Web` if `SentinelFlow` is not active.
- Fresh-org and production validation confirmed Case creation with `Origin = SentinelFlow`.
- Final security review should verify required Case fields in target packaging/test orgs.

## 9. Security Review Notes

Security-review posture:

- Current role model is understandable and package-scoped.
- Viewer is read-only and does not receive approval/execution Apex class access.
- Approver can operate the approval/execution workflow but does not receive delete, View All, or Modify All permissions.
- Admin has broad package administration rights and should be treated as trusted.
- Stable Apex uses `with sharing`, but explicit CRUD/FLS enforcement should be strengthened before formal submission.

Security-review references:

- `docs/security-review-evidence-pack.md`
- `docs/security-review-preparation.md`
- `docs/security-review-final-checklist.md`
- `docs/data-privacy-retention.md`
- `docs/salesforce-callout-security.md`
- `docs/maintenance.md`

Validation references:

- v1.0.0-rc.1 tag target: `92e344c6fc865ab339d20ee37fec888bafaae1bc`
- Package validation: `0AfdL00000az6W5SAI`, 17 passing, 0 failing.
- Hardened package deploy: `0AfdL00000azAXBSA2`, 17 passing, 0 failing.
- Fresh-org validation: `0AfBi000007rTsgKAE`, 14 passing, 0 failing.
- Production validation incident: `SI-000013`.
- Production validation Case: `00001051`.
- Error log validation: `SEL-000000`.

## 10. Final Checklist

Current 23B checklist:

- [x] Reviewed key objects.
- [x] Reviewed key permission sets.
- [x] Documented CRUD matrix.
- [x] Documented field-level security posture.
- [x] Documented Apex sharing declarations.
- [x] Documented LWC access model.
- [x] Captured known gaps.
- [x] Captured security-review notes.
- [ ] Add explicit Apex CRUD checks before all stable DML.
- [ ] Add explicit Apex FLS checks or `Security.stripInaccessible` where user-visible/user-sourced fields are read or written.
- [ ] Add SOQL read enforcement where practical.
- [ ] Add role-based Apex tests for Admin, Approver, and Viewer allow/deny behavior.
- [ ] Decide whether custom object sharing should remain `ReadWrite` or move toward private sharing for production customer orgs.
- [ ] Decide whether Admin needs delete, View All, and Modify All on all reviewed custom objects.
- [ ] Decide whether payload fields should remain visible to Viewer.

Next milestone:

```text
23C - Apex/LWC Security Scan Checklist
```
