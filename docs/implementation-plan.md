# Zentom Suite Implementation Plan

## Decision

Build one monorepo named `zentom-suite`.

Keep all product modules inside it, separated by responsibility:

- `apps/`: user-facing apps and Salesforce package
- `services/`: backend, AI, policy, memory, and integration engines
- `packages/`: shared code
- `infra/`: database, Docker, and deployment assets
- `docs/`: architecture and setup documentation
- `tests/`: integration, security, and Salesforce tests

## Final Product Rule

- Zentom AI = brain
- SentinelFlow = Salesforce monitoring app
- Agentforce = execution layer
- Salesforce = system of record
- Tomcodex = company

## Migration Plan

1. Create `zentom-suite`.
2. Move or copy the existing SentinelFlow website into `apps/sentinelflow-web`.
3. Move or copy existing Salesforce metadata into `apps/sentinelflow-salesforce`.
4. Keep backend APIs in `services/zentom-api`.
5. Add Zentom engines one by one:
   - `zentom-policy-engine`
   - `zentom-ai-engine`
   - `zentom-memory-engine`
   - `zentom-integration-engine`
6. Use shared packages only when two or more modules need the same code.

## First Development Target

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

## Build Order

### Week 1

- Create monorepo
- Move existing website
- Set up backend API
- Set up database schema
- Set up Salesforce DX folder
- Create core docs

### Week 2

- Create `Sentinel_Incident__c`
- Create `Sentinel_Incident_Event__e`
- Create Apex publisher
- Send test incident to Zentom API
- Store incident in database

### Week 3

- Build rule-based incident analyzer
- Build risk engine
- Build policy engine
- Show incidents in dashboard

### Week 4

- Add AI recommendation
- Add confidence score
- Add approval-required logic
- Store model output

### Week 5

- Build Salesforce Case creation
- Build Task creation
- Build audit log
- Build Replay view

### Week 6

- Polish dashboard
- Add org health score
- Add setup wizard
- Prepare demo script
- Document security model
