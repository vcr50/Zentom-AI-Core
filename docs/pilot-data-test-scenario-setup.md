# Pilot Data & Test Scenario Setup

## 1. Purpose
This document outlines the standard test data requirements and operational scenarios to be executed during the SentinelFlow Beta 2 pilot. These scenarios are designed to prove the value, safety, and operational visibility of the AI engine to the customer's operations team without relying on live production incidents.

## 2. Test Data Requirements
To successfully execute these scenarios, the following test data must be seeded or available in the pilot sandbox:
- **Test User Accounts:** Standard Salesforce User records (to trigger actions).
- **Test Accounts/Contacts:** Mock records to use during DML operations.
- **Sentinel_Error_Log__c:** Clear out any legacy test data prior to the pilot kickoff to ensure clean dashboards.

## 3. Scenario 1: Standard FLOW_FAILURE (Missing Required Field)
- **Objective:** Demonstrate Zentom AI's ability to intercept, trace, and explain a standard Flow error.
- **Steps:**
  1. Trigger an intentional `FLOW_FAILURE` by executing a test Flow that attempts to insert a record missing a required field (e.g., `OwnerId`).
  2. Open the newly created `Sentinel_Incident__c` record.
  3. **Verify:** The **Zentom AI Explanation Panel** renders and correctly identifies the missing field as the root cause with a high confidence score.

## 4. Scenario 2: Unhandled Exception in Trigger (Safe Case Creation)
- **Objective:** Demonstrate the AI's recommendation engine and seamless ITSM handover.
- **Steps:**
  1. Trigger an intentional `System.NullPointerException` inside a mock Apex trigger.
  2. Open the resulting `Sentinel_Incident__c` record.
  3. Verify the AI traces the error to the exact line of Apex code.
  4. Click the **"Create Salesforce Case"** button.
  5. **Verify:** A new native Salesforce Case is created with the AI's explanation prepopulated in the case description.

## 5. Scenario 3: Human Approval Flow
- **Objective:** Prove the core safety model (*"AI explains and recommends. Policy controls action. Human approval controls execution."*).
- **Steps:**
  1. Trigger a high-risk failure that the Zentom Engine categorizes as requiring `APPROVAL_REQUIRED`.
  2. Ensure the Incident's Orchestration Mode is set to `HYBRID`.
  3. As a Sentinel Admin, navigate to the Command Center and locate the pending approval.
  4. Manually approve or reject the action.
  5. **Verify:** The system respects the human override and updates the incident status accordingly without autonomous execution.

## 6. Scenario 4: AI Command Center Telemetry
- **Objective:** Demonstrate real-time operational visibility.
- **Steps:**
  1. Rapidly trigger 3-5 `FLOW_FAILURE` incidents to simulate a traffic spike.
  2. Open the **SentinelFlow Command Center**.
  3. **Verify:** 
     - The Live Incident Radar updates.
     - The **Zentom AI Signal** preview panel successfully displays the latest active incident's AI Status and Confidence Score.

## 7. Success Checklist
- [ ] Test data seeded in the target sandbox.
- [ ] Scenario 1 executed successfully.
- [ ] Scenario 2 executed successfully.
- [ ] Scenario 3 executed successfully.
- [ ] Scenario 4 executed successfully.
- [ ] Customer pilot users formally sign-off on the scenarios.
