# SentinelFlow Backup and Recovery Plan

## 1. Purpose

This document defines the backup and recovery plan for SentinelFlow v1.0 production readiness.

The goal is to ensure SentinelFlow can recover from hosted API failures, hosted PostgreSQL issues, Salesforce metadata problems, configuration mistakes, source-code issues, and documentation loss with clear ownership and repeatable steps.

## 2. Backup Scope

Backup scope:

- Hosted PostgreSQL
- Zentom API configuration
- Salesforce package metadata
- Salesforce incident and audit data
- Documentation
- GitHub source code
- Release snapshots

Minimum production backup policy:

- GitHub source code: backed up through Git remote.
- Hosted DB: daily backup/export before production.
- Salesforce metadata: tracked in Git.
- Salesforce customer data: remains in customer org.
- Documentation: tracked in Git and DOCX backup copies.
- Release snapshots: tagged in Git before beta/v1.0 releases.

## 3. Hosted PostgreSQL Backup Plan

Hosted PostgreSQL tables to protect:

- `incidents`
- `risk_scores`
- `policy_decisions`
- `ai_recommendations`
- `memory_entries`

Backup requirements:

- Confirm hosted provider backup capability.
- Enable daily backups or daily exports before production.
- Keep backup credentials out of Git.
- Document restore procedure.
- Test restore into a non-production database.
- Verify pgvector extension availability during restore.

Minimum v1.0 target:

- Daily backup/export.
- Manual export before major releases.
- Restore test completed before v1.0 release candidate.

## 4. Salesforce Metadata Backup Plan

Salesforce metadata is backed up through the `zentom-suite` GitHub repository.

Salesforce metadata to protect:

- SentinelFlow Lightning App
- SentinelFlow tabs
- SentinelFlow LWC components
- Apex classes and tests
- `Sentinel_Incident__c`
- `Sentinel_Audit_Log__c`
- `Zentom_Policy_Decision__c`
- SentinelFlow permission sets
- Custom metadata settings
- Runbook metadata
- Remote Site Setting / future Named Credential metadata
- Salesforce package manifest

Backup requirements:

- Keep deployable metadata in Git.
- Commit and push after each milestone.
- Tag release snapshots.
- Validate package manifest before release.

## 5. Salesforce Data Backup Plan

Salesforce customer data remains in the customer Salesforce org.

Salesforce data involved in SentinelFlow:

- `Sentinel_Incident__c`
- `Sentinel_Audit_Log__c`
- `Zentom_Policy_Decision__c`
- Created Case references
- Approval status
- Execution status
- Replay timeline data

Production recommendation:

- Customer admins should use their standard Salesforce backup/export policy.
- SentinelFlow should not become the only copy of customer operational history.
- For support, export only the minimum required records and logs.
- Avoid storing secrets or unnecessary sensitive data in SentinelFlow objects.

## 6. Zentom API Configuration Backup

Configuration to protect:

- Render service settings
- Render environment variables
- `DATABASE_URL`
- `AI_MODE`
- `AI_PROVIDER`
- `AI_MODEL`
- Dockerfile
- `render.yaml`
- `.env.production.example`

Code/config tracked in Git:

- `services/zentom-api/Dockerfile`
- `services/zentom-api/render.yaml`
- `services/zentom-api/.env.production.example`

Secret values:

- Must not be committed to Git.
- Must be stored in the hosting provider environment variable manager.
- Must be documented as required keys without exposing values.

## 7. GitHub Repository Backup

Code backup source:

```text
zentom-suite GitHub repo
```

Code backup items:

- `zentom-suite` GitHub repo
- Dockerfile
- `render.yaml`
- Salesforce package manifest
- `docs` folder
- Salesforce package metadata
- Zentom API source code
- Dataset and experiment documentation

Backup requirements:

- Push milestone commits to GitHub.
- Use release tags for beta and v1.0 snapshots.
- Avoid force-pushing release branches.
- Keep protected branch rules as a future production hardening task.

## 8. Documentation Backup

Documentation sources:

- Markdown docs in `docs/`
- FRD/Maintenance DOCX backup copies
- Release notes
- Install guide
- Security/privacy/support docs

Backup requirements:

- Track Markdown docs in Git.
- Keep DOCX backups for polished release documents.
- Commit docs after each milestone.
- Tag documentation freeze snapshots.

