from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db, init_database
from app.services.dataset_service import (
    SUPPORTED_DATASET_FORMATS,
    dataset_to_jsonl,
    export_dataset,
)
from app.services.incident_service import process_incident
from app.services.memory_service import (
    backfill_embeddings,
    build_memory_context,
    search_memory_entries,
    search_similar_memories,
)

app = FastAPI(
    title="Zentom API",
    description="Core API for Zentom AI and SentinelFlow",
    version="0.1.0",
)


@app.on_event("startup")
def startup() -> None:
    init_database()


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "zentom-api",
        "message": "Zentom API is ready",
    }


@app.post("/api/incidents/receive")
def receive_incident(payload: dict, db: Session = Depends(get_db)):
    return process_incident(payload, db)


@app.get("/api/memory/search")
def search_memory(
    incident_type: str | None = None,
    runbook_key: str | None = None,
    risk_level: str | None = None,
    query_text: str | None = None,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    memories = search_memory_entries(
        db=db,
        incident_type=incident_type,
        runbook_key=runbook_key,
        risk_level=risk_level,
        query_text=query_text,
        limit=limit,
    )

    return {
        "count": len(memories),
        "memories": [to_memory_response(memory) for memory in memories],
    }


@app.get("/api/memory/context-preview")
def memory_context_preview(
    incident_type: str | None = None,
    runbook_key: str | None = None,
    risk_level: str | None = None,
    query_text: str | None = None,
    limit: int = 3,
    db: Session = Depends(get_db),
):
    memories = search_memory_entries(
        db=db,
        incident_type=incident_type,
        runbook_key=runbook_key,
        risk_level=risk_level,
        query_text=query_text,
        limit=limit,
    )

    return {
        "matchCount": len(memories),
        "contextInjected": len(memories) > 0,
        "memoryContext": build_memory_context(memories),
    }


@app.get("/api/memory/similar")
def similar_memory(
    query: str,
    limit: int = 3,
    db: Session = Depends(get_db),
):
    result = search_similar_memories(
        db=db,
        query_text=query,
        limit=limit,
    )
    memories = result["memories"]

    return {
        "count": len(memories),
        "query": query,
        "searchMethod": result["searchMethod"],
        "memories": [to_memory_response(memory) for memory in memories],
    }


@app.post("/api/memory/backfill-embeddings")
def run_backfill_embeddings(db: Session = Depends(get_db)):
    result = backfill_embeddings(db)
    return {
        "message": "Embedding backfill complete",
        **result,
    }


@app.get("/api/dataset/export")
def get_export_dataset(
    format: str = "alpaca",
    db: Session = Depends(get_db),
):
    export_format = format.lower()

    if export_format not in SUPPORTED_DATASET_FORMATS:
        raise HTTPException(
            status_code=400,
            detail="Supported dataset export formats: alpaca, jsonl.",
        )

    dataset = export_dataset(db, format=export_format)

    if export_format == "jsonl":
        return Response(
            content=dataset_to_jsonl(dataset),
            media_type="application/x-ndjson",
        )

    return {
        "format": export_format,
        "count": len(dataset),
        "dataset": dataset,
    }


@app.get("/api/dataset/export-jsonl")
def get_export_dataset_jsonl(db: Session = Depends(get_db)):
    dataset = export_dataset(db, format="jsonl")
    return Response(
        content=dataset_to_jsonl(dataset),
        media_type="application/x-ndjson",
    )


def to_memory_response(memory) -> dict:
    return {
        "id": memory.id,
        "sourceType": memory.source_type,
        "sourceId": memory.source_id,
        "incidentType": memory.incident_type,
        "runbookKey": memory.runbook_key,
        "riskLevel": memory.risk_level,
        "summary": memory.summary,
    }
