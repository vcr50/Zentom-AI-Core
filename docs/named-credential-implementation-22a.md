# Milestone 22A: Named Credential Implementation Plan

## Purpose

Milestone 22A starts the production implementation sprint by preparing SentinelFlow to move from the working beta Remote Site Setting callout model to a Named Credential based production callout model.

This is an implementation branch and rollout plan. The working beta callout path must remain available until the Named Credential path is validated end to end.

## Branch

Implementation branch:

```text
milestone-22a-named-credential
```

## Current Beta Model

Current flow:

```text
ZentomIncidentClient
-> Reads Zentom_Setting__mdt.Default.Base_URL__c
-> Uses Remote Site Setting Zentom_API
-> Calls https://zentom-api.onrender.com/api/incidents/receive
```

Current Apex endpoint behavior:

```apex
request.setEndpoint(baseUrl + '/api/incidents/receive');
```

Current beta metadata:

- Custom Metadata: `Zentom_Setting__mdt.Default.Base_URL__c`
- Remote Site Setting: `Zentom_API`
- Hosted API: `https://zentom-api.onrender.com`

## Target Production Model

Target flow:

```text
ZentomIncidentClient
-> Uses Named Credential
-> callout:Zentom_API/api/incidents/receive
-> Future External Credential / auth layer
```

Future Apex endpoint behavior:

```apex
request.setEndpoint('callout:Zentom_API/api/incidents/receive');
```

## Safe Rollout Strategy

Rollout sequence:

1. Add Named Credential metadata.
2. Add feature flag in Custom Metadata.
3. Update Apex to support both modes.
4. Validate callout through Named Credential.
5. Keep Remote Site fallback until stable.

Important rule:

```text
Do not delete the working Remote Site flow until Named Credential callout is validated.
```

## Proposed Metadata Changes

### Named Credential

Add:

```text
force-app/main/default/namedCredentials/Zentom_API.namedCredential-meta.xml
```

Initial expected configuration:

```text
Label: Zentom API
Name: Zentom_API
Endpoint: https://zentom-api.onrender.com
Protocol: NoAuthentication
Principal Type: Anonymous
```

Future v1.0/auth layer:

- External Credential
- Permission Set Mapping
- Shared secret or authenticated integration pattern if required

### Custom Metadata Feature Flag

Add fields to `Zentom_Setting__mdt`:

```text
Callout_Mode__c
Named_Credential__c
```

Recommended values:

```text
Callout_Mode__c = REMOTE_SITE | NAMED_CREDENTIAL
Named_Credential__c = Zentom_API
```

Initial beta-safe default:

```text
Callout_Mode__c = REMOTE_SITE
```

Named Credential validation value:

```text
Callout_Mode__c = NAMED_CREDENTIAL
```

## Apex Changes Required

Update `ZentomIncidentClient.getApiEndpoint()` to support both endpoint modes:

```text
REMOTE_SITE:
  baseUrl + '/api/incidents/receive'

NAMED_CREDENTIAL:
  'callout:' + namedCredential + '/api/incidents/receive'
```

Required behavior:

- Default to the current Remote Site behavior if the feature flag is blank.
- Use Named Credential only when explicitly configured.
- Keep `baseUrlOverride` test hook for existing tests.
- Add test coverage for both endpoint modes.
- Throw a clear configuration exception if the selected mode is invalid.

## Test Plan

Unit tests:

- Existing Remote Site/Base URL behavior still passes.
- Named Credential endpoint returns `callout:Zentom_API/api/incidents/receive`.
- Blank feature flag defaults to Remote Site behavior.
- Invalid configuration raises a clear exception.
- Existing incident persistence assertions still pass.

Manual Salesforce validation:

1. Deploy Named Credential metadata to scratch org.
2. Deploy Custom Metadata fields.
3. Deploy Apex changes.
4. Keep `Callout_Mode__c = REMOTE_SITE`.
5. Run existing test incident and confirm current behavior still works.
6. Switch `Callout_Mode__c = NAMED_CREDENTIAL`.
7. Run test incident again.
8. Confirm hosted API receives request.
9. Confirm Sentinel Incident is created.
10. Confirm risk, policy, recommendation, runbook, audit logs, replay timeline, approval panel, and dashboard still work.

## Rollback Plan

Rollback is simple because the Remote Site flow remains intact.

Rollback steps:

1. Set `Zentom_Setting__mdt.Default.Callout_Mode__c = REMOTE_SITE`.
2. Confirm `Base_URL__c = https://zentom-api.onrender.com`.
3. Confirm Remote Site Setting `Zentom_API` is active.
4. Re-run test incident.
5. Confirm Salesforce write-back and replay timeline.

If code rollback is required:

- Revert `ZentomIncidentClient` to last known-good Remote Site implementation.
- Leave Named Credential metadata inactive/unused.
- Re-run stable tests.

## Validation Evidence Required

Before 22A can be marked complete, capture:

- Branch name.
- Changed files.
- Deployment/validation command.
- Stable Apex test results.
- Scratch org or beta org validation result.
- Named Credential callout endpoint evidence from test/mock or debug log.
- Test incident created through Named Credential mode.
- Rollback mode verified or documented.

## 22A Completion Criteria

Milestone 22A is complete when:

- Named Credential metadata exists.
- Feature flag metadata exists.
- `ZentomIncidentClient` supports both Remote Site and Named Credential modes.
- Existing Remote Site flow still works.
- Named Credential callout is validated.
- Stable tests pass.
- Beta package remains deployable.
- Maintenance doc records affected files, validation evidence, and rollback note.
