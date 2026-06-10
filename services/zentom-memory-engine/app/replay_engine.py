"""
Zentom Memory Engine — Replay Engine

Builds and manages replay packets for incident audit trails.
Replay packets capture the full decision chain for compliance,
debugging, and learning from past incidents.

Replay packet structure:
  - Incident context (what happened)
  - AI analysis (what the AI recommended)
  - Risk assessment (how risky it was)
  - Policy decision (what was allowed/blocked)
  - Execution result (what actually happened)
  - Verification outcome (did it work)
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import json
import hashlib


class ReplayStatus(str, Enum):
    CREATED = "created"
    STORED = "stored"
    REPLAYED = "replayed"
    ARCHIVED = "archived"


class ReplayPacket:
    """
    A complete replay packet capturing the full incident lifecycle.

    Attributes:
        packet_id: Unique identifier (hash of incident + timestamp)
        incident: Raw incident data
        classification: AI classification output
        risk_score: Risk engine output
        recommendation: AI recommendation output
        policy_decision: Policy engine output
        approval: Approval workflow output (if applicable)
        execution_result: What happened when action was taken
        verification: Post-action verification result
        timeline: Ordered list of events with timestamps
    """

    def __init__(
        self,
        incident: dict,
        classification: dict | None = None,
        risk_score: dict | None = None,
        recommendation: dict | None = None,
        policy_decision: dict | None = None,
        approval: dict | None = None,
    ):
        self.incident = incident
        self.classification = classification
        self.risk_score = risk_score
        self.recommendation = recommendation
        self.policy_decision = policy_decision
        self.approval = approval
        self.execution_result: dict | None = None
        self.verification: dict | None = None
        self.timeline: list[dict] = []
        self.created_at = datetime.utcnow()
        self.status = ReplayStatus.CREATED.value

        # Generate packet ID
        raw = json.dumps(incident, sort_keys=True, default=str) + self.created_at.isoformat()
        self.packet_id = hashlib.sha256(raw.encode()).hexdigest()[:16]

        # Add initial timeline event
        self._add_event("packet_created", "Replay packet created for incident")

    def _add_event(self, event_type: str, description: str, data: dict | None = None):
        """Add an event to the timeline."""
        self.timeline.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "description": description,
            "data": data or {},
        })

    def add_classification(self, classification: dict):
        """Add classification result to the packet."""
        self.classification = classification
        self._add_event(
            "classified",
            f"Incident classified as {classification.get('incident_type', 'unknown')}",
            {"confidence": classification.get("confidence_score")},
        )

    def add_risk_score(self, risk_score: dict):
        """Add risk assessment to the packet."""
        self.risk_score = risk_score
        self._add_event(
            "risk_scored",
            f"Risk score: {risk_score.get('total_score', 'N/A')} ({risk_score.get('risk_level', 'unknown')})",
            {"total_score": risk_score.get("total_score")},
        )

    def add_recommendation(self, recommendation: dict):
        """Add AI recommendation to the packet."""
        self.recommendation = recommendation
        self._add_event(
            "recommended",
            f"Action recommended: {recommendation.get('recommended_action', 'unknown')}",
            {"confidence": recommendation.get("confidence_score")},
        )

    def add_policy_decision(self, decision: dict):
        """Add policy decision to the packet."""
        self.policy_decision = decision
        self._add_event(
            "policy_decided",
            f"Policy decision: {decision.get('decision', 'unknown')}",
            {"requires_approval": decision.get("requires_approval")},
        )

    def add_approval(self, approval: dict):
        """Add approval result to the packet."""
        self.approval = approval
        self._add_event(
            "approved",
            f"Approval: {approval.get('status', 'unknown')} by {approval.get('approver', 'system')}",
        )

    def add_execution_result(self, result: dict):
        """Add execution result to the packet."""
        self.execution_result = result
        self._add_event(
            "executed",
            f"Execution: {result.get('status', 'unknown')}",
            {"action": result.get("action_taken")},
        )

    def add_verification(self, verification: dict):
        """Add verification result to the packet."""
        self.verification = verification
        self._add_event(
            "verified",
            f"Verification: {'passed' if verification.get('remediation_successful') else 'failed'}",
        )

    def to_dict(self) -> dict:
        """Serialize the full replay packet."""
        return {
            "packet_id": self.packet_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "incident": self.incident,
            "classification": self.classification,
            "risk_score": self.risk_score,
            "recommendation": self.recommendation,
            "policy_decision": self.policy_decision,
            "approval": self.approval,
            "execution_result": self.execution_result,
            "verification": self.verification,
            "timeline": self.timeline,
            "event_count": len(self.timeline),
        }

    def to_storage_dict(self) -> dict:
        """
        Serialize for memory store storage.
        Flattens the packet into a single-level dict compatible with MemoryStore.
        """
        return {
            "source_type": "replay_packet",
            "source_id": self.packet_id,
            "incident_type": (self.classification or self.incident).get("incident_type", "unknown"),
            "title": self.incident.get("error_message", "")[:200] if self.incident.get("error_message") else f"Replay packet {self.packet_id}",
            "summary": self.recommendation.get("summary", "") if self.recommendation else "",
            "root_cause": self.recommendation.get("root_cause", "") if self.recommendation else "",
            "recommended_action": self.recommendation.get("recommended_action", "") if self.recommendation else "",
            "runbook_key": self.recommendation.get("runbook_key", "") if self.recommendation else "",
            "risk_level": self.risk_score.get("risk_level", "") if self.risk_score else "",
            "policy_decision": self.policy_decision.get("decision", "") if self.policy_decision else "",
            "execution_status": self.execution_result.get("status", "") if self.execution_result else "",
            "outcome_status": "success" if self.verification and self.verification.get("remediation_successful") else "failure" if self.verification else "",
            "confidence_score": self.recommendation.get("confidence_score") if self.recommendation else None,
            "embedding_text": self.recommendation.get("summary", "") if self.recommendation else "",
            "metadata_json": {
                "packet_id": self.packet_id,
                "timeline_events": len(self.timeline),
                "incident_severity": self.incident.get("severity", ""),
                "environment": self.incident.get("environment", ""),
            },
        }


def build_replay_packet(
    incident: dict,
    model_output: dict | None = None,
    policy_output: dict | None = None,
    classification: dict | None = None,
    risk_score: dict | None = None,
    recommendation: dict | None = None,
    approval: dict | None = None,
) -> dict:
    """
    Build a complete replay packet from incident processing outputs.

    Backward-compatible: accepts old (model_output, policy_output) and new parameters.
    """
    packet = ReplayPacket(
        incident=incident,
        classification=classification,
        risk_score=risk_score,
        recommendation=recommendation or model_output,
        policy_decision=policy_output,
        approval=approval,
    )
    return packet.to_dict()


def build_replay_packet_object(
    incident: dict,
    classification: dict | None = None,
    risk_score: dict | None = None,
    recommendation: dict | None = None,
    policy_decision: dict | None = None,
) -> ReplayPacket:
    """Build a ReplayPacket object (mutable, can be updated later)."""
    return ReplayPacket(
        incident=incident,
        classification=classification,
        risk_score=risk_score,
        recommendation=recommendation,
        policy_decision=policy_decision,
    )

