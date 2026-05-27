# Pilot Day-1 Execution Checklist

## 1. Purpose
This document provides the step-by-step runbook for the very first day of the SentinelFlow Beta 2 Pilot. It ensures that the initial customer experience is flawless, tightly supervised, and immediately proves the platform's value.

## 2. Morning Health Check (Internal Team)
- [ ] **API Status:** Verify the Zentom backend is online and latency is within normal limits (<2000ms).
- [ ] **Salesforce Webhook:** Trigger a hidden synthetic `FLOW_FAILURE` to ensure the Salesforce gateway is intercepting and routing payloads successfully.
- [ ] **Slack:** Confirm the `#sentinelflow-pilot-support` channel is monitored by the on-call engineer.

## 3. Customer Login & Sandbox Setup
- [ ] **Login Verification:** Have the primary Customer Pilot Admin log into the `astrosoft` Sandbox.
- [ ] **App Navigation:** Ensure the user can locate and open the "SentinelFlow" Lightning App.
- [ ] **Command Center Initialization:** Verify the Command Center dashboard loads without component errors.

## 4. Supervised Scenario Execution
During the first hour of the pilot, execute the following actions alongside the customer:
- [ ] **Trigger a Failure:** The customer manually triggers the predefined "Missing Required Field" Flow error (from Milestone 38D).
- [ ] **Dashboard Validation:** Refresh the Command Center and watch the Live Incident Radar update.
- [ ] **AI Preview Validation:** Confirm the Zentom AI Signal preview identifies the new incident and populates a confidence score.
- [ ] **Deep Trace Validation:** Click into the `Sentinel_Incident__c` record and review the Zentom AI Explanation Panel. Confirm the customer understands the root cause breakdown.
- [ ] **Approval Workflow:** Trigger a high-risk failure, navigate to the Command Center, and have the customer manually "Approve" the AI's mitigation recommendation.

## 5. End of Day 1 Review
- [ ] **CSAT Pulse Check:** Ask the customer: *"Did the AI accurately identify the issues you triggered today?"*
- [ ] **Support Review:** Verify zero unhandled exceptions or governor limit warnings in `Sentinel_Error_Log__c`.
- [ ] **Sign-off:** Customer formally agrees that Day 1 scenarios have passed.

## 6. Next Steps
- Hand the reins to the customer to operate the system asynchronously for the remainder of the pilot week.
- Begin capturing metrics for the Pilot Monitoring Log (Milestone 39E).
