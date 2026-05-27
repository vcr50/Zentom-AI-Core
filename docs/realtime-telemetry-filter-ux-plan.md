# Realtime Telemetry & Dashboard Filter UX Plan

## 1. Purpose
This document outlines the strategy for upgrading the SentinelFlow Command Center dashboard to provide near-realtime telemetry and an intuitive filter UX. The goal is to make the dashboard feel active and live, improving enterprise trust without over-engineering full event-streaming at this beta stage.

## 2. Customer Feedback Addressed
During the May 27, 2026 demo (Milestone 35), Enterprise Operations Leaders and Salesforce Architects provided the following P2 feedback:
- **Telemetry Gap:** Some dashboard sections lacked live telemetry and trends (e.g., AI confidence, critical incident spikes).
- **Filter UX:** Dashboard filters need better clarity and ease of use.
- **Incomplete Feel:** Modules displaying "Coming Soon" made the platform feel partially incomplete.

## 3. Current Dashboard Telemetry
The dashboard currently provides:
- Live Incident Radar (Critical traffic, open incidents)
- Approval Clearance Queue (Pending approvals)
- Executed Actions & Cases Created
- Flight Recorder (Replay events)
- Zentom Engine AI Signal Preview
- Basic Date Range filtering (Today, Last 7 Days, All)

## 4. Near-Realtime Telemetry Strategy
Rather than implementing heavy WebSockets or Platform Events for full streaming right now, we will employ a **Near-Realtime** approach:
- **Periodic Polling/Refresh:** Ensure lightning components can auto-refresh at defined intervals or make manual refresh highly responsive.
- **Trend Indicators:** Add visual trend metrics (e.g., "+5% since yesterday") next to KPIs for Incident Volume, Critical Incidents, and AI Confidence.
- **Health Indicators:** Display live API/system health statuses distinctly.

## 5. Filter UX Strategy
Filters must be obvious and simple. We will upgrade the filtering mechanism to include:
- **Time Range:** Today / 7 Days / 30 Days (expanding from the current implementation)
- **Environment:** Production / Sandbox / All
- **Risk Level:** Critical / High / Medium / Low / All
- **Status:** Approval Required / Executed / Open / Closed / All

*Note: For the beta, if backend query support is limited, these filters will be implemented at the UI-level by filtering the cached dataset in the LWC.*

## 6. Data Freshness Indicators
To directly help the customer understand whether the dashboard is live or static, we will enhance the existing header:
- **Last refreshed:** `10:42 AM`
- **Data mode:** `Near realtime`
- **Manual Refresh Button:** Highly visible and responsive.

## 7. Placeholder Reduction Plan
Where live data or specific modules are not yet ready, we will strictly avoid "Coming Soon." Instead, we will use intentional, professional wording:
- *Telemetry mapping ready*
- *Live signal connection planned*
- *No data available for selected filter*

This ensures the product feels intentional and production-oriented.

## 8. Future Realtime Architecture
Post-beta, we will transition to a fully live streaming architecture:
- **Salesforce Platform Events / Change Data Capture (CDC):** Push real-time state changes from the backend to the LWC layer.
- **Zentom Engine Webhook to Event Bus:** Direct streaming of AI reasoning traces and log metrics without polling.

## 9. Validation Checklist
- [ ] Telemetry trend sections (Incidents, Critical, Approvals, AI Confidence) are visually defined.
- [ ] Filter UX (Time, Environment, Risk, Status) is mocked or implemented.
- [ ] "Data freshness" indicator clearly states "Near realtime" with a timestamp.
- [ ] All "Coming Soon" placeholders are replaced with intentional messaging.

## 10. Success Criteria
- The dashboard feels "alive" and actively monitoring.
- Users can clearly see what data is fresh and how to manipulate views via intuitive filters.
- There is no perception of an incomplete or placeholder-heavy product.
