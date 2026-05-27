# Production Deployment Runbook

## 1. Purpose
This runbook provides the exact, step-by-step instructions for deploying SentinelFlow `v1.0.0-rc1` into the customer's live production Salesforce environment. It ensures a zero-downtime transition and guarantees all metadata and security configurations are applied perfectly.

## 2. Pre-Deployment Checklist
- [ ] Confirm `v1.0.0-rc1` tag is finalized.
- [ ] Obtain Production Org credentials and a deployment slot (e.g., Friday 9:00 PM EST).
- [ ] Confirm Zentom Production API endpoints (`https://api.zentom.ai/v1/...`) are scaled up to handle production load.

## 3. Deployment Steps

### Step 3.1: Metadata Deployment
Deploy the `v1.0.0-rc1` package to the production org using the Salesforce CLI or Change Sets.
```bash
sfdx force:source:deploy -p force-app -u productionOrgAlias
```
*Wait for successful validation and deployment.*

### Step 3.2: Configuration & Security
1. **Named Credentials:** Update the `Zentom_API` Named Credential to point to the production URL (`https://api.zentom.ai`).
2. **Authentication:** Apply the production API keys/OAuth tokens in the secure Custom Metadata Type / Auth Provider.
3. **Remote Site Settings:** Verify `https://api.zentom.ai` is active.
4. **Permission Sets:** Assign the `SentinelFlow_Admin` and `SentinelFlow_User` permission sets to the production operations team.

## 4. Post-Deployment Verification (Smoke Tests)
- [ ] Log in as a standard Operations User.
- [ ] Open the **SentinelFlow Command Center**. Ensure the UI loads without permission errors.
- [ ] Trigger a safe, artificial `FLOW_FAILURE` (using a designated test class).
- [ ] Verify the incident routes to the Zentom API and an `aiTrace` successfully populates the `Sentinel_Incident__c` record.
- [ ] Confirm the AI Explanation Panel renders correctly.

## 5. Rollback Plan
If any step in the post-deployment verification fails, immediately execute the rollback plan:
1. Deactivate the Webhook Trigger / Flow intercepting `FLOW_FAILURE` events to sever the connection to Zentom.
2. Escalate to the Lead Salesforce Architect and CTO.
3. If necessary, execute `sfdx force:source:deploy` with the previous stable state (if upgrading from a prior version) or manually uninstall the unmanaged metadata.
