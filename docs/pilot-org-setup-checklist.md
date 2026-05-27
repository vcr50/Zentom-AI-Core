# Pilot Org Setup Checklist

## 1. Purpose
This document provides the step-by-step technical checklist to ensure the Target Pilot Sandbox environment is fully configured, connected to the Zentom API, and functionally validated for the customer pilot.

## 2. Target Pilot Org
- **Target Environment:** Enterprise full sandbox (e.g., `astrosoft`)
- **Type:** Full / Partial Copy Sandbox

## 3. Org Access Requirements
- [ ] System Administrator access granted to SentinelFlow deployment lead.
- [ ] Pilot users identified and provisioned in the sandbox.

## 4. Package Installation Checklist
- [ ] SentinelFlow Beta 2 managed/unmanaged package installed successfully.
- [ ] SentinelFlow Lightning App is visible in the App Launcher.

## 5. Permission Set Assignment
- [ ] `SentinelFlow_Admin` permission set assigned to deployment lead and Operations Managers.
- [ ] `SentinelFlow_User` permission set assigned to general pilot participants.
- [ ] Field-Level Security (FLS) for `Sentinel_Incident__c` verified.

## 6. Custom Metadata / Settings
- [ ] Verify `SentinelFlow_Config__mdt` records are appropriately seeded for the pilot org.
- [ ] Confirm Webhook Callout Mode is set to `ACTIVE`.

## 7. API Endpoint Configuration
- [ ] Zentom API URL configured in Custom Metadata or Named Credentials.

## 8. API Key / Auth Configuration
- [ ] API Key / Auth headers configured in Named Credentials (if enabled for the pilot environment).

## 9. Remote Site / Named Credential Setup
- [ ] Named Credential configured for the Zentom Backend API.
- [ ] Remote Site Settings approved and active for external API routing.

## 10. Test Incident Validation
- [ ] Trigger a test `FLOW_FAILURE` incident.
- [ ] Confirm incident is intercepted and successfully sent to the Zentom API.
- [ ] Verify `aiTrace` fields automatically populate on the `Sentinel_Incident__c` record.

## 11. Dashboard Validation
- [ ] Open the SentinelFlow Command Center.
- [ ] Verify live telemetry components load without errors.
- [ ] Verify **Command Center AI Signal preview** renders correctly for the test incident.

## 12. AI Explanation Panel Validation
- [ ] Open the `Sentinel_Incident__c` record page.
- [ ] Verify the **Zentom AI Explanation Panel** renders correctly and displays deep reasoning.

## 13. Replay Timeline Validation
- [ ] Verify the **Replay Timeline** component renders sequential logs for the test incident.

## 14. Case Creation Validation
- [ ] Click "Create Salesforce Case" from the Incident record.
- [ ] Verify a new native Salesforce Case is successfully generated and linked.

## 15. Error Logging Validation
- [ ] Introduce a deliberate integration error (e.g., bad API key).
- [ ] Verify the `Sentinel_Error_Log__c` object is accessible and accurately captures the failure.

## 16. Pilot Setup Pass/Fail Result
- **Result:** [PENDING / PASS / FAIL]
- **Sign-off:** Pilot Org is fully provisioned and passes end-to-end functionality tests, ready for user handover.
