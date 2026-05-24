# SentinelFlow Monitoring and Error Alerts Plan

## 1. Purpose

This document defines the production monitoring and alerting plan for SentinelFlow v1.0 readiness.

The goal is to detect hosted API downtime, hosted PostgreSQL issues, Salesforce callout failures, incident processing failures, approval/execution errors, and Render service health problems before they materially affect users.

## 2. Monitoring Scope

Monitoring scope:

- Hosted Zentom API
- Hosted PostgreSQL
- Salesforce callouts
- Incident processing
- Risk, policy, recommendation, and runbook generation
- Approval and execution flow
- Case creation
- Replay timeline and audit events
- SentinelFlow dashboard and Org Health Score
- Render service health

Out of scope for current hosted production readiness:

- Hosted Ollama monitoring
- Hosted HYBRID model monitoring
- GPU infrastructure monitoring
- Customer-side local model gateway monitoring

## 3. API Health Checks

Health endpoint:

```text
GET https://zentom-api.onrender.com/
```

Expected:

```json
{
  "status": "running",
  "service": "zentom-api",
  "message": "Zentom API is ready"
}
```

Monitoring expectation:

- Endpoint returns HTTP 200.
- Response status is `running`.
- Response service is `zentom-api`.
- Response message confirms the API is ready.

Failure impact:

- Salesforce callouts may fail.
- Incident intake may stop.
- Beta or production testers may see no new incident records.

## 4. Database Health Checks

Health endpoint:

```text
GET https://zentom-api.onrender.com/api/health/db
```

Expected:

```text
status = ok
databaseType = postgresql
missingTables = []
pgvector enabled = true
```

Monitoring expectation:

- Endpoint returns HTTP 200.
- Status is `ok`.
- Database type is `postgresql`.
- Required tables are present.
- `missingTables` is empty.
- pgvector is enabled.

Failure impact:

- Incidents may not persist.
- Risk scores, policy decisions, recommendations, and memory entries may fail to save.
- Hosted API may still respond but lose core persistence behavior.

## 5. Salesforce Callout Monitoring

Salesforce callouts should be monitored through:

- Apex debug logs.
- Sentinel Incident creation results.
- Callout response handling in `ZentomIncidentClient`.
- User reports from beta and production testers.
- Future scheduled Apex health checks.

Callout checks:

- Remote endpoint is reachable.
- Request does not fail with unauthorized endpoint.
- Request does not timeout after Render wake-up.
- Response body is valid JSON.
- Response includes risk, policy, recommendation, and runbook fields.
- Salesforce write-back succeeds.

Common callout failure causes:

- Hosted API down.
- Render cold start.
- Remote Site Setting misconfigured.
- Future Named Credential misconfigured.
- Base URL points to old Cloudflare or local URL.
- Hosted database unavailable.

## 6. Incident Processing Monitoring

Incident processing monitoring should confirm:

- Salesforce incident signal is sent.
- Hosted Zentom API receives the request.
- Risk score is calculated.
- Policy decision is generated.
- Recommendation is generated.
- Runbook key is selected.
- Salesforce record is created or updated.
- Audit logs are created.
- Replay timeline includes expected events.

Key processing indicators:

- New `Sentinel_Incident__c` created.
- Risk score populated.
- Risk level populated.
- Policy decision populated.
- Recommendation populated.
- Runbook key populated.
- Status and approval status populated.
- Audit log count increases.

## 7. Error Categories

Production error categories:

- API availability error
- Database availability error
- Salesforce callout authorization error
- Salesforce callout timeout
- Invalid hosted API response
- Incident persistence error
- Risk/policy/recommendation mapping error
- Approval workflow error
- Execution workflow error
- Case creation error
- Replay timeline error
- Dashboard or Org Health Score UI error
- Permission set or access error
- Documentation/setup error

Each error should be tagged with:

- Severity
- Source system
- User role
- Affected workflow
- Reproducibility
- Workaround availability

## 8. Alert Severity Levels

```text
P0 - Hosted API down
P1 - Salesforce callout failing
P1 - Hosted DB unavailable
P2 - Incident processing failing
P2 - Approval/execution failure
P3 - Dashboard/replay UI issue
P4 - Documentation or non-blocking issue
```

Response expectations:

- P0: investigate immediately.
- P1: fix before production workflow continues.
- P2: fix before release candidate or provide accepted workaround.
- P3: batch into polish or support sprint.
- P4: document or backlog.

## 9. Alert Channels

Initial alert channels:

- Render dashboard and logs
- Manual health check results
- Salesforce debug logs
- Beta support reports
- Internal project tracker

Planned production alert channels:

- Email alerts
- Slack alerts
- UptimeRobot or Better Stack alerts
- Render deploy failure notifications
- Salesforce scheduled health check alerts

Alert content should include:

- Severity
- Affected service
- Endpoint or workflow
- Timestamp
- Error message
- Recent deployment, if any
- Suggested first diagnostic step

## 10. Manual Monitoring Checklist

Manual checklist:

- Open hosted API health URL
- Open `/docs`
- Check `/api/health/db`
- Run a test incident from Salesforce
- Confirm Sentinel Incident is created
- Confirm audit logs are created
- Confirm approval panel loads
- Confirm Case creation works
- Confirm Replay Timeline shows full event flow

Recommended manual cadence before v1.0:

- Run before each release candidate validation.
- Run after each hosted API deployment.
- Run after Salesforce metadata deployment.
- Run after environment variable changes.
- Run after hosted database maintenance.

## 11. Future Automated Monitoring

Planned automated monitoring:

- UptimeRobot or Better Stack ping monitor
- Render logs monitoring
- Email/Slack alerting
- Salesforce scheduled health check Apex
- Daily hosted DB health check
- Error log object inside Salesforce

Future Salesforce health check design:

- Scheduled Apex calls hosted API health endpoint.
- Scheduled Apex calls hosted DB health endpoint.
- Results are stored in a Salesforce health/error object.
- Admin receives alert when checks fail repeatedly.
- Dashboard shows latest integration health.

Future hosted API monitoring design:

- External monitor pings `/`.
- External monitor pings `/api/health/db`.
- Failed checks trigger alert.
- Render logs are reviewed for repeated 5xx errors.
- Incident endpoint failures are summarized.

## 12. Production Readiness Requirements

Monitoring is production-ready when:

- Hosted API health check is defined.
- Hosted DB health check is defined.
- Manual monitoring checklist is documented.
- Alert severity levels are documented.
- Alert channels are selected.
- Salesforce callout failure process is documented.
- Incident processing failure process is documented.
- Render logs can be reviewed by the support owner.
- Future automated monitoring path is documented.
- v1.0 release candidate includes monitoring validation.
