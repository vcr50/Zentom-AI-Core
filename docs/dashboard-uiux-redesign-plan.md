# SentinelFlow Dashboard UI/UX Redesign Plan

## 1. Purpose

This document defines 32A Dashboard UX Wireframe for Milestone 32 SentinelFlow Dashboard App UI/UX Redesign.

Goal:

```text
Plan a polished, marketplace-ready SentinelFlow dashboard redesign while preserving existing Apex/controller logic and existing data behavior.
```

Design planning mode:

- Use Figma for design thinking and wireframe review.
- Use SLDS + custom scoped LWC CSS for Salesforce implementation.
- Do not add Tailwind or external CSS dependencies to the Salesforce package.

Milestone 32 rule:

```text
Now UI polish is allowed.
Do not break existing Apex/controller logic.
Dashboard redesign must preserve existing data behavior.
```

## 2. Current Dashboard Status

Current dashboard status:

- Existing dashboard surfaces are functional but need stronger visual hierarchy.
- Org Health Score, incident status, approvals, actions, replay, and error visibility need clearer grouping.
- Marketplace screenshots need a more polished, executive-friendly first impression.
- Current data behavior should be treated as stable unless a separate backend milestone is opened.

Current constraints:

- Preserve existing Apex/controller contracts.
- Preserve existing fields, queries, and data loading assumptions.
- Avoid object model changes.
- Avoid new automation behavior.
- Avoid new feature scope unless separately approved.

## 3. Redesign Goal

Redesign goal:

- Make the dashboard immediately understandable to Salesforce admins, operations owners, and marketplace reviewers.
- Put org health and operational risk at the top of the page.
- Make pending approvals easy to find and act on.
- Make recent incidents, executed actions, created Cases, replay events, and system health scannable.
- Improve screenshot readiness for AppExchange / AgentExchange listing assets.

Success criteria:

- Existing data continues to load.
- Existing approval/action flows remain unchanged.
- Dashboard sections are visually distinct and easy to scan.
- Responsive layout works for desktop and tablet review.
- Marketplace screenshots look complete, trustworthy, and privacy-safe.

## 4. Dashboard Layout

Recommended layout:

1. Top app header.
2. Org Health hero section.
3. KPI card section.
4. Pending approval queue.
5. Recent incidents table.
6. Executed actions / created Cases.
7. Replay timeline section.
8. Error logs / system health section.

Layout guidance:

- Use a dense operational dashboard, not a marketing landing page.
- Keep page sections unframed or as clear full-width bands where possible.
- Use cards only for individual repeated items, KPI blocks, and compact dashboard modules.
- Avoid nested cards.
- Prioritize scan speed, status clarity, and confidence.

The dashboard should answer:

- Is my org healthy?
- What needs approval now?
- What is critical?
- What actions were executed?
- Can I audit/replay the decision?

## 4.1 Top App Header

Purpose:

- Establish the dashboard as SentinelFlow Command Center.
- Keep the product/brand signal visible for demos and marketplace screenshots.
- Provide a clear last-refreshed timestamp and refresh affordance.

Recommended contents:

- `SentinelFlow`.
- `by Tomcodex · Powered by Zentom AI`.
- Last refreshed value.
- Refresh button.
- Date range controls.

Optional later:

- Search.
- Filters.
- Environment selector.

## 5. Org Health Hero Section

Purpose:

- Make Org Health Score the first visual anchor.
- Summarize current operational posture without requiring the user to inspect tables first.

Recommended contents:

- Org Health Score.
- Health label, such as Healthy, Watch, At Risk, or Critical.
- Active incident count.
- Pending approval count.
- Last refreshed timestamp.
- Primary risk driver summary.

Design notes:

- Use restrained status color, not a single-hue page theme.
- Keep the score large enough to scan but not oversized.
- Avoid decorative gradients or unrelated illustration.
- Ensure sensitive org/customer data is not exposed in marketplace screenshots.

## 6. KPI Card Section

Recommended KPI cards:

- Open incidents.
- Critical incidents.
- Pending approvals.
- Executed actions.
- Cases created.
- Failed actions.

Design notes:

- Use consistent card sizing.
- Include a small icon on each KPI card.
- Include concise labels and values.
- Use iconography where helpful.
- Use status indicators for warning/critical values.
- Avoid text overflow on smaller screens.

## 7. Pending Approval Queue

Purpose:

- Surface the highest-value operational work: human review before action.

