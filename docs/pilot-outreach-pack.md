# SentinelFlow Pilot Outreach Pack

## 1. Short Product Intro

SentinelFlow helps Salesforce teams turn operational incidents into explainable, approval-gated actions.

It connects Salesforce to the hosted Zentom API, receives incident signals, scores risk, records policy decisions, recommends a runbook, supports human approval, creates safe Salesforce follow-up actions such as Cases, and preserves an audit-friendly Replay Timeline.

Current pilot focus:

- Controlled real-customer validation.
- Human approval before execution.
- Clear replay/audit evidence.
- Low-risk Salesforce workflow testing.
- Feedback before wider marketplace rollout.

Short description:

```text
SentinelFlow is a Salesforce incident intelligence and approval workflow pilot that helps teams review high-risk operational signals, understand recommended next steps, approve safe actions, and audit what happened through a replay timeline.
```

## 2. Who the Pilot Is For

The pilot is for Salesforce customers who:

- Have a Salesforce admin available for installation and validation.
- Use Salesforce Cases or want to validate safe Case creation after approval.
- Care about incident triage, operational visibility, approval controls, and auditability.
- Can start in a sandbox or developer org before production use.
- Can participate in guided onboarding and a short feedback cycle.
- Are comfortable testing a controlled pilot rather than a full marketplace release.

Best-fit pilot roles:

- Salesforce Admin.
- Operations lead.
- Support or service leader.
- Automation owner.
- Security, governance, or audit stakeholder.
- Technical evaluator.

The pilot is not intended for customers who require full autonomous remediation, production Agentforce integration, hosted HYBRID Ollama, or major custom integrations as a condition for evaluation.

## 3. What the Customer Will Test

Pilot customers will test:

- SentinelFlow package installation or deployment validation.
- Permission assignment for Admin, Approver, and Viewer roles.
- Hosted Zentom API configuration.
- Hosted API and hosted database health checks.
- A standard `FLOW_FAILURE` test incident.
- Sentinel Incident creation and hosted incident write-back.
- Risk score, risk level, policy decision, recommendation, and runbook output.
- Human approval and rejection behavior.
- Approved Salesforce Case creation.
- Replay Timeline audit evidence.
- Dashboard and Org Health Score visibility.
- Support escalation and feedback process.

Expected validation scenario:

```text
Incident type: FLOW_FAILURE
Expected risk score: 95
Expected risk level: CRITICAL
Expected policy decision: HUMAN_APPROVAL_REQUIRED
Expected runbook: FLOW_FAILURE_BASIC_RECOVERY
Expected safe action: CREATE_CASE after human approval
```

## 4. Time Required

Recommended pilot time commitment:

| Activity | Estimated time |
| --- | --- |
| Intro call or demo | 30-45 minutes |
| Pre-onboarding coordination | 15-30 minutes |
| Guided setup and validation | 60-90 minutes |
| Workflow testing | 45-60 minutes |
| Observation and feedback period | 1-2 weeks |
| Pilot review call | 30-45 minutes |

Customer time is usually concentrated in two sessions:

- Session 1: Intro/demo and pilot fit.
- Session 2: Guided setup, validation, and first feedback.

Optional follow-up sessions may be scheduled for production readiness review, issue triage, or additional stakeholder feedback.

## 5. Benefits for Pilot Customer

Pilot customer benefits:

- Early access to SentinelFlow before wider marketplace rollout.
- Guided Salesforce setup and validation support.
- A structured way to evaluate incident intelligence in a real org.
- Human-approved workflow for safe action testing.
- Replay Timeline evidence for audit and trust review.
- Opportunity to influence v1.0.1 fixes and future roadmap priorities.
- Clear support path during the pilot.
- Low-risk validation before broader rollout.

Customer-specific value to explore:

- Faster understanding of high-risk Salesforce operational signals.
- More consistent approval workflow for recommended actions.
- Better traceability from incident intake to decision and execution.
- Clearer operational review through dashboard and replay evidence.

