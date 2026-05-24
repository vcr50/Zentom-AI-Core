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
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Most hosts should route external HTTPS traffic to container port `8000`.

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
