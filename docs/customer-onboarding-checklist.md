# SentinelFlow Customer Onboarding Checklist

## 1. Purpose

This checklist defines the Milestone 26B customer onboarding process for SentinelFlow v1.0.0-rc.1 and post-v1 customer rollout.

The goal is to give customer admins and the SentinelFlow support team a repeatable go-live path that verifies Salesforce access, package installation, permissions, Zentom API configuration, test incident processing, approval, execution, replay, dashboard, Org Health Score, and support handoff.

## 2. Target Customer Profile

Target customer:

- Salesforce customer with active admin access.
- Uses Salesforce Cases or wants SentinelFlow to create operational Cases after approved incident recommendations.
- Wants hosted Salesforce incident intelligence through the Zentom API.
- Can participate in guided onboarding, validation, and feedback capture.

Recommended onboarding roles:

- Salesforce Admin.
- SentinelFlow Admin.
- SentinelFlow Approver.
- SentinelFlow Viewer.
- Customer technical contact.
- SentinelFlow support/contact owner.

Target org types:

- Sandbox.
- Developer org.
- Production org.

Production org onboarding should happen only after sandbox/developer validation or explicit customer approval.

## 3. Pre-Onboarding Requirements

Before onboarding starts:

- [ ] Confirm customer has Salesforce admin access.
- [ ] Confirm target org type: sandbox, developer, or production.
- [ ] Confirm Salesforce Org Id.
- [ ] Confirm customer technical contact.
- [ ] Confirm customer approver contact.
- [ ] Confirm planned onboarding date/time.
- [ ] Confirm whether onboarding is validation-only or go-live.
- [ ] Confirm customer understands that free-form error messages should not contain sensitive personal data or regulated data.
- [ ] Confirm current SentinelFlow release candidate: `v1.0.0-rc.1`.
- [ ] Confirm hosted Zentom API target: `https://zentom-api.onrender.com`.
- [ ] Confirm package installation method and deployment owner.
- [ ] Confirm rollback contact and escalation path.

Evidence to capture:

- Org type.
- Org Id.
- Admin user or role.
- Permission assignment plan.
- Target callout mode: `REMOTE_SITE` or `NAMED_CREDENTIAL`.
- Planned validation scenario.

## 4. Salesforce Org Readiness Checklist

Org readiness:

- [ ] Salesforce admin can deploy metadata or install package components.
- [ ] Customer has access to Setup.
- [ ] Customer can assign permission sets.
- [ ] Customer can view Custom Metadata records.
- [ ] Customer can view Remote Site Settings.
- [ ] Customer can view Named Credentials if using `NAMED_CREDENTIAL` mode.
- [ ] Customer can run or coordinate anonymous Apex validation where needed.
- [ ] Customer can create Salesforce Cases or approve package users who can create Cases.
- [ ] Customer can access debug logs if troubleshooting is required.
- [ ] Customer has approved use of hosted Zentom API endpoint.

Org configuration checks:

- [ ] `Case.Origin` supports `SentinelFlow` or fallback behavior is accepted.
- [ ] Target users can open the SentinelFlow app.
- [ ] Browser restrictions do not block Lightning Web Components.
- [ ] Network/security policy allows callouts to `https://zentom-api.onrender.com`.
- [ ] Customer support channel is established for onboarding issues.

## 5. Package Installation Checklist

Package installation:

- [ ] Deploy SentinelFlow package.
- [ ] Confirm stable package components are installed.
- [ ] Confirm SentinelFlow app is available.
- [ ] Confirm custom objects are available:
  - `Sentinel_Incident__c`
  - `Sentinel_Audit_Log__c`
  - `Zentom_Policy_Decision__c`
  - `Sentinel_Error_Log__c`
  - `Zentom_Setting__mdt`
  - `Zentom_Runbook__mdt`
- [ ] Confirm Lightning Web Components are available:
  - `zentomApprovalPanel`
  - `zentomReplayTimeline`
  - `zentomDashboard`
- [ ] Confirm Apex classes are available:
  - `ZentomIncidentClient`
  - `ZentomApprovalController`
  - `ZentomExecutionController`
  - `ZentomReplayController`
  - `ZentomDashboardController`
  - `ZentomRunbookService`
- [ ] Confirm runbook metadata exists for `FLOW_FAILURE_BASIC_RECOVERY`.
- [ ] Confirm no install/deploy errors remain open.

