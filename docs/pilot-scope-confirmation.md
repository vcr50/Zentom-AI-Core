# Pilot Scope Confirmation

## 1. Purpose
This document defines the clear boundaries, capabilities, and goals for the SentinelFlow controlled pilot implementation. Establishing a strict scope ensures both our engineering team and the customer are fully aligned on the deliverables for this beta phase.

## 2. Pilot Customer / Audience
- **Target Customer:** Enterprise Operations Leaders and Salesforce Architects
- **Primary Users:** Sentinel Operations Admins, IT Security Teams

## 3. Pilot Decision Status
- **Status:** GO
- **Context:** Following the successful Milestone 37 re-demo, the customer upgraded their decision from CONDITIONAL GO to a full GO, clearing the path for this pilot.

## 4. Pilot Scope
The pilot is designed to prove the core value proposition of SentinelFlow: safe, visible, and governed AI-assisted incident management within Salesforce. It is deliberately constrained to high-value, low-risk operational workflows to build trust before expanding to full autonomous modes.

## 5. In-Scope Capabilities
The following features and capabilities are actively included in the pilot:
- SentinelFlow Command Center
- `FLOW_FAILURE` incident handling
- Zentom `aiTrace` visibility
- AI Explanation Panel (Incident record)
- Risk scoring
- Policy decision engine
- Human approval workflow
- Safe Case creation
- Replay Timeline
- Error logging
- Dashboard AI Signal preview

## 6. Out-of-Scope Capabilities
To maintain focus and mitigate enterprise risk, the following are strictly out-of-scope for the pilot phase:
- Slack bot integration
- Full auto-heal (unattended autonomous execution)
- Digital Twin modeling
- Full realtime event streaming
- Custom AI agents
- Multi-org production rollout

## 7. Pilot Environments
- **Primary:** Target Salesforce Sandbox (`astrosoft` equivalent)
- **Backend:** Managed Zentom AI API instance

## 8. Pilot Users / Roles
- **Sentinel Admin:** Can review, approve, or reject AI recommendations.
- **Sentinel Operations Manager:** Monitors the Command Center dashboard and tracks overall incident health.

## 9. Success Criteria
- SentinelFlow successfully intercepts and traces live `FLOW_FAILURE` incidents in the pilot sandbox.
- The AI Explanation and Command Center previews render accurately with active signals.
- The human approval workflow effectively governs action execution.
- Customer operations teams express confidence in the system's transparency and safety.

## 10. Next Steps
- Execute Pilot Org Setup Checklist (Milestone 38B)
- Finalize Pilot Security / Access Readiness (Milestone 38C)
- Configure Pilot Data & Test Scenarios (Milestone 38D)