## 9. Recovery Scenarios

### Scenario 1: Hosted API down

Impact:

- Salesforce callouts fail.
- New incident processing may stop.

Recovery:

- Check Render service status.
- Check latest deployment logs.
- Open `https://zentom-api.onrender.com/`.
- Restart or redeploy service if needed.
- Validate `/api/health/db`.
- Run Salesforce test incident.

### Scenario 2: Hosted database unavailable

Impact:

- Hosted API may fail to persist incidents and recommendations.

Recovery:

- Check `https://zentom-api.onrender.com/api/health/db`.
- Check hosted DB provider status.
- Verify `DATABASE_URL`.
- Restart hosted API if connection pool is stale.
- Restore from backup if data loss occurred.

### Scenario 3: Accidental database data loss

Impact:

- Hosted incident, risk, policy, recommendation, or memory data may be missing.

Recovery:

- Stop write-heavy testing if needed.
- Identify time of data loss.
- Restore latest valid backup into test DB.
- Validate restored tables.
- Promote restored DB or migrate recovered data according to provider process.
- Run incident processing regression test.

### Scenario 4: Salesforce metadata deployment issue

Impact:

- App, objects, Apex, LWC, permission sets, or metadata may be missing or broken.

Recovery:

- Revert to latest known-good Git commit or release tag.
- Validate beta/package manifest.
- Deploy to scratch org first.
- Deploy to affected org after validation.
- Re-run stable tests.

### Scenario 5: Wrong Zentom API URL configured

Impact:

- Apex may call old Cloudflare/local URL or invalid endpoint.

Recovery:

- Verify `Zentom_Setting__mdt.Default.Base_URL__c`.
- Set value to `https://zentom-api.onrender.com`.
- Verify Remote Site Setting or future Named Credential.
- Run test incident.

### Scenario 6: Render deployment rollback needed

Impact:

- New deployment may break hosted API behavior.

Recovery:

- Identify last known-good Git commit.
- Roll back Render deployment or redeploy previous commit.
- Confirm environment variables are unchanged.
- Validate `/`.
- Validate `/api/health/db`.
- Run test incident.

### Scenario 7: GitHub repo or branch issue

Impact:

- Source code or metadata history may be difficult to recover.

Recovery:

- Check remote repository status.
- Use local clones if remote is temporarily unavailable.
- Recover from release tags.
- Avoid destructive branch operations during release windows.
- Re-push known-good branch if needed.

### Scenario 8: Documentation loss

Impact:

- Install, support, security, privacy, release, or maintenance docs may be missing.

Recovery:

- Restore Markdown docs from Git.
- Restore DOCX from backup copies.
- Rebuild release docs from Markdown sources if needed.
- Tag documentation freeze after recovery.

## 10. Recovery Steps

General recovery workflow:

1. Identify affected system.
2. Assign severity.
3. Stop further risky changes.
4. Capture current logs and timestamps.
5. Identify last known-good state.
6. Restore config, code, metadata, or data from backup.
7. Validate health endpoint.
8. Validate database health endpoint.
9. Run Salesforce test incident.
10. Confirm write-back, replay timeline, dashboard, and approval/execution behavior.
11. Document the incident and fix.

## 11. Recovery Testing Schedule

Recommended schedule:

- Before v1.0 release candidate: full recovery test.
- Before each major release: metadata restore/deploy test.
- Monthly after production launch: hosted API and DB recovery drill.
- Quarterly after production launch: documentation and release tag verification.

Recovery testing checklist:

- Restore database backup into test DB
- Deploy Salesforce beta package into scratch org
- Verify hosted API health
- Verify `/api/health/db`
- Run test incident
- Confirm Salesforce write-back
- Confirm replay timeline
- Confirm dashboard loads

## 12. Production Readiness Requirements

Backup and recovery is production-ready when:

- Hosted DB backup/export process is documented.
- Restore process is tested in a non-production database.
- Salesforce metadata is tracked in Git.
- Salesforce package deploys into a clean org.
- Required Render/API configuration keys are documented.
- Secrets are not committed to Git.
- Documentation is tracked in Git.
- Release snapshots are tagged.
- Recovery scenarios and steps are documented.
- Recovery testing checklist passes before v1.0 release candidate.
