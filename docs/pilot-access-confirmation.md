# Pilot Access Confirmation

## 1. Purpose
This document serves as the formal verification that all necessary user and system access rights have been successfully provisioned for the SentinelFlow pilot. It ensures that both internal support engineers and customer pilot participants can securely interact with the platform.

## 2. Scope of Access
Access is strictly limited to the `astrosoft` Sandbox environment. No production data or production Salesforce credentials are to be used during this phase.

## 3. Provisioning Checklist

### Customer Access
- [ ] **Pilot Admins:** Confirmed receipt of login credentials and successful assignment of the `SentinelFlow_Admin` permission set.
- [ ] **Operations Users:** Confirmed receipt of login credentials and successful assignment of the `SentinelFlow_User` permission set.

### Internal Support Access
- [ ] **TAM & Support Engineers:** Granted read-only sandbox access to assist with debugging and monitoring telemetry without the ability to modify policies or execute approvals.

## 4. External Connectivity
- [ ] **Zentom Backend:** API Key and Named Credentials are confirmed active. The backend is successfully receiving standard POST payloads from the sandbox.
- [ ] **Webhook Gateway:** The Salesforce endpoint is successfully capturing external trigger events.

## 5. Slack Connectivity
- [ ] **Support Channel:** The dedicated `#sentinelflow-pilot-support` Slack channel is active.
- [ ] **Member Invites:** All key customer stakeholders (Operations Leaders, Architects) and internal TAMs/engineers have successfully joined the channel.

## 6. End-User Communication
- [ ] Welcome email sent to all pilot participants outlining login steps, providing a link to the Command Center, and sharing the support Slack channel details.

## 7. Sign-off
**Access Validation:** [PASS]
All pilot users and systems are confirmed active and securely connected.
