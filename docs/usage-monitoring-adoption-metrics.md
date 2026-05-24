# SentinelFlow Usage Monitoring and Adoption Metrics

## 1. Purpose

This document defines the Milestone 26D usage monitoring and adoption metrics plan for SentinelFlow v1.0.0-rc.1 and post-v1 customer rollout.

The goal is to track whether customers can install, configure, validate, use, trust, and repeatedly operate SentinelFlow after onboarding.

This plan connects product usage, Salesforce workflow usage, hosted API health, customer adoption, operational health, success signals, risk signals, and future automation.

## 2. Monitoring Scope

Monitoring scope:

- Salesforce SentinelFlow package usage.
- Sentinel Incident volume and status.
- Approval and execution workflow usage.
- Case creation from approved incidents.
- Replay Timeline availability and future usage tracking.
- Dashboard and Org Health Score usage.
- Hosted Zentom API health.
- Hosted PostgreSQL / pgvector health.
- API incident intake success/failure.
- Unauthorized and server error trends.
- Salesforce-side `Sentinel_Error_Log__c` volume.
- Render cold-start incidents.
- Customer onboarding and feedback activity.

Current measurement approach:

- Manual weekly review.
- Salesforce records and dashboard inspection.
- Hosted API health endpoints.
- Hosted API logs and error logs.
- Customer onboarding checklists.
- Production issue tracking.
- Feedback capture.

Future measurement approach:

- Automated metrics collection.
- Scheduled health snapshots.
- Customer/org-level usage summaries.
- Adoption dashboard.
- Alerting for risk thresholds.

## 3. Product Usage Metrics

Product usage metrics:

| Metric | Definition | Source | Review cadence |
| --- | --- | --- | --- |
| Sentinel Incidents created | Count of `Sentinel_Incident__c` records created in the review period. | Salesforce | Weekly |
| Critical incidents | Count of incidents with `Risk_Level__c = CRITICAL`. | Salesforce | Weekly |
| Pending approvals | Count of incidents with `Approval_Status__c = Pending Approval`. | Salesforce | Weekly |
| Approved incidents | Count of incidents with `Approval_Status__c = Approved`. | Salesforce | Weekly |
| Rejected incidents | Count of incidents with `Approval_Status__c = Rejected`. | Salesforce | Weekly |
| Executed actions | Count of incidents with `Execution_Status__c = Executed`. | Salesforce | Weekly |
| Cases created | Count of incidents with `Created_Case__c` populated, plus created Salesforce Cases with `Origin = SentinelFlow`. | Salesforce | Weekly |
| Replay timeline views/usage | Future count of Replay Timeline views or interactions. | Future instrumentation | Later |

Questions these metrics answer:

- Are customers creating real or test incidents?
- Are critical incidents being recognized?
- Are approvals happening or stalling?
- Are approved recommendations converting into safe actions?
- Are Cases being created successfully?
- Is Replay Timeline becoming part of review behavior?

## 4. Salesforce Usage Metrics

Salesforce usage metrics:

| Metric | Definition | Source | Review cadence |
| --- | --- | --- | --- |
| Active Salesforce admins | Users assigned `SentinelFlow_Admin` who participate in onboarding, setup, or issue review. | Permission assignment + onboarding evidence | Weekly during rollout |
| Active approvers | Users assigned `SentinelFlow_Approver` who approve, reject, or execute incidents. | Permission assignment + incident audit evidence | Weekly |
| Active viewers | Users assigned `SentinelFlow_Viewer` who use dashboard/replay views. | Permission assignment + future UI instrumentation | Later |
| Permission assignment completeness | Whether Admin, Approver, and Viewer roles are assigned as planned. | Onboarding checklist | Per customer |
| Test incident completion | Whether customer completed the `FLOW_FAILURE` test incident. | Onboarding checklist + Salesforce records | Per customer |
| Approval completion | Whether customer approved at least one test or real incident. | Salesforce records | Per customer/weekly |
| Execution completion | Whether customer executed Case creation from an approved incident. | Salesforce records | Per customer/weekly |
| Dashboard review usage | Whether dashboard is used during weekly/customer review. | Customer review notes | Weekly |

