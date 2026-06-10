# Zentom Memory Engine

Persistent memory, replay packets, and vector search for incident resolution patterns.

## Architecture

```
Incident → Memory Store → Vector Search → Similar Incidents
               ↓
          Replay Packet (audit trail)
               ↓
          Outcome Tracking (learning)
```

## Modules

| Module | Description |
|--------|-------------|
| `memory_store.py` | SQLite-backed memory store with search, stats, outcome tracking |
| `replay_engine.py` | ReplayPacket class with timeline, serialization, storage formatting |
| `vector_search.py` | TF-IDF similarity search + keyword matching (pgvector for production) |
| `main.py` | FastAPI service with REST endpoints |

## Memory Store Features

- **Store** incident memories with full context (type, risk, policy, outcome)
- **Search** by incident_type, risk_level, policy_decision, runbook_key, execution_status, outcome_status
- **Update outcomes** for learning loops
- **Statistics** — entry counts by type and outcome
- **SQLite** for dev, PostgreSQL + pgvector for production

## Replay Packet Structure

A ReplayPacket captures the full incident lifecycle:

1. **packet_created** — Initial incident captured
2. **classified** — AI classification result added
3. **risk_scored** — Risk assessment added
4. **recommended** — AI recommendation added
5. **policy_decided** — Policy decision added
6. **approved** — Approval result (if required)
7. **executed** — Action execution result
8. **verified** — Post-action verification

## Vector Search

- **TF-IDF similarity** — No external ML dependencies required
- **Cosine similarity** scoring between query and stored entries
- **Keyword search** — Simple exact-match fallback
- **Production upgrade** — Replace with sentence-transformers + pgvector

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `POST` | `/memory` | Store a memory entry |
| `GET` | `/memory/{id}` | Get entry by ID |
| `GET` | `/memory` | Search entries with filters |
| `PATCH` | `/memory/{id}/outcome` | Update execution outcome |
| `GET` | `/memory/stats` | Memory store statistics |
| `GET` | `/memory/count` | Count entries |
| `POST` | `/replay` | Build and store a replay packet |
| `POST` | `/search/similar` | TF-IDF similarity search |
| `POST` | `/search/keywords` | Keyword-based search |

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8004 --reload
# API docs: http://localhost:8004/docs
```

## Docker

```bash
docker build -t zentom-memory-engine .
docker run -p 8004:8004 zentom-memory-engine
```

## Source

🔗 [github.com/vcr50/salesforce-ops-monitoring-platform](https://github.com/vcr50/salesforce-ops-monitoring-platform)

