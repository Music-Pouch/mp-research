import json

from mp_research.io import persist_bundle
from mp_research.models import EngineName, EvidenceBundle, ResearchBrief, RunMetadata


def test_persist_bundle_writes_raw_engine_output(tmp_path):
    bundle = EvidenceBundle(
        brief=ResearchBrief(title="test", prompt="research this"),
        run=RunMetadata(engine=EngineName.GPT_RESEARCHER),
        raw_artifacts=["raw/engine-output.json"],
        raw_output={"context": [{"url": "https://example.com", "content": "evidence"}]},
    )

    run_dir = persist_bundle(bundle, tmp_path)

    assert (run_dir / "evidence.json").exists()
    assert (run_dir / "report.md").exists()
    raw_path = run_dir / "raw" / "engine-output.json"
    assert raw_path.exists()
    assert json.loads(raw_path.read_text())["context"][0]["content"] == "evidence"

    evidence = json.loads((run_dir / "evidence.json").read_text())
    assert "raw_output" not in evidence
    assert evidence["raw_artifacts"] == ["raw/engine-output.json"]
