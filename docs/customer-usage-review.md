# Customer Usage Review

## 1. Purpose
This document provides a structured review of SentinelFlow's post-launch adoption. Following the CTO's directive, production success equals a stable system *plus* real customer adoption. This framework measures how deeply the customer has integrated the tool into their daily operations.

## 2. Review Period
**Start Date:** [YYYY-MM-DD]  
**End Date:** [YYYY-MM-DD]

## 3. Customer / Org
- **Customer:** [Enterprise Name]
- **Target Org:** Production

## 4. Usage Metrics
*Track the following quantitative data points over the review period:*
- **SentinelFlow Logins / Active Users:** [X]
- **Command Center Dashboard Views:** [X]
- **Total Sentinel Incidents Processed:** [X]
- **`FLOW_FAILURE` Incidents Processed:** [X]
- **AI Explanation Panel Views:** [X]
- **Command Center AI Signal Views:** [X]
- **Approval Actions Completed:** [X]
- **Cases Created from SentinelFlow:** [X]
- **Replay Timeline Views:** [X]
- **Error Logs Created (`Sentinel_Error_Log__c`):** [X]
- **P0/P1/P2 Issues Reported:** [X]

## 5. Feature Adoption
*Analyze the spread of usage across different roles.* Are Level 1 support agents using the Case Creation button? Are Level 3 architects relying on the AI traces?

## 6. Incident Processing Activity
Are all `FLOW_FAILURE` events successfully routing through the system? Compare the number of native Salesforce flow errors to the number of SentinelFlow incidents created to verify total capture rate.

## 7. AI Trace Usage
Are users actually expanding and reading the AI Explanation Panel, or just glancing at the AI Signal on the dashboard?

## 8. Approval Workflow Usage
How many `HYBRID` incidents triggered a manual approval gate? What was the average time-to-approval by the admin team?

## 9. Replay Timeline Usage
Are users utilizing the replay timeline to reconstruct the sequence of events leading to a failure?

## 10. Dashboard Usage
Is the Command Center remaining open as a persistent tab for operations monitoring, or only being opened ad-hoc?

## 11. Support Tickets / Issues
Summarize any P3/P4 feature requests or UX friction reported during this period.

## 12. Customer Feedback
*Capture direct quotes or survey responses from the operations team regarding their workflow efficiency post-launch.*

## 13. Adoption Score
*(Select one based on the metrics above)*
- **[ ] High Adoption:** Customer actively uses dashboard, incidents, approval, replay, and AI trace.
- **[ ] Medium Adoption:** Customer uses dashboard and incident records, but limited approval/replay usage.
- **[ ] Low Adoption:** Customer installed product but rarely uses core workflow.

## 14. Risk Signals
Identify any behaviors that threaten long-term retention (e.g., users reverting to standard Salesforce setup audit trails, ignoring AI explanations).

## 15. Next Actions
- Define enablement steps if Adoption is Medium or Low.
- Escalate any severe UX friction to the v1.1.0 Roadmap Intake (Milestone 42F).
