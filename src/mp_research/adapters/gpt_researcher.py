from __future__ import annotations

import importlib.metadata
from datetime import datetime, timezone

from mp_research.adapters.base import ResearchAdapter
from mp_research.models import EvidenceBundle, ResearchBrief, RunMetadata


class GPTResearcherAdapter(ResearchAdapter):
    name = "gpt-researcher"

    async def run(self, brief: ResearchBrief, metadata: RunMetadata) -> EvidenceBundle:
        try:
            from gpt_researcher import GPTResearcher
        except ImportError as exc:
            raise RuntimeError(
                'GPT Researcher is not installed. Run: pip install -e ".[gpt-researcher]"'
            ) from exc

        try:
            metadata.engine_version = importlib.metadata.version("gpt-researcher")
        except importlib.metadata.PackageNotFoundError:
            metadata.engine_version = None

        researcher = GPTResearcher(query=brief.prompt)
        await researcher.conduct_research()
        report: str = await researcher.write_report()
        metadata.completed_at = datetime.now(timezone.utc)

        return EvidenceBundle(
            brief=brief,
            run=metadata,
            narrative_report=report,
            unresolved_questions=[
                "Structured claim/source extraction from GPT Researcher native context is pending."
            ],
            implementation_implications=[
                "Preserve native engine context before normalization.",
                "Only promote claims when source provenance can be mapped explicitly.",
            ],
        )
