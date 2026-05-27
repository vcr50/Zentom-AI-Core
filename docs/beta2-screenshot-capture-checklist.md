# Beta 2 Screenshot Capture Checklist — Milestone 34A

## 1. Purpose
Define the full set of screenshots needed for the Beta 2 customer presentation pack. Ensure every capture uses safe demo data, follows naming conventions, and passes a privacy/security check before inclusion.

## 2. Screenshot Rules

- ✅ Use only demo/sample data
- ✅ Capture from the polished Milestone 33 UI
- ✅ Use consistent browser zoom (100%)
- ✅ Use a clean browser window (no bookmarks bar, no extensions visible)
- ✅ Capture full-width where possible (1440px+ viewport recommended)
- ❌ No real customer data
- ❌ No secrets or tokens
- ❌ No API keys
- ❌ No personal information (names, emails, phone numbers)
- ❌ No internal Salesforce org IDs visible in URL bar
- ❌ No browser tabs showing unrelated content

## 3. Required Screenshots

| # | Screen | What to Capture | Priority |
|---|---|---|---|
| 1 | **Full Dashboard** | SentinelFlow Command Center — complete view including header, tower strip, health card, KPI grid, panels | P0 |
| 2 | **Org Health Score + KPI Cards** | Close-up of the health card (score, status, reason, meta pills) and the 8-card KPI grid | P0 |
| 3 | **Pending Approval Queue** | Clearance Queue panel with approval rows, risk badges, policy decisions, Review buttons | P0 |
| 4 | **Recent Incidents Table** | Live Traffic Board table with all 9 columns populated — Incident, Type, Environment, Risk, Policy, Status, Runbook, Approval, Created | P0 |
| 5 | **Replay Timeline** | Flight Recorder section showing audit events with timeline markers, decision badges, timestamps | P1 |
| 6 | **System Health / Error Logs** | Tower Systems panel showing API status, DB status, error log, error count, health badge | P1 |
| 7 | **Actions Placeholder** | Cleared Actions + Case Outcomes panels — show either populated rows or the polished empty state | P1 |
| 8 | **Experience Cloud Shell** | sentinelFlowBetaAppShell — sidebar, topbar, dark/light mode, glassmorphic cards | P1 |
| 9 | **Sidebar Navigation** | Close-up of the sidebar menu showing all nav items with icons and active state | P2 |
| 10 | **Mobile / Responsive View** | Dashboard at ≤760px showing stacked single-column layout | P2 |

## 4. Sample Data Rules

### Safe to Show
- Incident names: `INC-2025-001`, `INC-2025-002`, etc.
- Approval IDs: `APR-2025-001`, `APR-2025-002`, etc.
- Risk levels: CRITICAL, HIGH, MEDIUM, LOW
- Risk scores: numeric values (e.g., 92, 78, 45)
- Policy decisions: Escalate, Monitor, Auto-Approve
- Runbook keys: `RB-DEPLOY-ROLLBACK`, `RB-PERMISSION-AUDIT`, etc.
- Status values: Approval Required, Executed, Monitoring
- Execution actions: Create Case, Notify Admin, Rollback Deploy
- Timestamps: Any reasonable date/time
- Org health score: 0–100

### Never Show
- Real usernames or email addresses
- Salesforce org IDs (00D...)
- Session tokens or SIDs
- API keys or Named Credential values
- Real IP addresses
- Internal URLs beyond the app domain
- Browser autocomplete suggestions containing PII

## 5. Privacy / Security Check

Before including any screenshot in the presentation pack, verify:

| Check | Pass? |
|---|---|
| No real names visible | ☐ |
| No email addresses visible | ☐ |
| No org IDs in URL bar | ☐ |
| No session tokens visible | ☐ |
| No API keys or secrets | ☐ |
| No browser extensions showing PII | ☐ |
| No unrelated browser tabs visible | ☐ |
| Only demo/sample data in tables | ☐ |
| Only demo/sample data in cards | ☐ |
| Screenshot is from the polished 33B UI | ☐ |

## 6. Screenshot Naming Convention

Format: `beta2-XX-description.png`

| # | Filename |
|---|---|
| 1 | `beta2-01-full-dashboard.png` |
| 2 | `beta2-02-health-kpi-cards.png` |
| 3 | `beta2-03-pending-approvals.png` |
| 4 | `beta2-04-recent-incidents.png` |
| 5 | `beta2-05-replay-timeline.png` |
| 6 | `beta2-06-system-health.png` |
| 7 | `beta2-07-actions-placeholder.png` |
| 8 | `beta2-08-experience-shell.png` |
| 9 | `beta2-09-sidebar-nav.png` |
| 10 | `beta2-10-responsive-mobile.png` |

Storage path: `docs/screenshots/beta2/`

## 7. Capture Checklist

| # | Screenshot | Captured? | Privacy Check? | Final? |
|---|---|---|---|---|
| 1 | Full Dashboard | ☐ | ☐ | ☐ |
| 2 | Org Health + KPI Cards | ☐ | ☐ | ☐ |
| 3 | Pending Approval Queue | ☐ | ☐ | ☐ |
| 4 | Recent Incidents Table | ☐ | ☐ | ☐ |
| 5 | Replay Timeline | ☐ | ☐ | ☐ |
| 6 | System Health / Error Logs | ☐ | ☐ | ☐ |
| 7 | Actions Placeholder | ☐ | ☐ | ☐ |
| 8 | Experience Cloud Shell | ☐ | ☐ | ☐ |
| 9 | Sidebar Navigation | ☐ | ☐ | ☐ |
| 10 | Mobile / Responsive View | ☐ | ☐ | ☐ |

## 8. Final Readiness Status

| Criteria | Status |
|---|---|
| All P0 screenshots captured | ☐ Pending |
| All P1 screenshots captured | ☐ Pending |
| All privacy checks passed | ☐ Pending |
| Files saved with correct naming | ☐ Pending |
| Files stored in `docs/screenshots/beta2/` | ☐ Pending |
| Ready for 34B Demo Storyline | ☐ Pending |
