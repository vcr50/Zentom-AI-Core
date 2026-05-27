# Pilot Usage & Adoption Review

## 1. Purpose
This document provides a framework to measure how actively the customer operations team is engaging with SentinelFlow Beta 2. It helps us differentiate between technical stability (the app works) and operational adoption (the users actually use it).

## 2. Usage Metrics to Track
At the mid-point and end of the pilot, we will extract the following data:
- **Active Pilot Users:** Number of unique Salesforce users who have opened the Command Center.
- **Incident Interventions:** The percentage of `FLOW_FAILURE` incidents where a user explicitly viewed the AI Explanation Panel.
- **Approval Engagement:** The time taken for an admin to respond (approve/reject) to a `HYBRID` mode orchestration recommendation.
- **Case Generation Usage:** How many times the "Create Salesforce Case" button was utilized from the incident UI.

## 3. Potential Adoption Barriers
*Track observed friction points that prevent users from adopting the tool:*
- **Trust Deficit:** Users ignoring AI insights due to early inaccurate traces (Hallucinations).
- **UX Friction:** Dashboard is too slow to load, or the AI explanation requires too many clicks to find.
- **Process Misalignment:** The operations team is still relying on legacy Salesforce setup audit trails out of habit.

## 4. Intervention Strategies
If adoption metrics are lagging by the mid-point of the pilot, the TAM will execute the following interventions:
- **Re-education Sync:** A 15-minute screen-share to remind users of the Day-1 workflows.
- **Direct Feedback Solicitation:** Ask specific users *why* they bypassed SentinelFlow for a particular incident.
- **Configuration Tweaks:** Adjusting dashboard filters or layout to make critical data more prominent based on user feedback.
