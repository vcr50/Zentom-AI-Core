# Demo Session Checklist — Milestone 35B

## 1. Purpose
Ensure every live customer demo of SentinelFlow Beta 2 goes smoothly by verifying the environment, data, assets, and backup plans prior to the call.

## 2. Pre-Demo Setup
- [ ] Schedule confirmed with customer.
- [ ] Roles assigned (Presenter, Demo Engineer, Note Taker).
- [ ] Presentation slide deck loaded and reviewed.
- [ ] Browser window cleaned (no bookmarks bar, no extra extensions).
- [ ] Zoom level set to 100%.

## 3. Salesforce Org Readiness
- [ ] Logged into `astrosoft` Beta Sandbox.
- [ ] SentinelFlow app opens without errors.
- [ ] Command Center dashboard loads instantly.
- [ ] No real customer data visible anywhere in the org.

## 4. Hosted API Readiness
- [ ] Hosted API health check passes.
- [ ] Network tab confirms fast load times for components.

## 5. Demo Data Readiness
- [ ] 2-3 mock `Sentinel_Incident__c` records created (CRITICAL and HIGH).
- [ ] Pending Approval Queue has at least one incident ready for Review.
- [ ] Risk, policy, and runbook values are visibly populated.
- [ ] Error logs are populated in `Sentinel_Error_Log__c`.
- [ ] Flight Recorder has recent audit events.

## 6. Screenshot/Presentation Readiness
- [ ] Slide deck is open and ready to screen share.
- [ ] Backup screenshots (`docs/screenshots/beta2/`) are accessible locally in case of internet/org failure.

## 7. Live Demo Flow Checklist (Must-Check Before Demo)
- [ ] Dashboard text readable and styled correctly.
- [ ] KPI cards and System Health panels are visible.
- [ ] Test incident flow works end-to-end.
- [ ] Approval flow works (clicking Review changes status).
- [ ] Case creation works automatically upon approval.
- [ ] Replay timeline updates correctly.

## 8. Backup Plan
- **Primary:** Live driving in `astrosoft` org.
- **Secondary:** Fallback to the Beta 2 Screenshot Pack if the org is slow or inaccessible.
- **Tertiary:** Fallback to Slide Deck only.

## 9. Feedback Capture Checklist
- [ ] Note Taker has the Feedback Capture template ready.
- [ ] Prepared to record UI/UX feedback.
- [ ] Prepared to record Feature Gaps (P0/P1/P2).
- [ ] Prepared to record Security / Compliance questions.
- [ ] Prepared to record Integration requests.

## 10. Post-Demo Actions
- [ ] Send Beta 2 Feature Summary PDF.
- [ ] Send Technical Architecture Diagram.
- [ ] Schedule Pilot program follow-up call.
- [ ] Add feedback into the Milestone 36 product backlog.
