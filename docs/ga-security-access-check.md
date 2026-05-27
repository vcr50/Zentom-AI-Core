# GA Security & Access Final Check

## 1. Purpose
This document provides the final security validation checklist required before the production deployment. It ensures that the transition from the sandbox (Beta 2) to the live production environment does not introduce any data privacy violations or unauthorized access.

## 2. Production Authentication
- [ ] **API Keys/OAuth:** Confirm that production-grade API keys have been provisioned for the Zentom API, distinct from the keys used during the sandbox pilot.
- [ ] **Named Credentials:** Verify the Named Credential uses the production endpoint and secure authentication protocols (OAuth 2.0 or secure JWT).

## 3. Data Privacy & Compliance
- [ ] **PII Masking:** Confirm that the payload construction logic stripping Personally Identifiable Information (PII) before sending data to the Zentom API is fully active and validated.
- [ ] **Data Residency:** Confirm that the production Zentom API endpoints comply with the customer's data residency requirements (e.g., US-East vs. EU-West).

## 4. Field-Level Security (FLS) & Permission Sets
- [ ] **`SentinelFlow_User`:** Verify standard users only have READ access to `Sentinel_Incident__c` and `Sentinel_Error_Log__c`.
- [ ] **`SentinelFlow_Admin`:** Verify admins have full CRUD access, plus the system permissions required to execute the Human Approval workflow overrides.
- [ ] Verify that internal Salesforce logic prevents non-admins from altering the `AI_Confidence_Score__c` or `AI_Status__c` fields.

## 5. Audit Trails
- [ ] Verify that Salesforce Field History Tracking is enabled on the `Sentinel_Incident__c` object for the `AI_Status__c` and `Resolution_Action__c` fields to maintain a strict audit log of human overrides.

## 6. Sign-off
- **Lead Security Architect:** ____________________ Date: _________
- **Lead Salesforce Admin:** ____________________ Date: _________
