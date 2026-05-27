# Zentom AI Trace Contract

This document defines the `aiTrace` object returned by the Zentom API during incident processing (`/api/incidents/receive`). It exposes the AI's reasoning, confidence, and contextual logic without exposing unsafe or private chain-of-thought data.

## `aiTrace` Payload Schema

```json
{
  "aiTrace": {
    "aiReasoningStatus": "ACTIVE",
    "aiConfidenceScore": 87,
    "aiExplanation": "Zentom identified this as a critical Flow failure because the owner field is missing in a production workflow.",
    "riskReason": "Critical risk because the incident indicates a production flow failure with business process impact.",
    "policyReason": "Human approval is required because the risk level is CRITICAL.",
    "runbookReason": "FLOW_FAILURE_BASIC_RECOVERY was selected because the incident type is FLOW_FAILURE.",
    "memoryUsed": true,
    "orchestrationMode": "HYBRID",
    "brainVersion": "zentom-brain-v1"
  }
}
```

## Field Definitions

| Field | Type | Description |
|---|---|---|
| `aiReasoningStatus` | `string` | Status of the AI generation (`ACTIVE`, `RULE_ONLY`, or `FALLBACK`). |
| `aiConfidenceScore` | `integer` | Confidence level of the recommendation (0-100). |
| `aiExplanation` | `string` | Safe, human-readable explanation of why the incident occurred and why the recommendation was chosen. |
| `riskReason` | `string` | Explanation of why the incident received its calculated Risk Level. |
| `policyReason` | `string` | Explanation of why a specific governance policy (e.g., Human Approval) was applied. |
| `runbookReason` | `string` | Explanation of why the specific runbook was selected. |
| `memoryUsed` | `boolean` | Indicates whether past resolutions (memory) were injected into the context. |
| `orchestrationMode` | `string` | The current operating mode (`LLM`, `HYBRID`, or `RULE`). |
| `brainVersion` | `string` | The version of the Zentom Brain Engine used. |

## Safety Guarantee

The fields exposed in this trace provide visibility into the decision-making process for the SentinelFlow UI without exposing internal prompt structures, raw rule logic, or unvetted chain-of-thought outputs.
