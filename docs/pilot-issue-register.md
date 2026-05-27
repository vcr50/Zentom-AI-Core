# Pilot Issue & Incident Register

## 1. Purpose
This document serves as the master tracking log for any technical defects, outages, or functional gaps discovered during the SentinelFlow Beta 2 Pilot. Adhering to the CTO's directive, only real pilot issues (P0/P1/P2) will be addressed with hotfixes. All other feedback will be deferred to the GA roadmap.

## 2. Intake Process
Issues will be aggregated daily from the following sources:
1. `#sentinelflow-pilot-support` Slack channel escalations.
2. Direct customer reports via Jira / Email.
3. Exceptions caught by the `Sentinel_Error_Log__c` object.
4. Anomalies discovered during the internal *Daily Monitoring Log* (Milestone 40A) routine.

## 3. Triage Protocol
Upon logging an issue, the Technical Account Manager (TAM) and Support Lead will triage it according to the Severity Definitions established in the Support & Escalation Plan (Milestone 38F):
- **P1 (Critical):** Immediate engineering intervention. Full blocker.
- **P2 (High):** Degraded core functionality. Prioritized for the next patch.
- **P3 (Medium):** Minor bugs. Logged for review at the end of the pilot.
- **P4 (Low):** Feature requests/cosmetic changes. Deferred to Post-Pilot Roadmap.

## 4. The Register
*Track all discovered issues below.*

| Issue ID | Date Logged | Severity | Component | Description | Status | Resolution / PR |
|---|---|---|---|---|---|---|
| PILOT-001 | | | | | Open / In Progress / Resolved / Deferred | |
| PILOT-002 | | | | | Open / In Progress / Resolved / Deferred | |
| PILOT-003 | | | | | Open / In Progress / Resolved / Deferred | |

## 5. Decision Gates
- **Fix Now (Hotfix):** P1 and P2 issues that block pilot success metrics or severely damage trust in the AI reasoning.
- **Defer to GA:** P3 and P4 issues that are non-blocking or represent scope creep.
