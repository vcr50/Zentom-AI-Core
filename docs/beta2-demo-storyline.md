# Beta 2 Demo Storyline — Milestone 34B

## 1. Purpose
Define a repeatable demo script for the SentinelFlow Beta 2 presentation that walks stakeholders through the full incident governance lifecycle in under 10 minutes.

## 2. Demo Audience

| Audience | What They Care About |
|---|---|
| **CTO / VP Engineering** | Governance, risk reduction, audit trail |
| **Salesforce Admin / Architect** | Incident visibility, approval workflow, Case integration |
| **Security / Compliance Lead** | Policy enforcement, human-in-the-loop, replay evidence |
| **Product / Business Stakeholder** | Time to resolution, operational health, ROI |
| **Potential Customer / Partner** | Differentiation, platform value, roadmap |

## 3. Demo Goal
Prove that SentinelFlow transforms scattered Salesforce logs and errors into a **governed incident workflow** with risk scoring, policy enforcement, human approval, and full audit replay — all inside a single command center.

## 4. Opening Story

> *"Imagine it's Monday morning. Your Salesforce org processed 200 flows over the weekend. Three of them failed. One triggered a permission escalation. Another created duplicate records. The third silently broke a critical integration.*
>
> *You find out about it on Tuesday — from a customer complaint.*
>
> *What if your org could detect those failures, score their risk, recommend a fix, and wait for your approval — all before the customer ever noticed?"*

## 5. Problem Statement

Salesforce teams today face:

| Problem | Impact |
|---|---|
| **Scattered signals** | Errors in Setup, logs in Debug, Cases in Service — no single pane of glass |
| **No risk scoring** | All errors look the same — no way to prioritize |
| **No policy enforcement** | Anyone can fix anything, no governance trail |
| **Manual triage** | Admins spend hours searching logs, Slack threads, and emails |
| **No audit replay** | When regulators ask "what happened?", teams scramble |
| **Reactive response** | Problems are discovered by users, not by the system |

## 6. SentinelFlow Solution Story

SentinelFlow introduces a **governed incident lifecycle**:

```
Detect → Understand → Score Risk → Apply Policy → Recommend → Approve → Execute → Audit
```

| Stage | What SentinelFlow Does |
|---|---|
| **Detect** | Monitors flow failures, permission changes, deployment anomalies |
| **Understand** | Classifies incident type, maps to runbook, identifies environment |
| **Score Risk** | Assigns a 0–100 risk score with CRITICAL / HIGH / MEDIUM / LOW level |
| **Apply Policy** | Matches the incident against Zentom policy rules |
| **Recommend** | Suggests an action — Create Case, Notify Admin, Rollback Deploy |
| **Approve** | Human-in-the-loop approval before any action executes |
| **Execute** | Performs the approved action — creates a Case, sends notification |
| **Audit** | Records every step in the Flight Recorder for replay and compliance |

## 7. Demo Flow

### Scene 1 — Command Center Overview
**Action:** Open App Launcher → SentinelFlow → SentinelFlow Home
**Show:** Full dashboard — header, tower strip, health card, KPI grid
**Say:**
> *"This is the SentinelFlow Command Center. One screen shows you everything happening in your Salesforce org — health score, critical incidents, pending approvals, and system status."*

### Scene 2 — Org Health Score
**Action:** Point to the Org Health Radar card
**Show:** Score (e.g., 72/100), status badge (At Risk), reason text, meta pills
**Say:**
> *"The org health score is calculated from active incidents, pending approvals, and error rates. Right now we're at 72 — At Risk — because we have 3 critical incidents and 9 pending approvals."*

### Scene 3 — KPI Cards
**Action:** Scan across the 8 KPI cards
**Show:** Live Incidents, Critical Traffic, Awaiting Clearance, Cleared Actions, Cases Created, Failed Actions, Flight Recorder, Top Runbook
**Say:**
> *"These KPI cards give you the pulse at a glance. 12 live incidents, 3 critical, 9 awaiting human clearance, and 5 actions already executed and governed."*

### Scene 4 — Pending Approval Queue
**Action:** Scroll to the Clearance Queue panel
**Show:** Approval rows with risk badges, policy decisions, Review buttons
**Say:**
> *"This is the human-in-the-loop. Every incident that needs action comes here first. The system recommends, but a human approves. No auto-execution without governance."*