Recommended columns:

- Incident.
- Type.
- Severity / risk.
- Policy decision.
- Recommended runbook.
- Age.
- Action.

Design notes:

- Pending approvals should appear above lower-priority historical content.
- Risk and policy should be visually clear.
- Preserve existing approval/rejection behavior.
- Do not change controller logic or action semantics during redesign.
- Action should navigate to the existing incident review surface.

## 8. Recent Incidents Table

Purpose:

- Let admins and operators quickly scan recent operational incidents.

Recommended columns:

- Incident name or number.
- Type.
- Environment.
- Status.
- Risk.
- Policy.
- Runbook.
- Created date.

Design notes:

- Use table density appropriate for repeated operational use.
- Use clear empty, loading, and error states.
- Keep sample data privacy-safe in screenshots.
- Preserve existing sorting/filtering behavior unless separately scoped.

## 9. Executed Actions / Created Cases

Purpose:

- Show that approved automation produces governed, traceable Salesforce outcomes.

Recommended contents:

- Recently executed approved actions.
- Created Case records.
- Source incident.
- Execution timestamp.
- Execution result.
- Owner or queue where available.

Design notes:

- Emphasize that actions are approval-gated.
- Do not imply autonomous remediation beyond current product behavior.
- Make Case creation visible for marketplace screenshots.

## 10. Replay Timeline Section

Purpose:

- Demonstrate auditability and explainability of each incident lifecycle.

Recommended contents:

- `INCIDENT_RECEIVED`.
- `RISK_CALCULATED`.
- `ZENTOM_POLICY_EVALUATED`.
- `AI_RECOMMENDATION_GENERATED`.
- `HUMAN_APPROVED`.
- `RUNBOOK_ACTION_EXECUTED`.
- `CASE_CREATED`.

Design notes:

- Timeline should be scannable and chronological.
- Use compact event rows with timestamp, event type, and summary.
- Preserve existing replay/audit data behavior.
- Avoid adding events that are not backed by existing data.

## 11. Error Logs / System Health Section

Purpose:

- Give admins confidence that callout, API, execution, and logging issues are visible.

Recommended contents:

- API status.
- Hosted DB status.
- Latest `Sentinel_Error_Log__c` record where already returned by the controller.
- Error count.

Design notes:

- For now, only show data already returned by `ZentomDashboardController`.
- Do not add new Apex for this section in Milestone 32.
- Keep error messages sanitized.
- Avoid exposing secrets, tokens, payloads, or sensitive customer data.
- Use clear severity labels.
- Preserve existing error logging behavior.

## 11.1 Implementation Phases

Milestone 32 implementation phases:

- 32A: Dashboard UX Wireframe.
- 32B: Build App-like Dashboard Layout.
- 32C: Modern SLDS + Custom CSS.
- 32D: Data Display Helpers.
- 32E: Empty State UX.
- 32F: Responsive Testing.
- 32G: Salesforce Validation.
- 32H: Marketplace Screenshot QA.

Implementation constraint:

- Improve only `zentomDashboard.html`, `zentomDashboard.css`, and `zentomDashboard.js`.
- Preserve `ZentomDashboardController`, `getDashboardData` response shape, existing Apex tests, navigation behavior, and package manifest.

## 12. Responsive Design Checklist

Responsive checklist:

- Desktop dashboard uses a clear multi-column layout.
- Tablet layout keeps Org Health and approvals visible without horizontal scrolling.
- Tables handle narrow widths with controlled wrapping or responsive columns.
- KPI cards maintain stable dimensions.
- Buttons and row actions remain tappable.
- Text does not overflow containers.
- Loading, empty, and error states remain readable.
- Marketplace screenshot viewport is tested separately from day-to-day responsive behavior.

## 13. Marketplace Screenshot Checklist

Screenshot checklist:

- Org Health hero is visible and polished.
- KPI cards show realistic privacy-safe sample data.
- Pending approval queue includes a `FLOW_FAILURE` example.
- Recent incidents table is populated with non-sensitive data.
- Created Case is visible or linked.
- Replay Timeline shows approval-gated flow.
- Error/system health section shows clean or controlled sample state.
- No secrets, tokens, customer names, production org ids, or sensitive payloads appear.
- Page avoids unfinished placeholders in final screenshots.
- Visual hierarchy supports marketplace reviewer understanding within a few seconds.

Next milestone:

```text
32B - Dashboard visual design specification
```
