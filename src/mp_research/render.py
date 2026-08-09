from __future__ import annotations

from mp_research.models import EvidenceBundle


def render_markdown(bundle: EvidenceBundle) -> str:
    lines = [
        f"# {bundle.brief.title}",
        "",
        f"- **Engine:** {bundle.run.engine.value}",
        f"- **Engine version:** {bundle.run.engine_version or 'unknown'}",
        f"- **Job ID:** `{bundle.run.job_id}`",
        f"- **Started:** {bundle.run.started_at.isoformat()}",
        f"- **Completed:** {bundle.run.completed_at.isoformat() if bundle.run.completed_at else 'incomplete'}",
        "",
    ]

    if bundle.narrative_report:
        lines += ["## Engine report", "", bundle.narrative_report, ""]

    sections = [
        ("Claims", [claim.text for claim in bundle.claims]),
        ("Assumptions", bundle.assumptions),
        ("Contradictions", bundle.contradictions),
        ("Unresolved questions", bundle.unresolved_questions),
        ("Recommendations", bundle.recommendations),
        ("Alternatives", bundle.alternatives),
        ("Implementation implications", bundle.implementation_implications),
    ]

    for heading, items in sections:
        if items:
            lines += [f"## {heading}", ""]
            lines += [f"- {item}" for item in items]
            lines += [""]

    if bundle.sources:
        lines += ["## Sources", ""]
        for source in bundle.sources:
            label = source.title or source.id
            suffix = f" — {source.url}" if source.url else ""
            lines.append(f"- {label}{suffix}")
        lines.append("")

    return "\n".join(lines)
