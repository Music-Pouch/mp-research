from __future__ import annotations

from abc import ABC, abstractmethod

from mp_research.models import EvidenceBundle, ResearchBrief, RunMetadata


class ResearchAdapter(ABC):
    name: str

    @abstractmethod
    async def run(self, brief: ResearchBrief, metadata: RunMetadata) -> EvidenceBundle:
        """Execute research and normalize it into the Music Pouch evidence contract."""
        raise NotImplementedError
