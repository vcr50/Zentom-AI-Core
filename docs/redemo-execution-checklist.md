# Re-demo Execution Checklist

## 1. Purpose
This checklist serves as the definitive runbook for the re-demo with the Enterprise Operations and Salesforce Architecture teams. Its primary purpose is to secure the Conditional GO validation for the SentinelFlow pilot.

## 2. Re-demo Objective
Prove that the P1 concern ("Zentom AI is not visibly functioning during workflow execution") is unequivocally resolved, demonstrating that Zentom AI is an active, transparent, and safely governed neural layer.

## 3. Demo Environment
- **Salesforce Org:** `astrosoft` (Target Sandbox)
- **Zentom Backend:** Local / Staging Python API (Running and actively serving requests)
- **App Version:** SentinelFlow Beta 2 (with Milestone 36 updates)

## 4. Required Test Incident
- **Type:** `FLOW_FAILURE`
- **Context:** Simulate a critical production flow failure to trigger the AI engine's deep analysis pipeline.

## 5. AI Visibility Checks
- [ ] Show the Zentom API logs returning the `aiTrace` object.
- [ ] Verify that `aiTrace` fields (Status, Confidence, Mode, Explanations) are successfully persisted on the `Sentinel_Incident__c` record in Salesforce.

## 6. Incident Page Checks
- [ ] Open the newly created Sentinel Incident record.
- [ ] Show the **Zentom AI Explanation Panel** at the top of the layout.
- [ ] Explicitly point out the populated fields:
  - AI Status (ACTIVE)
  - Confidence Score
  - Orchestration Mode
  - AI Explanation
  - Risk Reason
  - Policy Reason
  - Runbook Reason

## 7. Command Center Checks
- [ ] Open the **SentinelFlow Command Center** dashboard.
- [ ] Point out the **Zentom AI Signal** preview panel.
- [ ] Demonstrate that the dashboard successfully highlights the latest active AI signal from the incident without requiring a drill-down.
- [ ] Click "View Full AI Trace" to verify navigation back to the incident record.

## 8. Safety/Governance Explanation
While demonstrating the UI, explicitly state the platform's core governance model:
> *"AI explains and recommends. Policy controls action. Human approval controls execution."*

## 9. Customer Validation Questions
Pause and ask the architecture team:
- Does this level of AI visibility provide the operational trust required for a production pilot?
- Is the separation between AI recommendation and human/policy execution clear?

## 10. Pass/Fail Criteria
- **Pass:** The customer confirms that the AI feels "alive" and the governance model is transparent, granting a Conditional GO for the pilot.
- **Fail:** The customer requests further visibility or raises new P1 objections regarding the safety or transparency of the AI engine.
