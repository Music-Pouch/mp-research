from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl


class EngineName(StrEnum):
    GPT_RESEARCHER = "gpt-researcher"
    OPEN_DEEP_RESEARCH = "open-deep-research"
    STORM = "storm"
    COSTORM = "costorm"


class SourceReference(BaseModel):
    id: str
    url: HttpUrl | None = None
    title: str | None = None
    source_type: str | None = None
    retrieved_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Claim(BaseModel):
    id: str
    text: str
    source_ids: list[str] = Field(default_factory=list)
    support_level: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    notes: str | None = None


class ResearchBrief(BaseModel):
    title: str
    prompt: str
    source_issue: str | None = None
    archetype: str | None = None
    constraints: list[str] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)


class RunMetadata(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid4()))
    engine: EngineName
    engine_version: str | None = None
    model_configuration: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    cost: dict[str, Any] = Field(default_factory=dict)


class EvidenceBundle(BaseModel):
    schema_version: str = "0.1.0"
    brief: ResearchBrief
    run: RunMetadata
    claims: list[Claim] = Field(default_factory=list)
    sources: list[SourceReference] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    implementation_implications: list[str] = Field(default_factory=list)
    raw_artifacts: list[str] = Field(default_factory=list)
    raw_output: Any | None = Field(default=None, exclude=True)
    narrative_report: str | None = None
