# Dashboard Future Data Mapping — Milestone 33D

## 1. Purpose
Document how each section of the SentinelFlow Command Center dashboard maps to current and future data sources, ensuring a clear path from skeleton UI to live neural-powered data.

## 2. SentinelFlow vs Zentom Architecture

```
┌─────────────────────────────────────────────────────────┐
│  SentinelFlow (Salesforce App)                          │
│  ═══════════════════════════════                        │
│  Skeleton / Command Center / UI Layer                   │
│  • LWC Components (zentomDashboard, etc.)               │
│  • Apex Controllers (ZentomDashboardController)         │
│  • Custom Objects (Sentinel_Incident__c, etc.)          │
│  • Experience Cloud Portal                              │
└──────────────────────┬──────────────────────────────────┘
                       │ REST / Callout
┌──────────────────────▼──────────────────────────────────┐
│  Zentom (Neural Brain / Intelligence Layer)             │
│  ═════════════════════════════════════                  │
│  AI OS / Decision Engine / Memory                       │
│  • Policy Engine (approval rules, risk scoring)         │
│  • AI Engine (pattern detection, RAG, embeddings)       │
│  • Memory Layer (context, learning, replay)             │
│  • API Gateway (health, predictions, analytics)         │
└─────────────────────────────────────────────────────────┘
```

**Key line:** SentinelFlow = Salesforce app / skeleton / command center. Zentom = neural brain / intelligence layer.

## 3. Current Skeleton Sections

| Section | Component | Location |
|---|---|---|
| Dashboard Home | `zentomDashboard` | SentinelFlow Home tab |
| Command Center | `sentinelFlowBetaAppShell` | Experience Cloud portal |
| Approval Queue | `zentomApprovalQueue` | Approvals nav item |
| Incident Detail | Standard record page | Sentinel_Incident__c |

## 4. Current Data Sources

| Object / Source | API Name | Status |
|---|---|---|
| Incidents | `Sentinel_Incident__c` | ✅ Live — SOQL via Apex |
| Audit Log | `Sentinel_Audit_Log__c` | ✅ Live — SOQL via Apex |
| Error Log | `Sentinel_Error_Log__c` | ✅ Live — SOQL via Apex |
| Policy Decisions | `Zentom_Policy_Decision__c` | ✅ Live — SOQL via Apex |
| Cases | `Case` (standard) | ✅ Live — linked from incidents |
| Runbook Metadata | `Zentom_Runbook__mdt` | ✅ Live — Custom Metadata |

## 5. Future Data Sources

| Source | Type | Status |
|---|---|---|
| Zentom AI Engine | REST API | 🔮 Future — pattern detection, predictions |
| Zentom Policy Engine | REST API | 🔮 Future — real-time approval rules |
| Zentom Memory / RAG | REST API | 🔮 Future — context-aware recommendations |
| Zentom Health API | REST API | 🔮 Future — API status, latency, uptime |
| External Monitoring | Webhook / Platform Event | 🔮 Future — Datadog, PagerDuty, etc. |

## 6. Zentom Neural Layer Mapping

| Zentom Capability | What It Provides | Dashboard Section |
|---|---|---|
| Risk Scoring Engine | Real-time risk scores per incident | Org Health Score, KPI cards |
| Pattern Detection | Anomaly detection across incidents | Neural Insights (future) |
| Policy Engine | Approval/reject recommendations | Pending Approvals, Clearance Queue |
| Memory / RAG | Historical context, similar incidents | Replay Timeline, Incident Detail |
| Prediction Engine | Forecasted incident trends | KPI trend indicators (future) |
| Health Monitor | API uptime, latency, error rates | System Health panel |

## 7. Card-by-Card Data Mapping

### Org Health Score
| Field | Current Source | Future Source |
|---|---|---|
| Score (0–100) | Derived: incidents + approvals + errors | Zentom scoring algorithm |
| Status label | Apex logic in `ZentomDashboardController` | Zentom Health API |
| Reason text | Apex logic based on counts | Zentom AI-generated summary |
| Meta pills | SOQL counts from incidents/approvals | Real-time Zentom metrics |

### KPI Cards (8 metrics)
| Card | Current Source | Future Source |
|---|---|---|
| Live Incidents | `Sentinel_Incident__c` count | Same + Zentom enrichment |
| Critical Traffic | `Sentinel_Incident__c` where risk = CRITICAL | Same + Zentom risk scoring |
| Awaiting Clearance | `Sentinel_Incident__c` where approval = Required | Same + Zentom policy engine |
| Cleared Actions | `Sentinel_Incident__c` where execution = Executed | Same |
| Cases Created | `Case` linked from incidents | Same |
| Failed Actions | Derived from execution status = Failed | Same + Zentom error analysis |
| Flight Recorder | `Sentinel_Audit_Log__c` count | Same + Zentom memory |
| Top Runbook | Most frequent `runbookKey` | Same + Zentom pattern detection |

