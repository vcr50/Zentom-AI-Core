"""
Zentom Memory Engine — FastAPI Service

REST API endpoints for:
  - Memory entry storage and retrieval
  - Replay packet creation and management
  - Vector/keyword similarity search
  - Memory statistics
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .memory_store import MemoryStore, get_store
from .replay_engine import ReplayPacket, build_replay_packet_object
from .vector_search import VectorSearch, get_search

app = FastAPI(
    title="Zentom Memory Engine",
    version="1.0.0",
    description="Persistent memory, replay, and vector search",
)


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class MemoryEntryInput(BaseModel):
    source_type: str = Field(default="incident", description="Entry type")
    source_id: Optional[str] = None
    incident_type: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    root_cause: Optional[str] = None
    recommended_action: Optional[str] = None
    runbook_key: Optional[str] = None
    risk_level: Optional[str] = None
    policy_decision: Optional[str] = None
    execution_status: Optional[str] = None
    outcome_status: Optional[str] = None
    confidence_score: Optional[int] = None
    embedding_text: Optional[str] = None
    metadata_json: Optional[dict] = None


class ReplayPacketInput(BaseModel):
    incident: dict
    classification: Optional[dict] = None
    risk_score: Optional[dict] = None
    recommendation: Optional[dict] = None
    policy_decision: Optional[dict] = None
    approval: Optional[dict] = None


class SearchQuery(BaseModel):
    query: str = Field(description="Search query text")
    incident_type: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)
    min_similarity: float = Field(default=0.1, ge=0.0, le=1.0)


class KeywordSearchQuery(BaseModel):
    keywords: list[str] = Field(description="Keywords to search for")
    incident_type: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)


class OutcomeUpdateRequest(BaseModel):
    execution_status: str
    outcome_status: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "service": "zentom-memory-engine",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


# --- Memory Store ---

@app.post("/memory")
async def store_memory(entry: MemoryEntryInput):
    """Store a new memory entry."""
    store = get_store()
    result = store.store(entry.model_dump())
    return result


@app.get("/memory/{entry_id}")
async def get_memory(entry_id: int):
    """Retrieve a memory entry by ID."""
    store = get_store()
    result = store.get(entry_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")
    return result


@app.get("/memory")
async def search_memory(
    incident_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    policy_decision: Optional[str] = None,
    runbook_key: Optional[str] = None,
    execution_status: Optional[str] = None,
    outcome_status: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """Search memory entries with filters."""
    store = get_store()
    results = store.search(
        incident_type=incident_type,
        risk_level=risk_level,
        policy_decision=policy_decision,
        runbook_key=runbook_key,
        execution_status=execution_status,
        outcome_status=outcome_status,
        limit=limit,
        offset=offset,
    )
    return {"count": len(results), "entries": results}


@app.patch("/memory/{entry_id}/outcome")
async def update_outcome(entry_id: int, request: OutcomeUpdateRequest):
    """Update execution and outcome status of a memory entry."""
    store = get_store()
    success = store.update_outcome(entry_id, request.execution_status, request.outcome_status)
    if not success:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")
    return {"message": "Outcome updated", "entry_id": entry_id}


@app.get("/memory/stats")
async def memory_stats():
    """Get memory store statistics."""
    store = get_store()
    return store.get_stats()


@app.get("/memory/count")
async def memory_count(incident_type: Optional[str] = None):
    """Count memory entries."""
    store = get_store()
    return {"count": store.count(incident_type)}


# --- Replay Packets ---

@app.post("/replay")
async def create_replay_packet(packet: ReplayPacketInput):
    """Build and store a replay packet."""
    replay = build_replay_packet_object(
        incident=packet.incident,
        classification=packet.classification,
        risk_score=packet.risk_score,
        recommendation=packet.recommendation,
        policy_decision=packet.policy_decision,
    )
    if packet.approval:
        replay.add_approval(packet.approval)

    # Store in memory
    store = get_store()
    storage_dict = replay.to_storage_dict()
    store_result = store.store(storage_dict)

    return {
        "packet_id": replay.packet_id,
        "status": "stored",
        "memory_id": store_result.get("id"),
        "event_count": len(replay.timeline),
        "timestamp": datetime.utcnow().isoformat(),
    }


# --- Vector Search ---

@app.post("/search/similar")
async def search_similar(query: SearchQuery):
    """Find similar incidents using TF-IDF similarity."""
    search = get_search()
    results = search.find_similar(
        query=query.query,
        incident_type=query.incident_type,
        limit=query.limit,
        min_similarity=query.min_similarity,
    )
    return {"count": len(results), "results": results}


@app.post("/search/keywords")
async def search_keywords(query: KeywordSearchQuery):
    """Find incidents by keyword matching."""
    search = get_search()
    results = search.find_by_keywords(
        keywords=query.keywords,
        incident_type=query.incident_type,
        limit=query.limit,
    )
    return {"count": len(results), "results": results}
