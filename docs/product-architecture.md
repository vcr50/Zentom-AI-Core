# Product Architecture

## Product Roles

- Tomcodex is the company.
- Zentom AI is the brain.
- SentinelFlow is the Salesforce monitoring app.
- Agentforce is the execution layer.
- Salesforce is the system of record.

## High-Level Flow

```text
Salesforce incident
  -> Zentom API receive
  -> Store in database
  -> Risk score
  -> AI recommendation
  -> Policy decision
  -> Dashboard display
  -> Replay log
```

## Core Modules

### SentinelFlow Web

The product website and dashboard frontend.

### SentinelFlow Salesforce

Salesforce package metadata, Apex, Lightning Web Components, objects, flows, permission sets, and platform events.

### Zentom API

Public backend entry point for incidents, recommendations, risk scoring, approvals, and dashboard data.

### Zentom AI Engine

Classification, root cause analysis, recommendation generation, prompt management, and confidence scoring.

### Zentom Policy Engine

Risk scoring, policy decisions, approval requirements, and action allowlists.

### Zentom Memory Engine

Incident memory, replay records, embeddings, similar incident search, and learning loops.

#### Milestone 13F Verification

- `all-minilm` embeddings are stored as 384-dim pgvector values.
- pgvector similarity search was verified with `searchMethod = vector`.
- Query `owner field is null` returned related `FLOW_FAILURE` memories.
- New memory row `10` was verified with a populated 384-dim embedding.
- On Windows, `uvicorn --reload` can hit a multiprocessing permission issue in this shell; non-reload Uvicorn was verified on port `8011`.

### Zentom Integration Engine

Salesforce API, Agentforce action calls, webhooks, and external integration clients.
