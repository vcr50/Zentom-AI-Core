# Pilot Support & Escalation Plan

## 1. Purpose
This document outlines the standard operating procedures for supporting the SentinelFlow Beta 2 pilot. It defines how issues are reported, prioritized, and resolved to ensure the pilot runs smoothly and any technical disruptions are handled immediately.

## 2. Primary Support Channels
- **Immediate Support (Slack):** A dedicated, shared Slack channel (`#sentinelflow-pilot-support`) will be used for real-time communication between the customer's operations team and our engineering/support staff.
- **Issue Tracking (Jira/Salesforce):** All non-urgent bugs, feature requests, and UI/UX feedback will be logged via our central issue tracking portal.

## 3. Severity Definitions
- **Severity 1 (Critical - P1):** The SentinelFlow app or Zentom API is completely down, blocking all incident tracking or causing severe disruption to the customer's sandbox environment.
- **Severity 2 (High - P2):** Core features (e.g., AI Explanation Panel, Command Center) are severely degraded or returning persistent errors, but the baseline incident logs are still functioning.
- **Severity 3 (Medium - P3):** Minor UI bugs, missing telemetry data in specific edge cases, or non-blocking performance degradation.
- **Severity 4 (Low - P4):** Cosmetic issues, feature requests, or documentation gaps.

## 4. Escalation Path & SLAs
| Severity | Initial Response Time | Resolution Target | Escalation Point |
|---|---|---|---|
| **P1** | < 15 Minutes | < 4 Hours | Lead Solutions Architect & CTO |
| **P2** | < 2 Hours | < 24 Hours | Senior Support Engineer |
| **P3** | < 24 Hours | Next Patch Release | Product Manager |
| **P4** | < 48 Hours | Roadmap | Product Manager |

## 5. Key Contacts
- **Technical Account Manager (TAM):** Primary point of contact for the pilot health and business-level escalations.
- **Lead Solutions Architect:** Escalation point for complex integrations and API issues.
- **Support Engineering Lead:** Escalation point for product bugs and routing.

## 6. Post-Incident RCA Process
In the event of a P1 or P2 failure during the pilot:
- Immediate mitigation will be deployed.
- A full **Root Cause Analysis (RCA)** document will be provided to the customer within 48 hours of resolution.
- Preventative patches will be prioritized for the next sprint.

## 7. Feedback Capture Loops
- **Weekly Check-ins:** 30-minute sync between our TAM and the customer's Operations Lead to review dashboard telemetry and qualitative feedback.
- **End-of-Pilot Review:** Formal presentation to measure performance against the Pilot Success Metrics (Milestone 38E) and finalize the production rollout decision.
