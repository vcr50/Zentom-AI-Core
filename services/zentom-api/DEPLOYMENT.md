# Zentom API Deployment

## Milestone 17A: Online API In RULE Mode

First hosted deployment should prove the Salesforce-to-Zentom API path without hosted AI complexity.

Target flow:

```text
Salesforce -> Hosted Zentom API -> Risk -> Policy -> Rule Recommendation -> Salesforce write-back
```

Do not deploy Ollama for the first online beta.

## Required Environment

Use `services/zentom-api/.env.production.example` as the production template.

```env
APP_ENV=production
DATABASE_URL=
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_API_KEY=
AI_MODEL=zentom-rule-v1
LOCAL_LLM_URL=
LOCAL_LLM_MODEL=
EMBEDDING_MODEL=all-minilm
```

`AI_MODE=RULE` disables local LLM calls and avoids any dependency on GPU, Ollama, or paid LLM providers.

## Docker Entrypoint

The API image starts with:

```text
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Render provides `PORT` dynamically. Local Docker runs fall back to `8000`.

## Health Checks

Use:

```text
GET /
GET /docs
```

Expected health response:

```json
{
  "status": "running",
  "service": "zentom-api",
  "message": "Zentom API is ready"
}
```

## Recommended 17A Platform Path

1. Push repo to GitHub.
2. Create a Docker web service on Render, Railway, or Fly.io.
3. Point the service at `services/zentom-api/Dockerfile`.
4. Set production env vars from `.env.production.example`.
5. Deploy in `AI_MODE=RULE`.
6. Verify `/` and `/docs`.

## Later Milestones

- 17B: Update Salesforce `Zentom_Setting__mdt.Base_URL__c` to the hosted API URL.
- 17C: Add hosted PostgreSQL.
- 17D: Decide hosted/local model strategy later.

## Milestone 17C: Hosted PostgreSQL Hardening

Use Neon Postgres first for the hosted beta database.

Render environment variables:

```env
DATABASE_URL=<neon-postgres-connection-url>
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_API_KEY=
AI_MODEL=zentom-rule-v1
LOCAL_LLM_URL=
LOCAL_LLM_MODEL=
EMBEDDING_MODEL=all-minilm
```

Use the Neon connection string with the password revealed and copied from the Neon dashboard. Keep the value private and store it only in Render environment variables or a local uncommitted `.env` file.

On startup the API:

1. Connects to `DATABASE_URL`.
2. Runs `CREATE EXTENSION IF NOT EXISTS vector` for PostgreSQL.
3. Creates required tables with SQLAlchemy if they do not exist.

Required hosted tables:

- `incidents`
- `risk_scores`
- `policy_decisions`
- `ai_recommendations`
- `memory_entries`

Production-safe verification endpoint:

```text
GET /api/health/db
```

Expected hosted response:

```json
{
  "status": "ok",
  "databaseType": "postgresql",
  "databaseConfigured": true,
  "missingTables": [],
  "pgvector": {
    "enabled": true,
    "status": "enabled"
  }
}
```

If the hosted database does not support pgvector, keep vector/RAG memory features local and continue hosted beta in `AI_MODE=RULE`. Neon and Supabase generally support pgvector; Render Postgres support should be verified before relying on hosted vector search.

Recommended 17C validation:

1. Set `DATABASE_URL` in Render.
2. Redeploy the Zentom API service.
3. Verify `GET /api/health/db`.
4. POST a hosted incident to `/api/incidents/receive`.
5. Re-run Salesforce anonymous Apex and confirm Salesforce write-back.

Backup/export plan for beta:

- Use Neon dashboard backups/restore points where available.
- Keep `GET /api/dataset/export?format=alpaca` and `format=jsonl` as lightweight memory dataset exports.
- Before schema changes, export datasets and record table counts from `/api/health/db`.
