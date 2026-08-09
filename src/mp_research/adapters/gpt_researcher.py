from __future__ import annotations

import importlib.metadata
from datetime import UTC, datetime
from typing import Any

from mp_research.adapters.base import ResearchAdapter
from mp_research.models import EvidenceBundle, ResearchBrief, RunMetadata, SourceReference


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

        context = researcher.get_research_context()
        costs = researcher.get_costs()
        native_sources = researcher.get_research_sources()
        source_urls = researcher.get_source_urls()

        metadata.completed_at = datetime.now(UTC)
        if isinstance(costs, dict):
            metadata.cost = costs
        else:
            metadata.cost = {"native": costs}

        sources = self._normalize_sources(native_sources, source_urls)
        raw_output = {
            "context": context,
            "costs": costs,
            "sources": native_sources,
            "source_urls": source_urls,
        }

        return EvidenceBundle(
            brief=brief,
            run=metadata,
            sources=sources,
            narrative_report=report,
            raw_artifacts=["raw/engine-output.json"],
            raw_output=raw_output,
            unresolved_questions=[
                (
                    "Claim-level extraction is not implemented yet; no claims are promoted "
                    "until they can be mapped to explicit source provenance."
                )
            ],
            implementation_implications=[
                "Preserve GPT Researcher context, costs, and source records before normalization.",
                "Do not infer claim confidence or provenance from report prose.",
            ],
        )

    @staticmethod
    def _normalize_sources(
        native_sources: Any,
        source_urls: Any,
    ) -> list[SourceReference]:
        normalized: list[SourceReference] = []
        seen: set[str] = set()

        if isinstance(native_sources, list):
            for index, source in enumerate(native_sources):
                if not isinstance(source, dict):
                    continue
                url = source.get("url") or source.get("href")
                key = str(url or source.get("title") or index)
                if key in seen:
                    continue
                seen.add(key)
                normalized.append(
                    SourceReference(
                        id=f"gptr-source-{index + 1}",
                        url=url,
                        title=source.get("title"),
                        source_type="gpt-researcher",
                        metadata={
                            key: value
                            for key, value in source.items()
                            if key not in {"url", "href", "title", "content"}
                        },
                    )
                )

        if isinstance(source_urls, list):
            for url in source_urls:
                key = str(url)
                if key in seen:
                    continue
                seen.add(key)
                normalized.append(
                    SourceReference(
                        id=f"gptr-source-{len(normalized) + 1}",
                        url=url,
                        source_type="gpt-researcher",
                    )
                )

        return normalized
