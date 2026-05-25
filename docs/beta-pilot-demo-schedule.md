# SentinelFlow Beta Pilot Demo Schedule

## 1. Pilot Customer/Org

Pilot customer/org:

- Customer name: TBD.
- Salesforce org name: TBD.
- Org type: Sandbox, developer org, or approved low-risk customer environment.
- Org id: TBD.
- Primary customer contact: TBD.
- Customer Salesforce admin: TBD.
- Internal pilot owner: TBD.

Selection source:

- Use the customer/org selected in 30A Select Pilot Customer / Org.
- Confirm the selected org can support package validation, hosted API callouts, Case creation, approval testing, Replay Timeline review, dashboard review, and feedback capture.

Locked beta rule:

```text
No new features now.
Run pilot.
Collect feedback.
Fix only P0/P1/P2 issues.
```

## 2. Demo Date/Time

Demo schedule:

- Date: TBD.
- Time: TBD.
- Time zone: TBD.
- Duration: 30 to 45 minutes.
- Meeting link: TBD.
- Recording: Optional, only with customer approval.

Scheduling requirements:

- Customer admin and business stakeholder should both be available.
- Internal support owner should be available for follow-up triage.
- Demo should be scheduled after package/API readiness checks are confirmed.

## 3. Participants

Customer participants:

- Salesforce admin.
- Operations or support owner.
- Security/privacy stakeholder, if available.
- Executive or technical sponsor, if available.

Internal participants:

- Demo lead.
- Pilot owner.
- Technical support owner.
- Note taker / feedback owner.

## 4. Demo Objective

Demo objective:

- Validate SentinelFlow in the selected customer Salesforce environment.
- Show the real beta workflow end to end.
- Confirm the customer understands the governed automation model.
- Capture usability, trust, onboarding, security, and operational feedback.
- Identify P0/P1/P2 issues that must be fixed before broader rollout.

The demo is not a new feature discovery session. Feature requests can be captured, but only P0/P1/P2 issues should enter the active beta fix path.

## 5. Demo Agenda

Recommended agenda:

1. Introductions and pilot objective.
2. Confirm selected Salesforce org and beta limitations.
3. Open SentinelFlow app.
4. Show dashboard and Org Health Score.
5. Trigger or review test `FLOW_FAILURE` incident.
6. Open created Sentinel Incident record.
7. Explain risk, policy decision, recommendation, and runbook guidance.
8. Demonstrate human approval and rejection path.
9. Execute approved action and show created Case.
10. Show Replay Timeline and audit trail.
11. Explain security, privacy, callout, and retention posture.
12. Capture questions, feedback, blockers, and next actions.

## 6. Required Preparation

Customer preparation:

- Confirm pilot Salesforce org.
- Confirm admin availability.
- Confirm Case object access.
- Confirm permission set assignment support.
- Confirm outbound callouts are allowed.
- Confirm no sensitive production data will be entered into test incident text.

Internal preparation:

- Confirm package/version target.
- Confirm hosted API health.
- Confirm hosted DB availability.
- Confirm sample incident scenario.
- Confirm support owner and escalation path.
- Prepare feedback notes template.

## 7. Salesforce Org Access

Required access:

- Salesforce admin access for package setup and permission assignment.
- Access to SentinelFlow app tabs and records.
- Access to Case object for approved action validation.
- Access to setup items needed for callout configuration.

Access constraints:

- Prefer sandbox or developer org first.
- Avoid production data unless explicitly approved by the customer.
- Avoid storing customer secrets in notes, screenshots, or demo artifacts.
- Record only the minimum org details needed for validation and follow-up.

## 8. Package/API Readiness Check

Package readiness:

- Release candidate: `v1.0.0-rc.1`.
- Package manifest: `manifest/package-sentinelflow-beta.xml`.
- Stable tests: 17 passing / 0 failing.
- Permission sets identified and assignable.

API readiness:

- Hosted API: `https://zentom-api.onrender.com`.
- Hosted DB available.
- Default callout mode: `REMOTE_SITE`.
- Named Credential path validated, but not default.
- Shared secret authentication configured where required.
- Error logging path available for failed callouts or execution defects.

Readiness result:

- Status: TBD.
- Owner: TBD.
- Evidence link/location: TBD.

## 9. Test Scenario List

Required scenarios:

- Open SentinelFlow app and dashboard.
- Confirm Org Health Score card loads.
- Trigger or validate test `FLOW_FAILURE` incident.
- Open created Sentinel Incident record.
- Review AI Recommendation section.
- Review Policy Decision record.
- Approve incident.
- Execute approved action.
- Confirm Case creation.
- Review Replay Timeline.
- Review audit log entries.
- Validate error logging path with a controlled failure, if appropriate.

Out-of-scope scenarios:

- New AI architecture changes.
- Agentforce production integration.
- Hosted HYBRID Ollama changes.
- Full autonomous remediation.
- Large object model changes.

## 10. Feedback Capture Plan

Feedback capture owner:

- Owner: TBD.
- Notes location: TBD.
- Follow-up review date: TBD.

Feedback categories:

- Onboarding friction.
- Trust in recommendation and policy explanation.
- Approval/rejection clarity.
- Case creation usefulness.
- Replay/audit confidence.
- Dashboard and Org Health Score usefulness.
- Security/privacy concerns.
- P0/P1/P2 issues.
- Deferred feature requests.

Issue triage:

- P0: Pilot cannot proceed or customer/org is blocked.
- P1: Core pilot workflow fails or produces incorrect result.
- P2: Significant usability, supportability, or reliability issue that should be fixed before wider beta.
- P3/P4: Capture for backlog only.

## 11. Follow-Up Actions

Immediate follow-up:

- Send customer thank-you and recap.
- Confirm open issues, questions, and owners.
- Log P0/P1/P2 issues for fix consideration.
- Record deferred feature requests separately from beta fix work.
- Confirm whether the customer is ready for install/validation or scenario execution.

Next milestone:

```text
30C - Install/validate package
```

Exit criteria for 30B:

- Pilot customer/org confirmed or clearly marked TBD.
- Demo date/time proposed or scheduled.
- Participants and owners identified.
- Required preparation documented.
- Package/API readiness checks defined.
- Test scenario list agreed.
- Feedback capture owner identified.
- Locked beta rule reaffirmed.
