# SentinelFlow Production v1.0 Readiness Plan

## 1. Production Goal

SentinelFlow Private Beta v0.5.0 is complete. Milestone 21 prepares the product for SentinelFlow v1.0 production readiness.

The production goal is to move from a validated private beta workflow to a stable, secure, monitored, documented, and supportable v1.0 release candidate for real Salesforce customer environments.

## 2. Current Beta Status

Current status:

- SentinelFlow Private Beta v0.5.0 is ready.
- Milestone 20 Private Beta Release is complete.
- Salesforce beta package has been hardened.
- Fresh-org validation has passed.
- Hosted Zentom API is live.
- Hosted PostgreSQL + pgvector has been verified.
- Marketplace readiness documentation is complete.
- Beta test plan, scenarios, feedback capture, bug fix sprint plan, and beta release notes are complete.

Current hosted API:

```text
https://zentom-api.onrender.com
```

Current hosted mode:

```text
AI_MODE=RULE
```

## 3. Production Readiness Checklist

Required before v1.0:

- Hosted API stability plan complete.
- Monitoring and alerting plan complete.
- Database backup and recovery plan complete.
- Salesforce package stability verified.
- Named Credential migration plan complete.
- Security review checklist complete.
- v1.0 documentation freeze complete.
- Known beta limitations reviewed and either fixed, documented, or deferred.
- Private beta feedback reviewed.
- P0 and P1 issues closed.
- P2 issues closed or have accepted workarounds.
- Release candidate validation completed.

## 4. Hosted API Stability Requirements

Production readiness requires:

- Stable HTTPS endpoint.
- Health endpoint available.
- Database health endpoint available.
- Clear Render or hosting provider deployment process.
- Environment variables documented and protected.
- Startup behavior reliable.
- Request failures logged.
- Incident endpoint tested after every deployment.
- Hosted beta RULE mode behavior remains deterministic.

Required API checks:

```text
GET /
GET /api/health/db
POST /api/incidents/receive
```

Production decision needed:

- Continue Render for v1.0 launch, or move to a higher-availability hosting tier.
- Decide whether free-tier cold starts are acceptable for v1.0.

## 5. Salesforce Package Stability Requirements

Production readiness requires:

- Beta manifest remains clean.
- Stable tests pass.
- Fresh-org validation passes.
- Permission sets remain least-privilege.
- Package install process is documented.
- Custom Metadata setup is documented.
- Remote Site Setting is replaced or migration path is accepted.
- Approval and execution flows are stable.
- Case creation remains policy and approval gated.
- Replay timeline remains reliable.
- Dashboard and Org Health Score load for intended users.

Required Salesforce checks:

- Install package in clean org.
- Assign permission sets.
- Run test incident.
- Approve recommendation.
- Reject recommendation.
- Execute approved action.
- Confirm Case Origin equals `SentinelFlow`.
- Confirm replay timeline events.
- Confirm dashboard and Org Health Score.

## 6. Database Backup Requirements

Production readiness requires a database backup and recovery plan for hosted PostgreSQL.

Required backup coverage:

- Incident payloads.
- Risk scores.
- Policy decisions.
- AI recommendations.
- Runbook keys.
- Memory entries.
- Dataset export records, if generated.

Backup requirements:

- Identify backup provider capability.
- Define backup frequency.
- Define retention period.
- Define restore process.
- Test restore process before v1.0.
- Document manual export fallback.

Minimum v1.0 expectation:

- Daily automated backups or provider-managed backup coverage.
- Manual export process documented.
- Restore steps documented.

## 7. Monitoring and Alerting Requirements

Production readiness requires basic monitoring for the hosted Zentom API and hosted database.

Required monitoring:

- API uptime.
- API health endpoint.
- DB health endpoint.
- Incident endpoint failures.
- 4xx and 5xx response rate.
- Render deployment failures.
- Database connection failures.
- Latency spikes.

Recommended alerts:

- API down.
- DB health check failing.
- Incident endpoint returning repeated errors.
- Render deploy failed.
- Database connection errors.
- Spike in failed Salesforce callouts.

Minimum v1.0 expectation:

- Health checks documented.
- Alert routing documented.
- Manual incident response steps documented.

## 8. Security Review Requirements

Production readiness requires closing security-review preparation gaps.

Required security review work:

- Finalize security review preparation document.
- Finalize data privacy and retention document.
- Finalize install guide.
- Finalize support/troubleshooting guide.
- Review all Apex sharing and permission assumptions.
- Review CRUD/FLS behavior.
- Review callout configuration.
- Review stored data fields.
- Review human approval and policy gates.
- Review replay/audit logging.
- Confirm no Ollama endpoint is publicly exposed.
- Confirm hosted beta/v1.0 does not allow direct autonomous high-risk execution.

Security principle:

SentinelFlow does not allow AI to directly execute high-risk actions. Risk scoring, policy evaluation, human approval, and replayable audit history remain core controls.

## 9. Named Credential Migration Requirement

Remote Site Setting is acceptable for MVP/private beta, but v1.0 production and marketplace readiness require a migration plan to:

- Named Credential
- External Credential
- Permission Set Mapping

Required migration work:

- Define target Named Credential.
- Define External Credential strategy.
- Define permission set mapping.
- Update Apex callout path if required.
- Update setup/install docs.
- Validate in a clean org.
- Confirm security-review alignment.

Current beta:

```text
Remote Site Setting: Zentom_API
URL: https://zentom-api.onrender.com
```

Target v1.0 direction:

```text
Named Credential based callout configuration
```

## 10. v1.0 Exit Criteria

Milestone 21 can exit when:

- Production readiness checklist is complete.
- Monitoring and alerting plan is complete.
- Backup and recovery plan is complete.
- Named Credential migration plan is complete.
- Security review final checklist is complete.
- v1.0 documentation is frozen.
- Release candidate passes regression validation.
- No open P0 issues remain.
- No open P1 issues remain.
- P2 issues are fixed or explicitly accepted with workarounds.
- Known limitations are documented.
- Decision is made for v1.0 release candidate readiness.
