import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import MemoryEntry
from app.services.embedding_client import generate_embedding

logger = logging.getLogger(__name__)


def create_memory_entry(
    db: Session,
    *,
    source_type: str,
    source_id: str | None = None,
    incident_type: str | None = None,
    title: str | None = None,
    summary: str | None = None,
    root_cause: str | None = None,
    recommended_action: str | None = None,
    runbook_key: str | None = None,
    risk_level: str | None = None,
    policy_decision: str | None = None,
    execution_status: str | None = None,
    outcome_status: str | None = None,
    embedding_text: str | None = None,
    embedding_vector: list[float] | None = None,
    metadata_json: dict | None = None,
) -> MemoryEntry:
    entry = MemoryEntry(
        source_type=source_type,
        source_id=source_id,
        incident_type=incident_type,
        title=title,
        summary=summary,
        root_cause=root_cause,
        recommended_action=recommended_action,
        runbook_key=runbook_key,
        risk_level=risk_level,
        policy_decision=policy_decision,
        execution_status=execution_status,
        outcome_status=outcome_status,
        embedding_text=embedding_text,
        embedding_vector=embedding_vector,
        metadata_json=metadata_json or {},
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_memory_entries(db: Session, limit: int = 10) -> list[MemoryEntry]:
    return (
        db.query(MemoryEntry)
        .order_by(MemoryEntry.created_at.desc(), MemoryEntry.id.desc())
        .limit(limit)
        .all()
    )


def search_memory_entries(
    db: Session,
    incident_type: str | None = None,
    runbook_key: str | None = None,
    risk_level: str | None = None,
    query_text: str | None = None,
    limit: int = 5,
) -> list[MemoryEntry]:
    query = db.query(MemoryEntry)

    if incident_type:
        query = query.filter(MemoryEntry.incident_type == incident_type)

    if runbook_key:
        query = query.filter(MemoryEntry.runbook_key == runbook_key)

    if risk_level:
        query = query.filter(MemoryEntry.risk_level == risk_level)

    if query_text:
        query = query.filter(MemoryEntry.embedding_text.ilike(f"%{query_text}%"))

    return (
        query
        .order_by(MemoryEntry.created_at.desc(), MemoryEntry.id.desc())
        .limit(limit)
        .all()
    )


def build_memory_context(memories: list[MemoryEntry]) -> str:
    if not memories:
        return "No similar memory entries found."

    blocks = []

    for memory in memories:
        blocks.append(f"""
Memory ID: {memory.id}
Incident Type: {memory.incident_type}
Risk Level: {memory.risk_level}
Policy Decision: {memory.policy_decision}
Runbook: {memory.runbook_key}
Summary: {memory.summary}
Root Cause: {memory.root_cause}
Recommended Action: {memory.recommended_action}
Outcome: {memory.outcome_status}
""".strip())

    return "\n---\n".join(blocks)


def search_similar_memories(
    db: Session,
    query_text: str,
    limit: int = 3,
    similarity_threshold: float = 0.30,
) -> dict:
    """Search memory entries by vector cosine similarity.

    Falls back to keyword search if embedding generation fails.
    Only works on PostgreSQL with pgvector.
    """
    query_embedding = generate_embedding(query_text)

    if query_embedding is None:
        logger.info("Embedding unavailable, falling back to keyword search.")
        memories = search_memory_entries(db, query_text=query_text, limit=limit)
        return {
            "searchMethod": "keyword",
            "memories": memories,
        }

    try:
        vector_literal = "[" + ",".join(str(v) for v in query_embedding) + "]"

        stmt = text(
            "SELECT id, 1 - (embedding_vector <=> CAST(:vec AS vector)) AS similarity "
            "FROM memory_entries "
            "WHERE embedding_vector IS NOT NULL "
            "AND 1 - (embedding_vector <=> CAST(:vec AS vector)) >= :threshold "
            "ORDER BY embedding_vector <=> CAST(:vec AS vector) "
            "LIMIT :lim"
        )

        rows = db.execute(
            stmt,
            {"vec": vector_literal, "threshold": similarity_threshold, "lim": limit},
        ).fetchall()

        if not rows:
            return {
                "searchMethod": "vector",
                "memories": [],
            }

        ids = [row[0] for row in rows]
        memories = (
            db.query(MemoryEntry)
            .filter(MemoryEntry.id.in_(ids))
            .all()
        )

        # Preserve similarity ranking order
        id_order = {mid: idx for idx, mid in enumerate(ids)}
        memories.sort(key=lambda m: id_order.get(m.id, 999))
        return {
            "searchMethod": "vector",
            "memories": memories,
        }

    except Exception as exc:
        logger.warning("Vector search failed, falling back to keyword: %s", exc)
        memories = search_memory_entries(db, query_text=query_text, limit=limit)
        return {
            "searchMethod": "keyword",
            "memories": memories,
        }


def backfill_embeddings(db: Session) -> dict:
    """Generate embeddings for all memory entries that don't have one yet."""
    entries = (
        db.query(MemoryEntry)
        .filter(
            MemoryEntry.embedding_vector.is_(None),
            MemoryEntry.embedding_text.isnot(None),
        )
        .all()
    )

    updated = 0
    failed = 0

    for entry in entries:
        try:
            embedding = generate_embedding(entry.embedding_text)
        except Exception as exc:
            logger.warning("Embedding backfill failed for memory %s: %s", entry.id, exc)
            embedding = None

        if embedding is not None:
            entry.embedding_vector = embedding
            updated += 1
        else:
            failed += 1

    if updated > 0:
        db.commit()

    return {
        "scanned": len(entries),
        "updated": updated,
        "failed": failed,
    }


def build_incident_memory_text(
    payload: dict,
    risk: dict,
    policy: dict,
    recommendation: dict,
) -> str:
    return f"""
Incident Type: {payload.get("incidentType")}
Source: {payload.get("source")}
Environment: {payload.get("environment")}
Error Message: {payload.get("errorMessage")}

Risk Level: {risk.get("riskLevel")}
Risk Score: {risk.get("totalScore")}

Policy Decision: {policy.get("decision")}
Policy Reason: {policy.get("reason")}

AI Summary: {recommendation.get("summary")}
Root Cause: {recommendation.get("rootCause")}
Recommended Action: {recommendation.get("recommendedAction")}
Runbook: {recommendation.get("runbookKey")}
""".strip()


def create_incident_memory(
    db: Session,
    incident_id: int,
    payload: dict,
    risk: dict,
    policy: dict,
    recommendation: dict,
) -> MemoryEntry:
    embedding_text = build_incident_memory_text(payload, risk, policy, recommendation)

    try:
        embedding_vector = generate_embedding(embedding_text)
    except Exception as exc:
        logger.warning("Embedding generation failed during memory creation: %s", exc)
        embedding_vector = None

    return create_memory_entry(
        db=db,
        source_type="INCIDENT",
        source_id=str(incident_id),
        incident_type=payload.get("incidentType"),
        title=f"{payload.get('incidentType')} - {risk.get('riskLevel')}",
        summary=recommendation.get("summary"),
        root_cause=recommendation.get("rootCause"),
        recommended_action=recommendation.get("recommendedAction"),
        runbook_key=recommendation.get("runbookKey"),
        risk_level=risk.get("riskLevel"),
        policy_decision=policy.get("decision"),
        execution_status="Not Started",
        outcome_status="Unknown",
        embedding_text=embedding_text,
        embedding_vector=embedding_vector,
        metadata_json={
            "payload": payload,
            "risk": risk,
            "policy": policy,
            "recommendation": recommendation,
        },
    )
