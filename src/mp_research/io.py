from __future__ import annotations

import json
from pathlib import Path

from mp_research.models import EvidenceBundle, ResearchBrief
from mp_research.render import render_markdown


def load_brief(path: Path) -> ResearchBrief:
    text = path.read_text()
    title = path.stem.replace("-", " ").title()

    if text.startswith("# "):
        first, *rest = text.splitlines()
        title = first.removeprefix("# ").strip()
        text = "\n".join(rest).strip()

    return ResearchBrief(title=title, prompt=text)


def persist_bundle(bundle: EvidenceBundle, out_root: Path) -> Path:
    run_dir = out_root / bundle.run.job_id
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "evidence.json").write_text(bundle.model_dump_json(indent=2))
    (run_dir / "report.md").write_text(render_markdown(bundle))

    if bundle.raw_output is not None:
        raw_dir = run_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "engine-output.json").write_text(
            json.dumps(bundle.raw_output, indent=2, default=str)
        )

    return run_dir
