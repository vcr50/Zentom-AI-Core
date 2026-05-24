# Render Uptime and Cold Start Strategy

## 1. Purpose

This document defines the SentinelFlow strategy for reducing or documenting Render free-tier cold start risk before production.

The goal is to keep private beta practical while making it clear that production Salesforce callouts should not depend on sleeping infrastructure.

## 2. Current Hosting Model

Current hosted API:

```text
https://zentom-api.onrender.com
```

Current model:

- Zentom API is deployed to Render.
- Hosted beta uses `AI_MODE=RULE`.
- Hosted PostgreSQL + pgvector is connected.
- Salesforce calls the hosted API through Remote Site or Named Credential mode.
- Render free-tier behavior may sleep after inactivity.

Current beta decision:

```text
Render free tier is acceptable for beta with documented retry/cold-start warning.
```

## 3. Cold Start Risk

Render free-tier services may spin down after inactivity.

Cold start risk:

- First request after idle time may be slow.
- First request may timeout.
- Salesforce Apex callout may fail before the Render service fully wakes.
- A second request often succeeds after the service is warm.

This is acceptable for private beta validation, but it is not acceptable as the final production reliability posture.

## 4. Impact on Salesforce Callouts

Salesforce impact:

- First Apex call may timeout if Render service is sleeping.
- The future method may complete without creating a Sentinel Incident if the hosted API response is unavailable or non-2xx.
- Admins/testers may need to wake the service before running validation.
- Retry after service wakes up.

Production rule:

```text
Production should not rely on free-tier sleeping infrastructure.
```

## 5. Current Mitigation

Current beta mitigation:

- Open `https://zentom-api.onrender.com/` before testing.
- Confirm root health endpoint returns `status = running`.
- Confirm `/api/health/db` returns `status = ok`.
- Retry Salesforce test incident after 30-60 seconds if the first call fails.
- Document cold-start behavior in install, support, beta testing, monitoring, and release docs.

Current health checks:

```text
GET https://zentom-api.onrender.com/
GET https://zentom-api.onrender.com/api/health/db
```

## 6. Short-term Beta Strategy

Recommended beta decision:

```text
Keep Render free tier for beta only.
```

Beta actions:

- Keep cold-start warning in support docs.
- Tell testers to wake the hosted API before callout scenarios.
- Record cold-start failures separately from product logic failures.
- Use retry behavior during beta validation.
- Continue tracking hosted API health in `docs/monitoring-error-alerts.md`.

Option A:

```text
Keep Render free for beta only.
```

Pros:

- Low cost.
- Already working.
- Good enough for controlled beta.

Cons:

- Cold starts can affect first Salesforce callout.
- Not suitable as final production reliability posture.

## 7. Production Strategy

Production recommendation:

```text
Use paid always-on hosting or another always-on cloud runtime.
```

Option B:

```text
Upgrade Render service to always-on paid plan.
```

Pros:

- Minimal migration.
- Keeps current deployment model.
- Reduces cold-start risk.

Cons:

- Adds monthly hosting cost.
- Still depends on Render service limits and region.

Option C:

```text
Move to AWS/Azure/GCP.
```

Pros:

- More production architecture options.
- Better control over scaling, networking, monitoring, and secrets.
- Stronger enterprise posture.

Cons:

- More DevOps complexity.
- More setup and operating overhead.

Option D:

```text
Add uptime monitor/keep-alive ping.
```

Pros:

- Simple to add.
- Can reduce cold-start frequency.
- Useful even with paid hosting for monitoring.

Cons:

- Free-tier platforms may restrict or discourage keep-alive patterns.
- Does not replace an always-on production runtime.

## 8. Monitoring Plan

Monitoring plan:

- Monitor `GET /`.
- Monitor `GET /api/health/db`.
- Track Salesforce callout failures.
- Track incident creation gaps.
- Track Render deploy failures.
- Review Render logs after callout failures.

Potential monitoring tools:

- UptimeRobot
- Better Stack
- Render service logs
- Email alerting
- Slack alerting
- Salesforce scheduled health check Apex

Minimum beta monitoring:

- Manual health check before test sessions.
- Manual DB health check before test sessions.
- Record cold-start behavior in beta notes.

Minimum production monitoring:

- Automated uptime check.
- Automated DB health check.
- Alert route for API down.
- Alert route for DB unavailable.
- Incident response owner.

## 9. Go/No-Go Criteria

Beta go criteria:

- Cold start risk documented.
- Beta mitigation documented.
- Testers know to wake the service and retry.
- Hosted API health endpoint works.
- Hosted DB health endpoint works.

Production go criteria:

- Production always-on requirement documented.
- Monitoring/keep-alive option documented.
- Hosting decision made: paid Render, AWS/Azure/GCP, or equivalent always-on runtime.
- Salesforce callouts are not dependent on sleeping free-tier infrastructure.
- API downtime and DB health alerts are configured or explicitly accepted for release candidate.

No-go for production:

- Free-tier cold starts remain the expected runtime behavior.
- No uptime monitoring exists.
- No owner is assigned for hosted API failures.
- Salesforce incident intake cannot be reliably validated after idle periods.
