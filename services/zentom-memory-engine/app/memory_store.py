"""
Zentom Memory Engine — Memory Store

Persistent storage for incident memories, replay records, and resolution patterns.
Provides in-memory store (dev) with SQLite/PostgreSQL backend support.

Memory entries store:
  - Incident context and classification
  - AI recommendations and confidence scores
  - Policy decisions and outcomes
  - Execution results and verification status
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import json
import sqlite3
import os


class MemoryEntryType(str, Enum):
    INCIDENT = "incident"
    RECOMMENDATION = "recommendation"
    POLICY_DECISION = "policy_decision"
    EXECUTION_RESULT = "execution_result"
    VERIFICATION = "verification"
    CHAT_MESSAGE = "chat_message"


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class OutcomeStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    UNKNOWN = "unknown"


class MemoryStore:
    """
    Persistent memory store for incident resolution patterns.

    Supports:
      - Store and retrieve memory entries
      - Search by incident type, risk level, policy decision
      - Track execution outcomes for learning
      - SQLite for dev, PostgreSQL + pgvector for production
    """

    def __init__(self, db_path: str = "zentom_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database schema."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_type TEXT NOT NULL,
                source_id TEXT,
                incident_type TEXT,
                title TEXT,
                summary TEXT,
                root_cause TEXT,
                recommended_action TEXT,
                runbook_key TEXT,
                risk_level TEXT,
                policy_decision TEXT,
                execution_status TEXT,
                outcome_status TEXT,
                confidence_score INTEGER,
                embedding_text TEXT,
                metadata_json TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_incident_type ON memory_entries(incident_type)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_risk_level ON memory_entries(risk_level)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_runbook_key ON memory_entries(runbook_key)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_policy_decision ON memory_entries(policy_decision)")
        conn.commit()
        conn.close()

    def store(self, entry: dict) -> dict:
        """
        Store a memory entry.

        Args:
            entry: Dict with memory fields (source_type, incident_type, summary, etc.)

        Returns:
            Dict with id, status, and timestamp
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            INSERT INTO memory_entries (
                source_type, source_id, incident_type, title, summary,
                root_cause, recommended_action, runbook_key, risk_level,
                policy_decision, execution_status, outcome_status,
                confidence_score, embedding_text, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.get("source_type", "incident"),
            entry.get("source_id"),
            entry.get("incident_type"),
            entry.get("title"),
            entry.get("summary"),
            entry.get("root_cause"),
            entry.get("recommended_action"),
            entry.get("runbook_key"),
            entry.get("risk_level"),
            entry.get("policy_decision"),
            entry.get("execution_status"),
            entry.get("outcome_status"),
            entry.get("confidence_score"),
            entry.get("embedding_text"),
            json.dumps(entry.get("metadata_json", {})) if isinstance(entry.get("metadata_json"), dict) else entry.get("metadata_json"),
        ))
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "id": entry_id,
            "status": "stored",
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get(self, entry_id: int) -> dict | None:
        """Retrieve a memory entry by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM memory_entries WHERE id = ?", (entry_id,)).fetchone()
        conn.close()

        if not row:
            return None

        result = dict(row)
        if result.get("metadata_json"):
            try:
                result["metadata_json"] = json.loads(result["metadata_json"])
            except json.JSONDecodeError:
                pass
        return result

    def search(
        self,
        incident_type: str | None = None,
        risk_level: str | None = None,
        policy_decision: str | None = None,
        runbook_key: str | None = None,
        execution_status: str | None = None,
        outcome_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """Search memory entries with filters."""
        conditions = []
        params = []

        if incident_type:
            conditions.append("incident_type = ?")
            params.append(incident_type)
        if risk_level:
            conditions.append("risk_level = ?")
            params.append(risk_level)
        if policy_decision:
            conditions.append("policy_decision = ?")
            params.append(policy_decision)
        if runbook_key:
            conditions.append("runbook_key = ?")
            params.append(runbook_key)
        if execution_status:
            conditions.append("execution_status = ?")
            params.append(execution_status)
        if outcome_status:
            conditions.append("outcome_status = ?")
            params.append(outcome_status)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM memory_entries WHERE {where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()
        conn.close()

        results = []
        for row in rows:
            result = dict(row)
            if result.get("metadata_json"):
                try:
                    result["metadata_json"] = json.loads(result["metadata_json"])
                except json.JSONDecodeError:
                    pass
            results.append(result)
        return results

    def update_outcome(self, entry_id: int, execution_status: str, outcome_status: str) -> bool:
        """Update the execution and outcome status of a memory entry."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            UPDATE memory_entries
            SET execution_status = ?, outcome_status = ?, updated_at = datetime('now')
            WHERE id = ?
        """, (execution_status, outcome_status, entry_id))
        affected = conn.total_changes
        conn.commit()
        conn.close()
        return affected > 0

    def count(self, incident_type: str | None = None) -> int:
        """Count memory entries, optionally filtered by type."""
        conn = sqlite3.connect(self.db_path)
        if incident_type:
            row = conn.execute("SELECT COUNT(*) FROM memory_entries WHERE incident_type = ?", (incident_type,)).fetchone()
        else:
            row = conn.execute("SELECT COUNT(*) FROM memory_entries").fetchone()
        conn.close()
        return row[0] if row else 0

    def get_stats(self) -> dict:
        """Get memory store statistics."""
        conn = sqlite3.connect(self.db_path)
        total = conn.execute("SELECT COUNT(*) FROM memory_entries").fetchone()[0]
        by_type = conn.execute("""
            SELECT incident_type, COUNT(*) as cnt FROM memory_entries
            WHERE incident_type IS NOT NULL GROUP BY incident_type
        """).fetchall()
        by_outcome = conn.execute("""
            SELECT outcome_status, COUNT(*) as cnt FROM memory_entries
            WHERE outcome_status IS NOT NULL GROUP BY outcome_status
        """).fetchall()
        conn.close()

        return {
            "total_entries": total,
            "by_incident_type": {row[0]: row[1] for row in by_type},
            "by_outcome": {row[0]: row[1] for row in by_outcome},
        }


# Global store instance (lazy init)
_store: MemoryStore | None = None


def get_store(db_path: str = "zentom_memory.db") -> MemoryStore:
    """Get or create the global MemoryStore instance."""
    global _store
    if _store is None or _store.db_path != db_path:
        _store = MemoryStore(db_path)
    return _store


def store_replay_record(record: dict) -> dict:
    """Backward-compatible function to store a replay record."""
    store = get_store()
    return store.store(record)