Key Salesforce adoption signal:

```text
Customer can move from incident intake -> approval -> Case creation -> replay review without Tomcodex/Zentom intervention.
```

## 5. Hosted API Metrics

Hosted API metrics:

| Metric | Definition | Source | Review cadence |
| --- | --- | --- | --- |
| API health status | Result of `GET https://zentom-api.onrender.com/`. | Hosted API health endpoint | Weekly/manual, later automated |
| `/api/health/db` status | DB health result including database type, configuration, missing tables, and pgvector status. | Hosted API DB health endpoint | Weekly/manual, later automated |
| Incident intake success count | Count of successful `POST /api/incidents/receive` requests. | Hosted API logs / future metrics | Weekly |
| Incident intake failure count | Count of failed incident intake attempts. | Hosted API logs / API error logs | Weekly |
| 401 unauthorized count | Count of unauthorized API requests. | Hosted API error logs | Weekly |
| 5xx error count | Count of server-side hosted API errors. | Hosted API logs / API error logs | Weekly |
| Average response time | Average hosted API response time. | Future instrumentation | Later |

Hosted API review checks:

- [ ] API health returns running status.
- [ ] DB health returns `status = ok`.
- [ ] DB health returns `databaseType = postgresql`.
- [ ] DB health returns `missingTables = []`.
- [ ] pgvector is enabled.
- [ ] 401 trend is reviewed for misconfiguration or suspicious access.
- [ ] 5xx trend is reviewed for stability issues.
- [ ] Incident intake failures are mapped to production issues when customer-impacting.

## 6. Customer Adoption Metrics

Customer adoption metrics:

| Metric | Definition | Source | Review cadence |
| --- | --- | --- | --- |
| Customers completing onboarding | Count of customers who pass the onboarding checklist. | `docs/customer-onboarding-checklist.md` evidence | Weekly |
| Active Salesforce admins | Number of customer admins participating in setup/review. | Onboarding/support records | Weekly |
| Active approvers | Number of approvers who use approval/execution workflow. | Salesforce audit/incident records | Weekly |
| Beta test scenarios completed | Count of completed beta/customer validation scenarios. | Beta testing/customer onboarding evidence | Weekly |
| Feedback items submitted | Count of bug reports, setup questions, feature requests, and feedback items. | Feedback capture / issue tracker | Weekly |
| Customers with no open P0/P1 blockers | Count and percentage of onboarded customers without critical blockers. | Production issue tracking | Weekly |
| Customers using dashboard in review | Count of customers using dashboard during review calls. | Customer review notes | Weekly |
| Customers trusting replay timeline | Count of customers who confirm Replay Timeline is useful/trusted. | Feedback capture | Weekly/monthly |

Adoption categories:

- Not started.
- Onboarding scheduled.
- Installed.
- Configured.
- Test incident passed.
- Approval/execution passed.
- Go-live ready.
- Active early customer.
- Blocked.

## 7. Operational Health Metrics

Operational health metrics:

| Metric | Definition | Source | Review cadence |
| --- | --- | --- | --- |
| Org Health Score | Current dashboard Org Health Score for customer org. | SentinelFlow dashboard | Weekly |
| Open critical incidents | Count of open CRITICAL Sentinel Incidents. | Salesforce | Weekly |
| Error log count | Count of `Sentinel_Error_Log__c` records in review period. | Salesforce | Weekly |
| Render cold-start incidents | Count of support/issues attributed to Render cold start. | Issue tracker/support notes | Weekly |
| Open P0/P1 blockers | Count of open high-severity issues. | Production issue tracking | Weekly/immediate |
| Aging pending approvals | Pending approvals older than agreed review window. | Salesforce | Weekly |
| Failed executions | Incidents with `Execution_Status__c = Failed`. | Salesforce | Weekly |
| Missing replay events | Incidents missing expected replay events. | Replay Timeline/Salesforce audit logs | Weekly |

Operational thresholds to review:

- Any open P0.
- Any open P1 older than target response/workaround window.
- Repeated 5xx API errors.
- Repeated Salesforce callout failures.
- More than one onboarding blocked by the same issue.
- Pending approvals aging without action.
- Error log count increasing without corresponding triage.

## 8. Weekly Review Dashboard

Weekly review dashboard should include:

```text
Week:
Reviewer:
Customers reviewed:
New customers onboarded:
Customers blocked:
Open P0:
Open P1:
Open P2:
Sentinel Incidents created:
Critical incidents:
Pending approvals:
Approved incidents:
Rejected incidents:
Executed actions:
Cases created:
API health:
DB health:
401 unauthorized count:
5xx error count:
Error log count:
Render cold-start incidents:
Feedback items submitted:
Patch candidates:
Roadmap candidates:
```

Weekly review questions:

- Are customers able to install without help?
- Are test incidents passing?
- Are approvals happening promptly?
- Are approved incidents producing Cases?
- Are customers using dashboard/replay in review?
- Are P0/P1 issues open?
- Are repeated support patterns emerging?
- Are any issues candidates for v1.0.1?
- Are any feedback items ready for roadmap review?

## 9. Success Signals

Success signals:

- Customer can install package without help.
- Customer can complete onboarding checklist.
- Test incident works.
- `FLOW_FAILURE` produces risk `95` and `CRITICAL`.
- Policy decision is `HUMAN_APPROVAL_REQUIRED`.
- Runbook is `FLOW_FAILURE_BASIC_RECOVERY`.
- Approval and execution work.
- Salesforce Case is created with `Origin = SentinelFlow`.
- Replay Timeline is trusted.
- Dashboard is used during review.
- Org Health Score is visible and understood.
- No P0/P1 blockers open.
- Customers submit actionable feedback.
- Customers can explain policy decision and approval workflow.
- Support questions decrease after onboarding.

Adoption success threshold for early rollout:

```text
Customer reaches go-live ready state with no open P0/P1 blockers and can complete incident -> approval -> Case -> replay/dashboard review.
```

## 10. Risk Signals

Risk signals:

- Repeated API callout failures.
- Repeated `/api/health/db` failures.
- Many pending approvals not acted on.
- High error log count.
- Render cold-start confusion.
- Customers do not understand policy decision.
- Dashboard/replay not being used.
- Replay Timeline missing expected events.
- Dashboard or Org Health Score not trusted.
- Cases not being created after approval.
- Approvers do not know when to approve/reject.
- Viewers cannot access expected read-only views.
- Multiple customers hit the same setup issue.
- P0/P1 blockers remain open.
- P2 issues age without owner or workaround.

Risk response:

- Convert repeated risk signals into production issues.
- Escalate P0/P1 signals immediately.
- Add documentation fixes for repeated setup questions.
- Map repeated P2 patterns to v1.0.1 patch candidates.
- Route product confusion to 26E Feedback-to-Roadmap Process.

## 11. Future Automation Plan

Future automation:

- Add scheduled API health snapshot.
- Add scheduled `/api/health/db` snapshot.
- Add hosted API request counters.
- Add incident intake success/failure counters.
- Add 401 unauthorized counter.
- Add 5xx error counter.
- Add average response time tracking.
- Add dashboard view/replay view instrumentation.
- Add customer/org-level adoption summary.
- Add weekly metrics export.
- Add alerting for repeated callout failures.
- Add alerting for high `Sentinel_Error_Log__c` volume.
- Add alerting for aging pending approvals.
- Add alerting for failed executions.
- Add adoption dashboard for customer success review.

Future data model options:

- Salesforce scheduled job writes daily health records.
- Hosted API writes daily metrics summaries.
- Admin dashboard displays usage and adoption trends.
- Customer success tracker stores onboarding stage and blockers.
- Patch planning dashboard links metrics to v1.0.1 candidates.

Automation priority:

1. API and DB health snapshots.
2. Incident intake success/failure counters.
3. Error log and 5xx trend tracking.
4. Pending approval aging.
5. Dashboard/replay usage instrumentation.
6. Customer adoption dashboard.
