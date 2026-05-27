# Pilot Security & Access Readiness

## 1. Purpose
This document ensures that all security and access controls are properly validated prior to allowing enterprise operations and architecture teams to use SentinelFlow Beta 2 during the pilot. It serves as the final security gate for the pilot org.

## 2. Data Privacy & Masking
- **Production Data:** No live production data will be used. The pilot is restricted strictly to a Partial/Full Sandbox environment.
- **Data Masking:** Ensure that any sensitive PII data inherently present in the sandbox has been anonymized or masked per enterprise security policies.
- **Incident Scope:** SentinelFlow will only track system-level `FLOW_FAILURE` logs. It does not extract or process customer PII as part of its AI trace logic.

## 3. Profiles & Permission Sets
- [ ] **SentinelFlow_Admin:** Verified that this permission set is restricted only to the core operational leads who require approval and policy-override privileges.
- [ ] **SentinelFlow_User:** Verified that general operations staff only have read/write access to incidents and read-only access to policies.
- [ ] **Salesforce FLS:** Field-Level Security verified; read/write access on `Sentinel_Incident__c` and related logs is appropriately restricted.

## 4. Integration Security
- [ ] **Zentom Backend Auth:** API calls between Salesforce and the Zentom AI Backend use secure endpoints (HTTPS).
- [ ] **Named Credentials:** API Keys are secured within Salesforce Named Credentials and never hardcoded in Apex or client-side LWC code.
- [ ] **Webhook Gateway:** The incoming webhook endpoint strictly authenticates requests to prevent unauthorized incident creation.

## 5. Network & Endpoint Constraints
- [ ] **Remote Site Settings:** Only the explicit Zentom API domain is whitelisted.
- [ ] **CORS Limitations:** SentinelFlow LWC components are strictly limited to rendering within the Salesforce trusted domains.

## 6. Audit & Governance Logging
- [ ] **Field History Tracking:** Enabled on critical fields like `Status`, `Owner`, and `Approval_Status` on `Sentinel_Incident__c`.
- [ ] **Execution Logs:** All AI reasoning traces and orchestration recommendations are natively tracked in the custom object history and `Sentinel_Error_Log__c` tables for auditability.

## 7. Operational Readiness Sign-off
- **Security Validation:** [PENDING / PASS / FAIL]
- **Sign-off By:** IT Security / Salesforce Architecture Lead
- **Date:** ___________

*Note: Achieving a PASS on this checklist is required before handing over sandbox credentials to the customer pilot team.*
