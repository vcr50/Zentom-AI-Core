# SentinelFlow Beta Pilot Install Validation

## 1. Pilot Org

Pilot org:

- Customer name: TBD.
- Salesforce org name: TBD.
- Org type: Sandbox, developer org, or approved low-risk customer environment.
- Org id: TBD.
- Primary customer admin: TBD.
- Internal validation owner: TBD.
- Validation date: TBD.

Locked beta rule:

```text
No new features now.
Run pilot.
Collect feedback.
Fix only P0/P1/P2 issues.
```

## 2. Package/Version Used

Package/version:

- Release candidate: `v1.0.0-rc.1`.
- Package manifest: `manifest/package-sentinelflow-beta.xml`.
- Expected test baseline: 17 passing / 0 failing.
- Package install target: Selected beta pilot org.
- Installation evidence location: TBD.

Validation note:

- Do not introduce new metadata or feature scope during beta install validation.
- If package install fails, classify as P0/P1/P2 depending on customer impact and pilot blockage.

## 3. Permission Sets Assigned

Permission sets:

- SentinelFlow admin permission set: TBD.
- SentinelFlow user/operator permission set: TBD.
- Case access confirmed: TBD.
- Sentinel Incident access confirmed: TBD.
- Policy Decision access confirmed: TBD.
- Replay/audit access confirmed: TBD.

Assignment evidence:

- Assigned users: TBD.
- Screenshot/evidence link: TBD.
- Result: TBD.

## 4. Hosted API URL

Hosted API:

```text
https://zentom-api.onrender.com
```

Validation owner:

- Owner: TBD.
- Validation timestamp: TBD.
- Evidence link/location: TBD.

## 5. Callout Mode

Default callout mode:

```text
REMOTE_SITE
```

Named Credential path:

- Status: Validated, but not default.
- Use only if explicitly configured for the pilot org.

Callout configuration checklist:

- Remote Site Setting configured for hosted API.
- Shared secret authentication configured where required.
- Test user has permission to execute the callout path.
- Error logging enabled for failed callouts.

## 6. API Health Check

API health check:

- Endpoint/method used: TBD.
- Expected result: Hosted API responds successfully.
- Actual result: TBD.
- Status: Pass / Fail / Blocked.
- Evidence: TBD.

Failure handling:

- API unreachable: classify as P0 if it blocks pilot validation.
- Authentication failure: classify as P1 if callout path cannot complete.
- Intermittent API failure: classify as P2 unless it blocks the full pilot.

## 7. DB Health Check

DB health check:

- Hosted DB status: TBD.
- Vector/search dependency status, if applicable: TBD.
- Expected result: Hosted DB supports the pilot API workflow.
- Actual result: TBD.
- Status: Pass / Fail / Blocked.
- Evidence: TBD.

Validation note:

- DB validation should prove the hosted service can persist or retrieve data needed by the beta workflow.
- Do not load customer-sensitive data into test payloads.

## 8. Test Incident Command

Test incident command:

```text
FLOW_FAILURE
```

Suggested payload fields:

- Incident type: `FLOW_FAILURE`.
- Source org: Selected pilot org.
- Test flow name: TBD.
- Severity input: TBD.
- Description: Use non-sensitive sample text only.

Execution owner:

- Owner: TBD.
- Timestamp: TBD.
- Evidence link/location: TBD.

## 9. Expected Result

Expected validation result:

```text
Hosted API: https://zentom-api.onrender.com
Risk: 95 / CRITICAL
Policy: HUMAN_APPROVAL_REQUIRED
Runbook: FLOW_FAILURE_BASIC_RECOVERY
Status: Approval Required
```

Expected Salesforce result:

- Sentinel Incident record is created.
- AI Recommendation section is populated.
- Policy Decision indicates human approval is required.
- Runbook is `FLOW_FAILURE_BASIC_RECOVERY`.
- Incident status is `Approval Required`.
- Error logging remains clean unless a controlled failure is being validated.

## 10. Validation Evidence

Evidence to capture:

- Package install result.
- Permission set assignment result.
- Hosted API health check result.
- Hosted DB health check result.
- Callout configuration evidence.
- Test `FLOW_FAILURE` command/payload.
- Created Sentinel Incident record.
- Expected risk, policy, runbook, and status values.
- Error log result.

Evidence location:

- Screenshots: TBD.
- Log files: TBD.
- Salesforce record links: TBD.
- Notes owner: TBD.

## 11. Pass/Fail Result

Validation result:

- Package install: Pass / Fail / Blocked.
- Permission sets: Pass / Fail / Blocked.
- Hosted API: Pass / Fail / Blocked.
- Hosted DB: Pass / Fail / Blocked.
- Callout mode: Pass / Fail / Blocked.
- Test incident: Pass / Fail / Blocked.
- Expected result: Pass / Fail / Blocked.
- Error logging: Pass / Fail / Blocked.

Final result:

- Overall status: Pass / Fail / Blocked.
- Blocking issues: TBD.
- P0/P1/P2 issues opened: TBD.
- Pilot can proceed to 30D Run pilot scenarios: Yes / No.

Exit criteria:

- Pilot org identified.
- Package/version recorded.
- Permission sets assigned or blocker documented.
- Hosted API and DB health checked.
- Callout mode confirmed.
- Test `FLOW_FAILURE` incident executed or blocker documented.
- Expected risk, policy, runbook, and status validated.
- Evidence captured.
- Pass/fail result recorded.
