from __future__ import annotations

from mp_research.adapters.base import ResearchAdapter
from mp_research.models import EvidenceBundle, ResearchBrief, RunMetadata


class OpenDeepResearchAdapter(ResearchAdapter):
    name = "open-deep-research"

    async def run(self, brief: ResearchBrief, metadata: RunMetadata) -> EvidenceBundle:
        raise NotImplementedError(
            "RS-002 adapter pending: normalize Open Deep Research run state into the Music Pouch evidence contract."
        )
