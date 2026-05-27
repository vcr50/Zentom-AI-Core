# Customer Demo Execution Plan — Milestone 35A

## 1. Purpose
Define the process, environment, and success criteria for executing the SentinelFlow Beta 2 presentation to early-access customers and internal stakeholders.

## 2. Demo Objective
Validate whether SentinelFlow Beta 2 clearly communicates customer value, trust, governance, and Salesforce incident response workflow during a controlled customer demo.

## 3. Target Customer / Audience
- IT/Business Leadership (CTO, VP of Platform)
- Salesforce CoE Leads / Lead Architects
- Security & Compliance Teams
- Pilot Program Candidates

## 4. Demo Environment
- **Org:** `astrosoft` (Beta Sandbox)
- **App:** App Launcher → SentinelFlow
- **Data State:** Controlled mock incidents, approvals, and error logs.
- **Connection:** Zentom neural layer simulated via mock API responses to ensure demo stability.

## 5. Demo Assets Used
- `beta2-demo-storyline.md`
- `beta2-customer-presentation-outline.md`
- `beta2-feature-summary.md`
- `beta2-screenshot-capture-checklist.md`
- `beta2-screenshot-qa-privacy-check.md`

## 6. Demo Flow
1. **Introduction (5 min):** Slide deck (Problem Statement, Vision, Architecture).
2. **Dashboard Overview (3 min):** Live Org — Health Score, KPI cards, System Health.
3. **Incident Lifecycle Deep Dive (5 min):** Live Org — Walk through a CRITICAL incident from the Pending Approval Queue.
4. **Approval & Execution (3 min):** Live Org — Execute approval, verify Case creation.
5. **Audit Trail (2 min):** Live Org — Show the Flight Recorder Replay Timeline.
6. **Value Summary & Next Steps (5 min):** Slide deck (Beta Scope, Pilot Call to Action).
7. **Q&A / Feedback (10 min):** Open discussion.

## 7. Roles and Responsibilities
- **Presenter:** Leads the slide presentation and live demonstration.
- **Demo Engineer:** Ensures the `astrosoft` org is staged with the correct incident records prior to the call.
- **Note Taker:** Captures customer questions, objections, and UI/UX feedback.
- **Account Executive:** Manages the relationship, pilot agreement, and follow-up.

## 8. Success Criteria
- Demo completes without technical failure or UI bugs.
- Customer understands the "human-in-the-loop" governance model.
- Customer expresses interest in the Pilot program.
- Clear, actionable feedback is captured for Milestone 36.

## 9. Feedback Capture Method
During the Q&A section, the Note Taker will record feedback directly into a structured document (to be created in 35B), categorizing comments into:
- UI/UX Feedback
- Feature Gaps (P0/P1/P2)
- Security / Compliance Concerns
- Integration Requests

## 10. Follow-up Process
1. Send the Beta 2 Feature Summary PDF.
2. Send the Technical Architecture Diagram.
3. Schedule a follow-up call to review Pilot requirements.
4. Synthesize demo feedback into the next development sprint.
