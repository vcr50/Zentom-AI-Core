# Zentom Suite

Zentom Suite is the monorepo for the Tomcodex Salesforce intelligence ecosystem.

## Final Product Rule

- Zentom AI = brain
- SentinelFlow = Salesforce monitoring app
- Agentforce = execution layer
- Salesforce = system of record
- Tomcodex = company

SentinelFlow is a Salesforce monitoring and incident intelligence app powered by Zentom AI.

## Repository Structure

```text
zentom-suite/
├── apps/
│   ├── sentinelflow-web/
│   ├── sentinelflow-salesforce/
│   └── zentom-admin-console/
├── services/
│   ├── zentom-api/
│   ├── zentom-ai-engine/
│   ├── zentom-policy-engine/
│   ├── zentom-memory-engine/
│   └── zentom-integration-engine/
├── packages/
│   ├── shared-types/
│   ├── shared-utils/
│   └── ui-components/
├── infra/
│   ├── docker/
│   ├── database/
│   └── deployment/
├── docs/
└── tests/
```

## Migrated Source

The existing `SentinelFlow` app has been copied into this monorepo by module:

- `apps/sentinelflow-web/`: migrated static SentinelFlow website
- `apps/sentinelflow-salesforce/`: migrated Salesforce metadata and manifests
- `services/zentom-api/legacy-sentinelflow-node/`: migrated existing Node API
- `services/zentom-ai-engine/legacy-zentom-ai/`: migrated existing Python Zentom AI service

See `docs/migration-map.md` for the source-to-destination map.

## First MVP Flow

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

## Migration Placement

- Existing website -> `apps/sentinelflow-web/`
- Existing Salesforce app -> `apps/sentinelflow-salesforce/`
- Backend code -> `services/zentom-api/`
- AI logic -> `services/zentom-ai-engine/`
- Risk/policy logic -> `services/zentom-policy-engine/`

## Local API Start

```powershell
cd services/zentom-api
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.