Installation evidence:

- Deploy/package id if available.
- Deploy status.
- Test status if validation was run.
- Installed org id.
- Installer/admin contact.

## 6. Permission Assignment Checklist

Required permission sets:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

Assignment checklist:

- [ ] Assign `SentinelFlow_Admin` to customer admin or SentinelFlow admin user.
- [ ] Assign `SentinelFlow_Approver` to approval/execution users.
- [ ] Assign `SentinelFlow_Viewer` to read-only dashboard/replay users.
- [ ] Confirm Admin can open SentinelFlow app.
- [ ] Confirm Approver can open approval panel and replay timeline.
- [ ] Confirm Viewer can open dashboard/replay views without approval/execution access.
- [ ] Confirm Viewer cannot approve, reject, or execute actions.
- [ ] Confirm Approver has Case create access if approved execution will create Cases.
- [ ] Capture assigned users or role mapping.

Permission notes:

- Viewer should remain read-only.
- Approver should not receive delete, View All, or Modify All through the SentinelFlow permission set.
- Admin is a trusted package administration role.

## 7. Zentom API Configuration Checklist

Hosted API:

```text
https://zentom-api.onrender.com
```

Custom Metadata:

```text
Zentom_Setting__mdt.Default.Base_URL__c = https://zentom-api.onrender.com
```

Configuration checklist:

- [ ] Verify `Zentom_Setting__mdt.Default.Base_URL__c`.
- [ ] Verify `Zentom_Setting__mdt.Default.Is_Active__c = true`.
- [ ] Verify callout mode:
  - `REMOTE_SITE`, or
  - `NAMED_CREDENTIAL`.
- [ ] If `REMOTE_SITE`, verify Remote Site Setting `Zentom_API`.
- [ ] If `REMOTE_SITE`, verify Remote Site URL is `https://zentom-api.onrender.com`.
- [ ] If `NAMED_CREDENTIAL`, verify Named Credential `Zentom_API`.
- [ ] If `NAMED_CREDENTIAL`, verify endpoint resolves to `callout:Zentom_API/api/incidents/receive`.
- [ ] Verify API key/shared-secret configuration if enabled for the customer.
- [ ] Confirm no secret values are stored in committed metadata or customer-visible docs.
- [ ] Confirm hosted API health endpoint returns running status.
- [ ] Confirm hosted DB health endpoint returns PostgreSQL connected, `missingTables = []`, and pgvector enabled.

Current safe fallback:

- `REMOTE_SITE` remains the default fallback mode after production validation.
- `NAMED_CREDENTIAL` is the production/security-review target path and has been validated.

## 8. Test Incident Checklist

Run the standard test incident:

```text
Incident type: FLOW_FAILURE
Source: Salesforce Flow
Environment: production or sandbox, matching target org
Action type: CREATE_CASE
```

Test checklist:

- [ ] Run `FLOW_FAILURE` test incident.
- [ ] Confirm Salesforce callout completes.
- [ ] Confirm hosted Zentom API receives incident.
- [ ] Confirm Sentinel Incident is created.
- [ ] Confirm hosted Zentom incident id is populated.
- [ ] Confirm risk score is `95`.
- [ ] Confirm risk level is `CRITICAL`.
- [ ] Confirm policy is `HUMAN_APPROVAL_REQUIRED`.
- [ ] Confirm runbook is `FLOW_FAILURE_BASIC_RECOVERY`.
- [ ] Confirm approval status is `Pending Approval`.
- [ ] Confirm incident status is `Approval Required`.
- [ ] Confirm no `Sentinel_Error_Log__c` record was created for the successful path.

Evidence to capture:

- Sentinel Incident name/id.
- Hosted Zentom incident id.
- Risk score and level.
- Policy decision.
- Runbook key.
- Any error log id, if failure occurred.

## 9. Approval + Execution Verification

Approval verification:

- [ ] Open the test Sentinel Incident as Admin or Approver.
- [ ] Confirm approval panel loads.
- [ ] Confirm recommendation and runbook details are visible.
- [ ] Approve incident.
- [ ] Confirm `Approval_Status__c = Approved`.
- [ ] Confirm `Recommendation_Status__c = Approved`.
- [ ] Confirm `Execution_Status__c = Ready for Execution` or expected pre-execution value.

Execution verification:

