# Docker

Local development Docker Compose files live here.

## Milestone 13A: PostgreSQL + pgvector

Current local setup uses the existing running container:

```text
Container: zentom-pgvector
Database: zentom_db
User: zentom_user
Password: zentom_password
Port: 5432
```

Zentom API local database URL:

```env
DATABASE_URL=postgresql://zentom_user:zentom_password@localhost:5432/zentom_db
```

Verify pgvector:

```powershell
docker exec zentom-pgvector psql -U zentom_user -d zentom_db -c "CREATE EXTENSION IF NOT EXISTS vector; SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

## Optional Fresh Compose Stack

Start Docker Desktop first, then run from the repository root:

```powershell
docker compose -f infra\docker\docker-compose.local.yml up -d postgres
```

PostgreSQL settings:

```text
Database: zentom_db
User: zentom
Password: zentom_dev
Host port: 5433
Container port: 5432
```

The data directory is stored on the D drive under:

```text
D:\TomCodeX Inc\zentom-suite\.docker-data\postgres
```

Fresh compose database URL:

```env
DATABASE_URL=postgresql://zentom:zentom_dev@localhost:5433/zentom_db
```

Verify pgvector after the container is healthy:

```powershell
docker compose -f infra\docker\docker-compose.local.yml exec postgres psql -U zentom -d zentom_db -c "CREATE EXTENSION IF NOT EXISTS vector; SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

## Milestone 16: Dockerized Zentom API

The local compose stack can also run the FastAPI service:

```powershell
docker compose -f infra\docker\docker-compose.local.yml up -d --build zentom-api
```

The API container uses the compose Postgres service:

```env
DATABASE_URL=postgresql://zentom:zentom_dev@postgres:5432/zentom_db
```

On Windows Docker Desktop, the API container reaches host Ollama through:

```env
LOCAL_LLM_URL=http://host.docker.internal:11434
LOCAL_LLM_MODEL=phi3:mini
EMBEDDING_MODEL=all-minilm
```

The container listens on port `8000`; the host maps it to `8012` to avoid conflicts with the local non-Docker API on `8011`.

Verify:

```powershell
curl http://127.0.0.1:8012/
curl http://127.0.0.1:8012/docs
curl "http://127.0.0.1:8012/api/memory/similar?query=owner%20field%20is%20null&limit=3"
curl "http://127.0.0.1:8012/api/dataset/export?format=alpaca"
```
