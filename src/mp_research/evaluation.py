from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluationScore(BaseModel):
    factual_correctness: float | None = Field(default=None, ge=0, le=5)
    source_quality: float | None = Field(default=None, ge=0, le=5)
    citation_traceability: float | None = Field(default=None, ge=0, le=5)
    completeness: float | None = Field(default=None, ge=0, le=5)
    useful_unknowns: float | None = Field(default=None, ge=0, le=5)
    decision_usefulness: float | None = Field(default=None, ge=0, le=5)
    reproducibility: float | None = Field(default=None, ge=0, le=5)
    latency: float | None = Field(default=None, ge=0, le=5)
    cost: float | None = Field(default=None, ge=0, le=5)
    integration_complexity: float | None = Field(default=None, ge=0, le=5)
    controllability: float | None = Field(default=None, ge=0, le=5)
    github_code_research: float | None = Field(default=None, ge=0, le=5)
    notes: list[str] = Field(default_factory=list)

    def mean(self) -> float | None:
        values = [
            value
            for key, value in self.model_dump().items()
            if key != "notes" and isinstance(value, (int, float))
        ]
        return sum(values) / len(values) if values else None
