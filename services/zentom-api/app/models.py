from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import UserDefinedType


class Base(DeclarativeBase):
    pass


class Vector(UserDefinedType):
    cache_ok = True

    def __init__(self, dimensions: int):
        self.dimensions = dimensions

    def get_col_spec(self, **kw):
        return f"vector({self.dimensions})"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            if isinstance(value, str):
                return value
            return "[" + ",".join(str(v) for v in value) + "]"

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None or isinstance(value, list):
                return value
            if isinstance(value, str):
                text_value = value.strip()
                if text_value.startswith("[") and text_value.endswith("]"):
                    return [
                        float(part)
                        for part in text_value[1:-1].split(",")
                        if part.strip()
                    ]
            return value

        return process


@compiles(Vector, "sqlite")
def compile_vector_sqlite(type_, compiler, **kw):
    return "TEXT"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_id: Mapped[str | None] = mapped_column(String(100), index=True)
    incident_type: Mapped[str | None] = mapped_column(String(100), index=True)
    source: Mapped[str | None] = mapped_column(String(100))
    environment: Mapped[str | None] = mapped_column(String(50), index=True)
    error_message: Mapped[str | None] = mapped_column(Text)
    action_type: Mapped[str | None] = mapped_column(String(100))
    confidence: Mapped[int | None] = mapped_column(Integer)
    raw_payload: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    risk_score: Mapped["RiskScore"] = relationship(back_populates="incident")
    policy_decision: Mapped["PolicyDecision"] = relationship(back_populates="incident")
    ai_recommendation: Mapped["AIRecommendation"] = relationship(back_populates="incident")


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    technical_severity: Mapped[int] = mapped_column(Integer)
    business_impact: Mapped[int] = mapped_column(Integer)
    blast_radius: Mapped[int] = mapped_column(Integer)
    operational_context: Mapped[int] = mapped_column(Integer)
    total_score: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    incident: Mapped[Incident] = relationship(back_populates="risk_score")


class PolicyDecision(Base):
    __tablename__ = "policy_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    decision: Mapped[str] = mapped_column(String(100))
    requires_approval: Mapped[bool] = mapped_column(Boolean)
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    incident: Mapped[Incident] = relationship(back_populates="policy_decision")


class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    summary: Mapped[str] = mapped_column(Text)
    root_cause: Mapped[str] = mapped_column(Text)
    recommended_action: Mapped[str] = mapped_column(Text)
    confidence_score: Mapped[int] = mapped_column(Integer)
    runbook_key: Mapped[str] = mapped_column(String(100))
    recommendation_status: Mapped[str] = mapped_column(String(50))
    model_name: Mapped[str] = mapped_column(String(100))
    raw_model_output: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    incident: Mapped[Incident] = relationship(back_populates="ai_recommendation")


class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_id: Mapped[str | None] = mapped_column(String(100))
    incident_type: Mapped[str | None] = mapped_column(String(100), index=True)
    title: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    root_cause: Mapped[str | None] = mapped_column(Text)
    recommended_action: Mapped[str | None] = mapped_column(Text)
    runbook_key: Mapped[str | None] = mapped_column(String(150), index=True)
    risk_level: Mapped[str | None] = mapped_column(String(50))
    policy_decision: Mapped[str | None] = mapped_column(String(100))
    execution_status: Mapped[str | None] = mapped_column(String(100))
    outcome_status: Mapped[str | None] = mapped_column(String(100))
    embedding_text: Mapped[str | None] = mapped_column(Text)
    embedding_vector: Mapped[list[float] | None] = mapped_column(Vector(384))
    metadata_json: Mapped[dict | None] = mapped_column(JSON().with_variant(JSONB, "postgresql"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )
