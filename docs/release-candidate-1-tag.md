# Release Candidate 1 (RC1) Tag

## 1. Purpose
This document confirms that the SentinelFlow Beta 2 codebase has been officially frozen and tagged as Release Candidate 1 (RC1). This tag represents the exact, immutable state of the code that will be deployed to the customer's production Salesforce environment.

## 2. Tag Information
- **Tag Name:** `v1.0.0-rc1`
- **Description:** SentinelFlow Beta 2 - General Availability Release Candidate 1
- **Included Fixes:** All patches from the Active Patch Queue (Milestone 41B) have been successfully merged into this tag.

## 3. Code Freeze Protocol
- **Status:** ACTIVE
- The `master` branch is now under a strict code freeze.
- **No new features or patches** may be merged into `master` without explicit, written override approval from the CTO and Lead Architect.
- Any new development must take place on isolated feature branches targeting the post-GA roadmap (`v1.1.0`).

## 4. Next Steps
With the codebase locked and tagged, engineering will now finalize the **Production Deployment Runbook** (Milestone 41D) to script the exact steps for deploying this specific RC1 package into production.
