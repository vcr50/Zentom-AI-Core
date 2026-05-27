# Pilot Daily Monitoring Log

## 1. Purpose
This document provides the daily operational checklist used during the SentinelFlow Beta 2 Pilot. It ensures that internal support teams systematically verify the health of the API, the Salesforce application, and the AI incident flows every single day without waiting for customer reports.

## 2. Pilot Status
**Status:** [LIVE / PAUSED / CONCLUDED]

## 3. Date / Monitoring Window
**Date:** [YYYY-MM-DD]
**Window:** [Morning / Evening / Ad-hoc]

## 4. Environment Checked
**Target Org:** `astrosoft` Sandbox

## Daily Check Items

### 5. Hosted API Status
- [ ] Zentom API is healthy (Endpoint returns 200 OK).
- [ ] API latency is within acceptable thresholds (< 2000ms).

### 6. Salesforce App Status
- [ ] SentinelFlow app opens successfully without permission errors.
- [ ] Command Center dashboard loads and Live Incident Radar is active.

### 7. Incident Flow Status
- [ ] Test/real `FLOW_FAILURE` incidents are being successfully intercepted.
- [ ] Incidents are routing to the Zentom API without callout exceptions.

### 8. AI Trace Status
- [ ] `aiTrace` reasoning object appears in the backend API response.
- [ ] `Sentinel_Incident__c` fields (Confidence, AI Status, Runbook Reason) are populating.
- [ ] Zentom AI Explanation Panel renders correctly on the Incident record page.
- [ ] Command Center AI Signal preview renders the latest active incident.

### 9. Approval / Case Creation Status
- [ ] Human Approval flow accurately blocks autonomous execution and updates status upon override.
- [ ] "Create Salesforce Case" button accurately generates a native case with prepopulated AI details.

### 10. Replay Timeline Status
- [ ] Replay timeline visually tracks the sequential logs for handled incidents.

## 11. Issues Observed
- **P0/P1 Issues:** [None / Detail issue]
- **Governor Limit Warnings:** [None / Detail issue]
- **Other Bugs:** [List any P2/P3 bugs discovered]

## 12. Customer Feedback Notes
- *Note any unstructured feedback gathered from the Slack channel today.*

## 13. Next Action
- [ ] Continue monitoring.
- [ ] Escalate observed bugs to the Patch Queue (Milestone 40E).