## 6. Pilot Limitations

Pilot limitations:

- Pilot is controlled and limited in scope.
- Human approval remains required before execution.
- Full autonomous remediation is not included.
- Agentforce production integration is not included.
- Hosted HYBRID Ollama is not included.
- Major AI architecture changes are not included.
- Large object model changes are not included.
- Custom customer-specific integrations are not included unless separately approved.
- Broader marketplace rollout happens only after pilot validation.

Operational limitations:

- Hosted API availability must be validated during setup.
- Render cold starts may require retry or warm-up depending on hosting tier.
- Customer should avoid entering secrets, credentials, regulated data, or sensitive personal data in test incident text.
- Production org use should follow sandbox/developer validation unless explicitly approved by the customer.

## 7. Support Process

Pilot support process:

- Assign a SentinelFlow support owner before onboarding.
- Confirm customer Salesforce admin and escalation contact.
- Capture target org type, Org Id, callout mode, and hosted API target.
- Use the support SLA / response policy for severity handling.
- Track production-impacting issues through production issue tracking.
- Track feedback through the feedback-to-roadmap process.
- Route patch-worthy issues into v1.0.1 patch planning.

Support evidence to collect:

- Salesforce Org Id.
- Org type: sandbox, developer, or production.
- Sentinel Incident id.
- Hosted Zentom incident id, if available.
- `Sentinel_Error_Log__c` id, if available.
- Error message or screenshot with sensitive data removed.
- Replay Timeline events, if relevant.
- Steps to reproduce.
- Business impact.

Escalation guidance:

- Security, data privacy, unsafe execution, approval bypass, hosted API outage, install blocker, and core workflow failure should be escalated immediately.
- Documentation, onboarding, dashboard, replay clarity, and usability issues should be reviewed during the pilot feedback cycle unless they block validation.

## 8. Call/Demo Agenda

Suggested intro call/demo agenda:

1. Introductions and customer context.
2. Customer Salesforce environment and target org discussion.
3. SentinelFlow short product overview.
4. Pilot goal and scope.
5. Demo of incident intake, risk scoring, policy decision, recommendation, approval, Case creation, Replay Timeline, and dashboard.
6. Review of pilot limitations and safety guardrails.
7. Customer selection fit check.
8. Required customer roles and access.
9. Proposed pilot timeline.
10. Support and escalation process.
11. Feedback process.
12. Next steps and scheduling.

Demo flow:

```text
Test incident -> Risk and policy -> Recommendation and runbook -> Human approval -> Safe action -> Replay Timeline -> Dashboard
```

## 9. Follow-Up Questions

Pilot fit questions:

- Which Salesforce org should we use for the first validation: sandbox, developer, or production?
- Who is the Salesforce admin for installation and configuration?
- Who should act as the pilot approver?
- Who should review dashboard and replay evidence?
- Does your team use Salesforce Cases today?
- Is Case creation an acceptable pilot action after human approval?
- Are outbound callouts to the hosted Zentom API allowed?
- Do you prefer Remote Site or Named Credential validation for the pilot?
- Are there internal security or privacy requirements we should know before setup?
- What kind of incident or workflow would make this pilot valuable for your team?

Pilot readiness questions:

- Can you support a 60-90 minute guided setup session?
- Can you provide feedback during a 1-2 week observation period?
- What would make this pilot successful for you?
- What would block pilot success?
- Who should receive support or escalation updates?
- Are there dates or business windows we should avoid?

Feedback questions:

- Was installation clear?
- Were the permission roles understandable?
- Did the test incident output make sense?
- Did the policy decision feel explainable?
- Did the recommendation and runbook feel useful?
- Did the approval workflow match your expectations?
- Was the created Case useful and safe?
- Did Replay Timeline provide enough audit evidence?
- Was the dashboard useful for review?
- What should be improved before broader rollout?

Milestone 27B result:

```text
27B - Pilot Outreach Pack: Complete
Next - Customer-facing pilot outreach message
```
