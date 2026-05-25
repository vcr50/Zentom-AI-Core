# SentinelFlow Beta Pilot Scenario Run

## 1. Pilot Org

Pilot org:

- Customer name: TBD.
- Salesforce org name: TBD.
- Org type: Sandbox, developer org, or approved low-risk customer environment.
- Org id: TBD.
- Pilot run date: TBD.
- Scenario owner: TBD.
- Customer admin/contact: TBD.

Locked beta rule:

```text
No new features now.
Run pilot.
Collect feedback.
Fix only P0/P1/P2 issues.
```

Prerequisites:

- 30A Select Pilot Customer / Org complete.
- 30B Schedule Pilot Demo complete.
- 30C Install / Validate Package complete or blocker documented.
- Package/version, permission sets, hosted API, hosted DB, callout mode, and test incident path validated.

## 2. Scenario List

Required pilot scenarios:

- Open SentinelFlow app.
- Review dashboard and Org Health Score.
- Run `FLOW_FAILURE` incident test.
- Verify risk and policy decision.
- Verify AI recommendation and runbook.
- Approve incident.
- Reject incident or validate rejection path.
- Execute approved action.
- Confirm Case creation.
- Verify Replay Timeline.
- Verify audit/error logging.
- Capture pass/fail result.

Out of scope:

- New features.
- Major AI architecture changes.
- Agentforce production integration.
- Hosted HYBRID Ollama changes.
- Full autonomous remediation.
- Large object model changes.

## 3. FLOW_FAILURE Incident Test

Scenario:

- Incident type: `FLOW_FAILURE`.
- Test description: Non-sensitive sample text only.
- Expected incident record: Created in the pilot org.
- Expected status after analysis: `Approval Required`.

Execution details:

- Command or action used: TBD.
- Executed by: TBD.
- Timestamp: TBD.
- Evidence link/location: TBD.

Pass criteria:

- Test incident is created.
- Incident type is correct.
- Record can be opened by assigned pilot users.
- No sensitive customer data is used.

## 4. Risk + Policy Verification

Expected risk:

```text
95 / CRITICAL
```

Expected policy:

```text
HUMAN_APPROVAL_REQUIRED
```

Verification checklist:

- Risk score displays as expected.
- Risk level displays as expected.
- Policy Decision record is created or visible.
- Human approval requirement is clear to the user.
- No automatic remediation occurs before approval.

Result:

- Status: Pass / Fail / Blocked.
- Actual risk: TBD.
- Actual policy: TBD.
- Evidence: TBD.

## 5. AI Recommendation + Runbook Check

Expected runbook:

```text
FLOW_FAILURE_BASIC_RECOVERY
```

Verification checklist:

- AI Recommendation section is populated.
- Recommendation is understandable to the pilot customer.
- Recommendation does not claim unsupported autonomous behavior.
- Runbook is `FLOW_FAILURE_BASIC_RECOVERY`.
- Suggested next action is governed by human approval.

Result:

- Status: Pass / Fail / Blocked.
- Actual recommendation summary: TBD.
- Actual runbook: TBD.
- Evidence: TBD.

## 6. Approval Workflow Test

Approval workflow:

- Open the test Sentinel Incident.
- Review risk, policy, recommendation, and runbook.
- Approve the recommended action.
- Confirm approval state is recorded.
- Confirm execution is available only after approval.

Pass criteria:

- Approval action succeeds.
- Incident status updates correctly.
- Approval event is captured for replay/audit review.
- No duplicate approval artifacts are created.

Result:

- Status: Pass / Fail / Blocked.
- Approved by: TBD.
- Evidence: TBD.

## 7. Rejection Workflow Test

Rejection workflow:

- Open a separate test incident or reset to a safe test state.
- Review recommendation and policy.
- Reject the recommended action.
- Confirm rejection state is recorded.
- Confirm execution is blocked after rejection.

Pass criteria:

- Rejection action succeeds.
- Incident status updates correctly.
- Rejection event is captured for replay/audit review.
- No Case or remediation action is executed after rejection.

Result:

- Status: Pass / Fail / Blocked.
- Rejected by: TBD.
- Evidence: TBD.

## 8. Case Creation Execution Test

Execution workflow:

- Use an approved `FLOW_FAILURE` incident.
- Execute the approved action.
- Confirm Salesforce Case is created.
- Confirm Case fields are populated with useful, non-sensitive context.
- Confirm incident links or references the created Case where supported.

Pass criteria:

- Approved action executes successfully.
- Case is created once.
- Case is visible to the expected customer user/admin.
- Case creation is logged for replay/audit review.

Result:

- Status: Pass / Fail / Blocked.
- Case id/link: TBD.
- Evidence: TBD.

## 9. Replay Timeline Verification

Replay Timeline verification:

- Open the Replay Timeline for the test incident.
- Confirm incident creation event appears.
- Confirm risk/policy/recommendation events appear.
- Confirm approval or rejection event appears.
- Confirm execution and Case creation event appears where applicable.
- Confirm timestamps are understandable.

Pass criteria:

- Timeline presents the expected sequence.
- Timeline supports customer audit/review needs.
- Missing or duplicate events are captured as issues.

Result:

- Status: Pass / Fail / Blocked.
- Missing events: TBD.
- Evidence: TBD.

## 10. Dashboard + Org Health Score Check

Dashboard check:

- Open SentinelFlow dashboard.
- Confirm dashboard loads without errors.
- Confirm Org Health Score card loads.
- Confirm recent incident or pilot activity is reflected where expected.
- Confirm dashboard language is clear to the customer.

Pass criteria:

- Dashboard is accessible to assigned users.
- Org Health Score is visible.
- No blocking UI or data-loading errors occur.
- Customer can explain the dashboard value after walkthrough.

Result:

- Status: Pass / Fail / Blocked.
- Org Health Score observed: TBD.
- Evidence: TBD.

## 11. Error Logging Check

Error logging check:

- Review logs after successful pilot scenario execution.
- Confirm no unexpected errors were generated.
- If using a controlled failure, confirm error is captured cleanly.
- Confirm error details avoid sensitive data.

Pass criteria:

- Errors are absent or expected.
- Any generated error is diagnosable.
- Error logging does not expose sensitive customer information.
- P0/P1/P2 issues are created for blocking or material failures.

Result:

- Status: Pass / Fail / Blocked.
- Error ids/links: TBD.
- Evidence: TBD.

## 12. Pass/Fail Summary

Scenario summary:

| Scenario | Result | Evidence | Issue ID |
| --- | --- | --- | --- |
| Open app/dashboard | TBD | TBD | TBD |
| Org Health Score | TBD | TBD | TBD |
| `FLOW_FAILURE` incident | TBD | TBD | TBD |
| Risk + policy | TBD | TBD | TBD |
| AI recommendation + runbook | TBD | TBD | TBD |
| Approval workflow | TBD | TBD | TBD |
| Rejection workflow | TBD | TBD | TBD |
| Case creation execution | TBD | TBD | TBD |
| Replay Timeline | TBD | TBD | TBD |
| Error logging | TBD | TBD | TBD |

Final pilot scenario result:

- Overall status: Pass / Fail / Blocked.
- P0 issues: TBD.
- P1 issues: TBD.
- P2 issues: TBD.
- P3/P4 backlog items: TBD.
- Ready for 30E Capture feedback: Yes / No.

Exit criteria:

- Required pilot scenarios executed or blockers documented.
- Evidence captured for each scenario.
- P0/P1/P2 issues logged for active beta fix consideration.
- Feature requests separated from active beta fixes.
- Customer feedback session is ready for 30E.