### Tower Strip (5 metrics)
| Metric | Current Source | Future Source |
|---|---|---|
| Org posture | `orgHealthStatus` from Apex | Zentom Health API |
| Awaiting clearance | Pending approvals count | Same |
| Critical traffic | Critical incidents count | Same |
| Cleared actions | Executed actions count | Same |
| Flight recorder | Replay events count | Same |

### Pending Approvals / Clearance Queue
| Field | Current Source | Future Source |
|---|---|---|
| Incident list | `Sentinel_Incident__c` WHERE Approval_Status = 'Required' | Same + Zentom confidence scores |
| Risk badge | `Risk_Level__c` field | Zentom real-time risk scoring |
| Policy decision | `Zentom_Policy_Decision__c` | Zentom Policy Engine API |
| Recommended action | `Execution_Action__c` or `Runbook_Key__c` | Zentom AI recommendation |

### Recent Incidents Table
| Column | Current Source | Future Source |
|---|---|---|
| Incident name/link | `Sentinel_Incident__c.Name` | Same |
| Type | `Incident_Type__c` | Same |
| Environment | Hardcoded "Salesforce" | Future: multi-env detection |
| Risk | `Risk_Level__c` + `Risk_Score__c` | Zentom risk scoring |
| Policy | `Zentom_Policy_Decision__c` | Zentom Policy Engine |
| Status | `Status__c` | Same |
| Runbook | `Runbook_Key__c` | Same + runbook catalog link |
| Approval | `Approval_Status__c` | Same |
| Created | `CreatedDate` | Same |

### System Health Panel
| Field | Current Source | Future Source |
|---|---|---|
| Zentom API status | Hardcoded "Loaded" | Zentom Health API ping |
| Hosted DB status | Hardcoded "Not reported" | Zentom DB health check |
| Latest error log | Derived from failed count | `Sentinel_Error_Log__c` latest |
| Error count | Derived from incidents | Same + Zentom error aggregation |

### Replay Timeline
| Field | Current Source | Future Source |
|---|---|---|
| Event list | `Sentinel_Audit_Log__c` | Same + Zentom memory enrichment |
| Event type | `Event_Type__c` | Same |
| Decision badge | `Decision__c` | Same |
| Incident link | `Incident__c` lookup | Same |

## 8. Menu-by-Menu Data Mapping

| Menu Item | Current State | Data Source | Future Enhancement |
|---|---|---|---|
| Command Center | Live dashboard | `ZentomDashboardController` | Zentom real-time feed |
| Incidents | Record list | `Sentinel_Incident__c` list view | AI-prioritized list |
| Approvals | Live queue | `ZentomApprovalQueue` component | Zentom confidence + auto-approve |
| Actions | Placeholder | Mock data in shell | Execution history from incidents |
| Runbooks | Placeholder | Mock data in shell | `Zentom_Runbook__mdt` catalog |
| Policies | Placeholder | Mock data in shell | Policy engine configuration UI |
| Analytics | Placeholder | Mock data in shell | Zentom analytics API |

## 9. Future Backend Requirements

| Requirement | Priority | Dependency |
|---|---|---|
| Deploy `ZentomDashboardController.getDashboardData` to production | P0 | Apex class update |
| Create Named Credential for Zentom API | P1 | Zentom API deployed |
| Add Zentom health check callout to System Health panel | P1 | Named Credential |
| Wire approval queue to live `getPendingApprovals` (replace mock) | P1 | Backend API running |
| Add real-time risk scoring from Zentom Policy Engine | P2 | Policy Engine API |
| Add neural insights section to dashboard | P2 | Zentom AI Engine |
| Add runbook catalog browsing | P2 | Runbook metadata expansion |
| Add multi-environment support | P3 | External monitoring integrations |

## 10. Milestone 33 Completion Criteria

| Criteria | Status |
|---|---|
| Dashboard CSS is polished and consistent | ✅ 33B |
| Visual QA passes all 8 checklist items | ✅ 33C |
| CSS class coverage is 100% | ✅ 33C (79 instances, 0 unmatched) |
| Future data mapping is documented | ✅ 33D (this document) |
| Card-by-card mapping covers all sections | ✅ 33D |
| Menu-by-menu mapping covers all nav items | ✅ 33D |
| Backend requirements are prioritized | ✅ 33D |
| No Apex / backend / object changes made | ✅ Scope respected |
| All changes committed and pushed | ✅ 33A–33D |
