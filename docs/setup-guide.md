# Setup Guide

## Final Structure

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
    ├── integration/
    ├── security/
    └── salesforce/
```

## 1. Backend API

The forward API scaffold is FastAPI:

```powershell
cd services/zentom-api
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check:

```text
http://127.0.0.1:8000
```

The migrated SentinelFlow Node service is preserved at:

```text
services/zentom-api/legacy-sentinelflow-node/
```

To run the legacy Node service:

```powershell
cd services/zentom-api/legacy-sentinelflow-node
npm install
npm run dev
```

## 2. Database

Create PostgreSQL database:

```powershell
createdb zentom_db
```

Apply schema from:

```text
infra/database/schema.sql
```

## 3. Salesforce App

Salesforce metadata lives in:

```text
apps/sentinelflow-salesforce/
```

Use Salesforce DX commands from that folder.

## 4. Web App

SentinelFlow website and dashboard live in:

```text
apps/sentinelflow-web/
```

The current migrated website is static HTML/CSS/JS from `SentinelFlow/website`.

If this becomes a React/Vite app:

```powershell
npm install
npm run dev
```

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