### Scene 5 — Incident Deep Dive
**Action:** Click a FLOW_FAILURE incident (e.g., INC-2025-003)
**Show:** Incident record page — type, risk score, policy decision, runbook, approval status
**Say:**
> *"Let's look at this flow failure. Risk score 92 — Critical. The policy engine says Escalate. The recommended action is Create Case. The runbook is RB-DEPLOY-ROLLBACK. But nothing happens until I approve it."*

### Scene 6 — Human Approval
**Action:** Click Review / Approve on the incident
**Show:** Approval status changing, execution result
**Say:**
> *"I approve the recommendation. SentinelFlow creates the Case, links it to the incident, and records the entire decision chain. If I reject it, that's recorded too."*

### Scene 7 — Case Creation
**Action:** Navigate to the linked Case
**Show:** Case record with incident reference, action taken, created timestamp
**Say:**
> *"The Case is created automatically with full context — incident ID, risk score, runbook, and who approved it. Your support team gets a pre-filled Case instead of a vague Slack message."*

### Scene 8 — Replay Timeline
**Action:** Scroll to the Flight Recorder section
**Show:** Timeline rows with markers, event types, decision badges, timestamps
**Say:**
> *"Every action is recorded in the Flight Recorder. When compliance asks 'who approved what, and when?' — you show them this. Full audit trail, every decision, every timestamp."*

### Scene 9 — System Health
**Action:** Point to the Tower Systems panel
**Show:** API status, DB status, error log, error count, health badge
**Say:**
> *"The system health panel monitors the operational posture of the platform itself. API status, database health, and error counts — all in one place."*

### Scene 10 — Governance Close
**Action:** Return to full dashboard view
**Show:** Complete command center
**Say:**
> *"That's the full lifecycle. Detect, score, recommend, approve, execute, audit. No scattered logs. No blind spots. No untracked changes. Just governed operations."*

## 8. Key Talking Points

| Point | One-liner |
|---|---|
| **Single pane of glass** | Everything in one command center, not 5 different Setup pages |
| **Risk scoring** | Not all errors are equal — SentinelFlow tells you which ones matter |
| **Human-in-the-loop** | AI recommends, humans approve — no autonomous execution |
| **Policy enforcement** | Every action follows a policy rule, not a guess |
| **Audit replay** | Full Flight Recorder for compliance, SOX, HIPAA, SOC 2 |
| **Case integration** | Actions create real Salesforce Cases, not just alerts |
| **Runbook mapping** | Every incident maps to a runbook — consistent response |
| **Zentom intelligence** | Future: AI-powered pattern detection, memory, and predictions |

## 9. Value Proof

| Metric | Before SentinelFlow | After SentinelFlow |
|---|---|---|
| Time to detect critical issue | Hours to days | Seconds |
| Triage time per incident | 30–60 min manual | 2 min with pre-scored risk |
| Audit trail completeness | Partial / manual | 100% automated |
| Governance evidence | Screenshots + emails | Flight Recorder replay |
| Case creation | Manual, often missed | Automatic on approval |
| Policy consistency | Ad hoc, person-dependent | Enforced by policy engine |

## 10. Closing Message

> *"Salesforce teams already have logs and errors, but they are scattered. SentinelFlow turns those signals into a governed incident workflow:*
>
> **Detect → Understand → Score Risk → Apply Policy → Recommend → Approve → Execute → Audit.**
>
> *One command center. Full governance. Complete audit trail. Ready for compliance."*

## 11. Follow-up Questions

Anticipate these from the audience:

| Question | Suggested Answer |
|---|---|
| *"Does this work with existing Salesforce data?"* | Yes — it uses standard objects (Case) and custom objects deployed via managed package. |
| *"Who controls the policy rules?"* | Admins configure policies. Zentom recommends, but policies are human-defined. |
| *"Can I customize the risk scoring?"* | Future: Zentom scoring will be configurable per incident type and org profile. |
| *"What about Slack / Teams notifications?"* | On the roadmap — Milestone 34+ will add notification channels. |
| *"Is this SOC 2 / HIPAA compliant?"* | The Flight Recorder provides full audit trail evidence. Compliance depends on org configuration. |
| *"How does this compare to Splunk / Datadog?"* | Those monitor infrastructure. SentinelFlow governs Salesforce-specific operational incidents. |
| *"What's the pricing model?"* | AppExchange managed package — pricing TBD based on org size and tier. |
