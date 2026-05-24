# Salesforce Callout Security

## Current Beta Callout Model

SentinelFlow beta uses:

```text
Remote Site Setting + Custom Metadata Base_URL__c
```

Current hosted endpoint:

```text
https://zentom-api.onrender.com
```

Beta metadata:

```text
Remote Site Setting: Zentom_API
URL: https://zentom-api.onrender.com

Custom Metadata: Zentom_Setting__mdt.Default
Base_URL__c: https://zentom-api.onrender.com
```

The Remote Site Setting stores only the base URL. Apex appends the endpoint path:

```text
/api/incidents/receive
```

This keeps the beta callout simple and stable while the hosted API remains in `AI_MODE=RULE`.

## Why Remote Site Remains For Beta

Remote Site Setting remains acceptable for the beta milestone because:

- It is already working in the verified Salesforce to Render flow.
- It avoids introducing credential plumbing before beta validation.
- No API key or secret is stored in the Remote Site Setting.
- The hosted Zentom API currently accepts beta incident payloads without Salesforce-managed authentication.
- The beta priority is deployment stability and package cleanliness.

## Future Package-Ready Model

Before AppExchange/security-review readiness, migrate the Zentom API callout to:

```text
Named Credential
External Credential
Permission Set Mapping
```

Target model:

```text
Apex -> callout:Zentom_API/api/incidents/receive
Named Credential -> External Credential -> Principal -> Permission Set Mapping
```

The future model should:

- Remove direct endpoint construction from Apex.
- Store endpoint and authentication configuration in Salesforce metadata.
- Support per-org setup without editing Apex.
- Use permission set mappings to control who can invoke the external credential.
- Avoid storing secrets in Custom Metadata, Custom Settings, labels, or Apex code.

## Migration Plan

1. Create a `Zentom_API` Named Credential pointed at `https://zentom-api.onrender.com`.
2. Create an External Credential for the hosted Zentom API.
3. Add a principal for the beta/prod integration identity.
4. Map the principal through a SentinelFlow permission set.
5. Update `ZentomIncidentClient` to use:

```text
callout:Zentom_API/api/incidents/receive
```

6. Remove the Remote Site Setting from the package manifest.
7. Keep `Zentom_Setting__mdt` for non-secret app configuration only, or replace `Base_URL__c` with a Named Credential name.
8. Validate install, permission assignment, Apex tests, and live callout.

## Security Rules

- Do not store API keys or secrets in Custom Metadata.
- Do not hardcode hosted URLs in Apex.
- Do not include endpoint paths in Remote Site URLs.
- Do not expose Ollama or local model endpoints directly.
- Use Named Credentials for authenticated production callouts.
- Keep all policy and safety checks inside the Zentom API.

## 18D Decision

For Milestone 18D:

```text
Beta = keep Remote Site Setting
AppExchange readiness = migrate to Named Credential + External Credential later
```

No code path changes are required for beta because the current Salesforce to Render callout is verified.
