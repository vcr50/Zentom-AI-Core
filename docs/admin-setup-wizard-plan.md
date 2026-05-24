# SentinelFlow Admin Setup Wizard Plan

## Purpose

The SentinelFlow Admin Setup Wizard should guide a Salesforce admin through the minimum steps required to configure and verify SentinelFlow after package installation.

For beta, this milestone is a planning document only. The actual wizard build is deferred to a later milestone, likely Milestone 21 or v1.0 preparation.

## Beta Decision

Milestone 19D scope:

```text
Planning document only
```

Future build scope:

```text
LWC: sentinelflowSetupWizard
Apex: SentinelFlowSetupController
Config source: Zentom_Setting__mdt
```

## Wizard Flow

The setup wizard should guide the admin through:

1. Confirm package installed.
2. Confirm permission sets.
3. Configure Zentom API URL.
4. Verify Remote Site / future Named Credential.
5. Test API connection.
6. Send test incident.
7. Confirm SentinelFlow app is working.
8. Show next steps.

## Screen 1: Welcome

Title:

```text
Welcome to SentinelFlow Setup
```

Subtitle:

```text
Powered by Zentom AI
```

Show:

- Hosted API: `https://zentom-api.onrender.com`
- Current mode: `RULE`
- Package status: `Beta`

Purpose:

- Confirm the admin is starting the SentinelFlow beta setup path.
- Explain that hosted beta uses safe rule-based recommendations.
- Explain that production/high-risk actions require policy evaluation and human approval.

## Screen 2: API Configuration

Fields:

- Base URL
- Environment
- Active / Inactive

Target configuration:

```text
Zentom_Setting__mdt.Default.Base_URL__c
```

Expected beta value:

```text
https://zentom-api.onrender.com
```

Important beta note:

Updating Custom Metadata from LWC requires careful handling. For beta, API configuration may remain manual through deployed metadata or admin setup instructions. The wizard can initially display values and provide validation before it writes configuration.

Future implementation options:

- Apex Metadata API wrapper.
- Setup page that deep-links admins to the Custom Metadata record.
- Named Credential based configuration after the marketplace security-review migration.

## Screen 3: Permission Check

Check whether the current user has:

- `SentinelFlow_Admin`
- `SentinelFlow_Approver`
- `SentinelFlow_Viewer`

Recommended behavior:

- Show assigned permission sets.
- Warn if no SentinelFlow permission set is assigned.
- Show admin instructions for assigning permission sets.
- Do not attempt broad permission escalation from the wizard.

## Screen 4: Connection Test

Call:

```text
GET https://zentom-api.onrender.com/
```

Expected response:

```text
Zentom API is ready
```

Recommended behavior:

- Display success if HTTP 200 is returned.
- If the first call fails, explain Render cold start and allow retry.
- If callout authorization fails, instruct admin to verify `Zentom_API` Remote Site Setting.
- Future version should test Named Credential instead of Remote Site Setting.

## Screen 5: Send Test Incident

Trigger:

```apex
ZentomIncidentClient.sendIncident(
    'FLOW_FAILURE',
    'Salesforce Flow',
    'production',
    'Flow failed because owner field is null and missing account owner'
);
```

Expected result:

- Sentinel Incident created.
- Risk: `95 / CRITICAL`.
- Policy: `HUMAN_APPROVAL_REQUIRED`.
- Runbook: `FLOW_FAILURE_BASIC_RECOVERY`.
- Status: `Approval Required`.
- Approval Status: `Pending Approval`.
- Replay timeline events created.

Recommended behavior:

- Show the created Sentinel Incident link.
- Show the returned risk and policy summary.
- Show a retry option if the hosted API cold-started.

## Screen 6: Finish

Show links to:

- SentinelFlow Dashboard
- Sentinel Incidents
- Install Guide
- Security Review Preparation
- Data Privacy & Retention

Suggested final message:

```text
SentinelFlow setup is ready for beta validation.
```

## Future Components

LWC:

```text
sentinelflowSetupWizard
```

Apex:

```text
SentinelFlowSetupController
```

Configuration source:

```text
Zentom_Setting__mdt
```

Future controller responsibilities:

- Read current `Zentom_Setting__mdt` configuration.
- Check permission set assignments for current user.
- Test hosted API health.
- Send a safe test incident.
- Return setup status summary to the LWC.

## Security Considerations

- Do not store secrets in Custom Metadata.
- Do not expose Ollama or local model endpoints.
- Do not allow the wizard to bypass policy evaluation.
- Do not allow the wizard to perform autonomous production actions.
- Keep all test incidents clearly labeled and low risk.
- Use Named Credential, External Credential, and Permission Set Mapping before marketplace security review.

## Later Build Milestone

Actual wizard implementation is deferred.

Recommended future milestone:

```text
Milestone 21: Admin Setup Wizard Implementation
```

The beta package remains installable and verified without the wizard because the install guide provides manual setup steps.
