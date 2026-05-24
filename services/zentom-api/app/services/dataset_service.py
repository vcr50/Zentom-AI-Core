import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import MemoryEntry

SUPPORTED_DATASET_FORMATS = {"alpaca", "jsonl"}


def export_dataset(db: Session, format: str = "alpaca") -> list[dict]:
    """
    Exports Zentom memories into dataset formats for LLM instruction tuning.
    """
    if format.lower() not in SUPPORTED_DATASET_FORMATS:
        return []

    # 14B - Dataset selection rule
    memories = (
        db.query(MemoryEntry)
        .filter(
            MemoryEntry.source_type == "INCIDENT",
            MemoryEntry.summary.isnot(None),
            MemoryEntry.root_cause.isnot(None),
            MemoryEntry.recommended_action.isnot(None),
        )
        .order_by(MemoryEntry.created_at.desc())
        .all()
    )

    dataset = []

    for memory in memories:
        meta = memory.metadata_json or {}
        payload = meta.get("payload", {})

        # 14C - Alpaca output format
        instruction = (
            "You are Zentom AI. Analyze the following Salesforce incident and recommend a safe resolution. "
            "You must not override policy, risk, approval, or runbook safety controls."
        )

        input_text = (
            f"Incident Type: {memory.incident_type}\n"
            f"Risk Level: {memory.risk_level}\n"
            f"Policy Decision: {memory.policy_decision}\n"
            f"Runbook: {memory.runbook_key}\n"
            f"Incident Context: {json.dumps(payload)}"
        )

        output_json = {
            "summary": memory.summary,
            "rootCause": memory.root_cause,
            "recommendedAction": memory.recommended_action,
            "confidenceScore": meta.get("recommendation", {}).get("confidenceScore", 80),
            "runbookKey": memory.runbook_key,
        }

        dataset.append(
            {
                "instruction": instruction,
                "input": input_text.strip(),
                "output": json.dumps(output_json, separators=(",", ":")),
            }
        )

    return dataset


def dataset_to_jsonl(dataset: list[dict]) -> str:
    return "\n".join(json.dumps(record, separators=(",", ":")) for record in dataset)


def save_dataset_json(dataset: list[dict], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    return path