- [ ] Execute Case creation.
- [ ] Confirm `Execution_Status__c = Executed`.
- [ ] Confirm `Execution_Action__c = CREATE_CASE`.
- [ ] Confirm incident status is `Action Created`.
- [ ] Confirm `Created_Case__c` is populated.
- [ ] Open created Case.
- [ ] Confirm Case `Origin = SentinelFlow`.
- [ ] Confirm Case priority is correct for CRITICAL/HIGH incidents.
- [ ] Confirm Case subject references `FLOW_FAILURE` and `CRITICAL`.

Negative checks:

- [ ] Viewer cannot approve incident.
- [ ] Viewer cannot execute Case creation.
- [ ] Incident cannot be executed before approval.
- [ ] Incident cannot be executed twice after successful execution.

## 10. Replay + Dashboard Verification

Replay Timeline checklist:

- [ ] Confirm Replay Timeline loads for the test incident.
- [ ] Confirm expected events are present:
  - `INCIDENT_RECEIVED`
  - `RISK_CALCULATED`
  - `ZENTOM_POLICY_EVALUATED`
  - `AI_RECOMMENDATION_GENERATED`
  - `RUNBOOK_SELECTED`
  - `HUMAN_APPROVED`
  - `RUNBOOK_ACTION_EXECUTED`
  - `CASE_CREATED`
- [ ] Confirm event order is correct.
- [ ] Confirm replay payloads do not expose secrets.
- [ ] Confirm no LWC or Apex permission errors appear.

Dashboard checklist:

- [ ] Confirm SentinelFlow dashboard loads.
- [ ] Confirm recent incident appears.
- [ ] Confirm approval queue reflects current status.
- [ ] Confirm recent execution/Case creation appears.
- [ ] Confirm risk distribution reflects CRITICAL incident.
- [ ] Confirm Dashboard + Org Health Score loads.
- [ ] Confirm Org Health Score area displays expected value/status.
- [ ] Confirm Admin, Approver, and Viewer see expected dashboard access.

## 11. Support Handoff Checklist

Support handoff:

- [ ] Capture customer admin contact.
- [ ] Capture customer approver contact.
- [ ] Capture support contact and escalation channel.
- [ ] Capture target org type and org id.
- [ ] Capture callout mode.
- [ ] Capture Sentinel Incident id from onboarding test.
- [ ] Capture created Case number/id.
- [ ] Capture Replay Timeline validation result.
- [ ] Capture Dashboard + Org Health Score validation result.
- [ ] Capture permission assignments.
- [ ] Capture known limitations or accepted risks.
- [ ] Capture customer feedback.
- [ ] Document any open onboarding issues in the production issue tracking process.

Customer feedback prompts:

- Was installation clear?
- Were permission roles understandable?
- Did the test incident result make sense?
- Was approval/execution workflow clear?
- Was replay timeline useful?
- Was dashboard/Org Health Score useful?
- What would block go-live?
- What should be improved before broader rollout?

## 12. Go-Live Readiness Criteria

Go-live can proceed when:

- [ ] Customer has Salesforce admin access confirmed.
- [ ] Target org type is documented.
- [ ] SentinelFlow package is deployed.
- [ ] Required permission sets are assigned.
- [ ] `Zentom_Setting__mdt.Default.Base_URL__c` is verified.
- [ ] Remote Site or Named Credential mode is verified.
- [ ] Hosted API health passes.
- [ ] Hosted DB health passes.
- [ ] `FLOW_FAILURE` test incident passes.
- [ ] Risk score `95` and risk level `CRITICAL` are confirmed.
- [ ] Policy `HUMAN_APPROVAL_REQUIRED` is confirmed.
- [ ] Runbook `FLOW_FAILURE_BASIC_RECOVERY` is confirmed.
- [ ] Incident approval passes.
- [ ] Case creation execution passes.
- [ ] Replay Timeline passes.
- [ ] Dashboard + Org Health Score pass.
- [ ] Support handoff is complete.
- [ ] Customer feedback is captured.
- [ ] No open P0/P1 onboarding issues remain.
- [ ] P2 issues are fixed or accepted with documented workaround.

No-go criteria:

- Package install fails.
- Required permissions cannot be assigned.
- Hosted API or DB health fails.
- Salesforce callout fails without accepted workaround.
- Incident write-back fails.
- Approval or execution fails.
- Case creation fails.
- Replay Timeline fails.
- Dashboard or Org Health Score fails.
- Secret exposure or security concern is detected.
