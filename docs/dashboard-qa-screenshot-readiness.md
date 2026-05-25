# SentinelFlow Dashboard QA + Screenshot Readiness

## 1. Purpose

This document defines 32C Dashboard QA + Screenshot Readiness for Milestone 32 Dashboard UI/UX Redesign.

Goal:

```text
Confirm the redesigned SentinelFlow dashboard is ready for QA review and marketplace screenshots without changing data/controller behavior.
```

Milestone 32 rule:

```text
No data/controller changes.
Only dashboard QA and screenshot readiness.
```

## 2. Validation Evidence

Validation evidence:

- Full manifest validation: failed due unrelated Apex class coverage in manifest.
- Dashboard controller test result: `ZentomDashboardControllerTest` passed 6/6.
- Narrow dashboard LWC validation: succeeded.
- Dashboard-specific deploy id: `0AfdL00000b0iQMSAY`.
- Dashboard bundle validated: `zentomDashboard`.
- Files validated: `zentomDashboard.html`, `zentomDashboard.css`, `zentomDashboard.js`, and bundle metadata.

Validation interpretation:

- 32B is acceptable because dashboard-specific validation passed.
- Existing controller behavior was preserved.
- Full manifest coverage issues should remain separate from dashboard UI/UX QA.

## 3. UI Sections Verified

Sections to verify:

- Org Health hero card.
- KPI summary cards.
- Pending approval queue.
- Recent incidents table.
- Executed actions panel.
- Created Cases panel.
- Replay mini timeline.
- System health / error log panel.
- Loading state.
- Empty states.
- Error state.

Verification result:

| Section | Desktop | Responsive | Screenshot Ready | Notes |
| --- | --- | --- | --- | --- |
| Org Health hero | TBD | TBD | TBD | TBD |
| KPI cards | TBD | TBD | TBD | TBD |
| Pending approvals | TBD | TBD | TBD | TBD |
| Recent incidents | TBD | TBD | TBD | TBD |
| Executed actions / cases | TBD | TBD | TBD | TBD |
| Replay timeline | TBD | TBD | TBD | TBD |
| System health / errors | TBD | TBD | TBD | TBD |

## 4. Desktop QA

Desktop QA checklist:

- Header and date range controls are aligned.
- Org Health hero is first and visually dominant.
- KPI cards scan left to right without text overflow.
- Pending approval queue is visible above lower-priority sections.
- Recent incidents table is readable and horizontally scrolls only when needed.
- Executed actions and created Cases are visually paired.
- Replay timeline reads chronologically and does not overlap.
- System health panel is readable and does not imply unsupported backend checks.
- All buttons and links remain clickable.
- No sensitive data appears in sample values.

Desktop result:

- Status: Pass / Fail / Blocked.
- Browser/viewport: TBD.
- Evidence: TBD.

## 5. Responsive QA

Responsive QA checklist:

- Tablet layout stacks content cleanly.
- Mobile/narrow layout uses one-column sections.
- KPI cards keep stable sizing.
- Tables remain usable with horizontal scrolling.
- Compact rows wrap without overlap.
- Timeline rows do not overflow.
- Date range controls remain usable.
- Text remains legible and does not overlap adjacent UI.

Responsive result:

- Status: Pass / Fail / Blocked.
- Viewports tested: TBD.
- Evidence: TBD.

## 6. Data Behavior Check

Data behavior checks:

- `getDashboardData` wire still drives dashboard data.
- Existing response shape is unchanged.
- Existing arrays are still used for incidents, approvals, executions, replay events, and cases.
- No Apex/controller change was introduced.
- No new data endpoint was introduced.
- Empty and error states continue to render.
- Existing date range behavior is preserved.

Result:

- Status: Pass / Fail / Blocked.
- Evidence: TBD.

## 7. Navigation Behavior Check

Navigation behavior checks:

- Incident links still open `Sentinel_Incident__c` records.
- Case links still open `Case` records.
- Date range buttons still refresh the dashboard.
- Pending approval links use existing incident navigation.
- Executed action and created Case links preserve existing behavior.
- Replay timeline incident links preserve existing behavior.

Result:

- Status: Pass / Fail / Blocked.
- Evidence: TBD.

## 8. Screenshot List

Required screenshots:

- Dashboard hero + KPI cards.
- Pending approvals queue.
- Recent incidents table.
- Executed actions / created cases.
- Replay timeline section.
- System health / error log panel.

Screenshot rules:

- Use privacy-safe sample data.
- Do not expose org ids, customer names, secrets, tokens, or sensitive payloads.
- Ensure no loading spinners or unfinished placeholders are visible.
- Prefer a viewport that shows the Org Health hero and KPI cards together.
- Capture at least one screenshot that shows approval-gated workflow value.

## 9. Known Issues

Known issues:

| Issue | Severity | Impact | Owner | Target |
| --- | --- | --- | --- | --- |
| Full manifest validation coverage issue | Non-dashboard | Full manifest validation blocked by unrelated Apex coverage | TBD | Separate milestone |

Known issue rules:

- Dashboard-specific QA issues may remain in Milestone 32.
- Apex/controller/data behavior issues require separate explicit scope.
- Full manifest coverage failures unrelated to dashboard UI should not block screenshot readiness if dashboard-specific validation passes.

## 10. Readiness Result

Readiness result:

- Desktop QA: Pass / Fail / Blocked.
- Responsive QA: Pass / Fail / Blocked.
- Data behavior check: Pass / Fail / Blocked.
- Navigation behavior check: Pass / Fail / Blocked.
- Screenshot readiness: Pass / Fail / Blocked.

Final result:

- Ready for screenshots: TBD.
- Needs UI polish: TBD.
- Blocked: TBD.

Next milestone:

```text
32D - Dashboard screenshot capture
```
