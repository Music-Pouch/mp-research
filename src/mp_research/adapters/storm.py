from __future__ import annotations

from mp_research.adapters.base import ResearchAdapter
from mp_research.models import EvidenceBundle, ResearchBrief, RunMetadata


class StormAdapter(ResearchAdapter):
    name = "storm"

    async def run(self, brief: ResearchBrief, metadata: RunMetadata) -> EvidenceBundle:
        raise NotImplementedError(
            "RS-002 adapter pending: normalize STORM/Co-STORM artifacts into the Music Pouch evidence contract."
        )
