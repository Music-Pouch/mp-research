# Music Pouch Research Runner

`mp-research` is the execution layer for Music Pouch research spikes.

It converts a research brief (or eventually a GitHub research-spike issue) into a normalized evidence bundle that can be reviewed, compared, promoted into durable research, and used to propose an ADR.

The runner deliberately separates research execution from architecture approval, engine-native output from Music Pouch's evidence contract, and deterministic evaluation from engine routing.

## Status

RS-002 bootstrap.

The initial implementation provides:

- an engine adapter protocol;
- a Music Pouch evidence schema;
- a CLI;
- Markdown + JSON output;
- a GPT Researcher adapter;
- explicit adapter slots for Open Deep Research and STORM/Co-STORM;
- a deterministic evaluation rubric.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[gpt-researcher]"
cp .env.example .env
```

Set the provider/search keys required by your chosen engine, then:

```bash
mp-research run \
  --engine gpt-researcher \
  --brief examples/briefs/technical-archaeology.md \
  --out runs
```

A run emits:

```text
runs/<job-id>/
├── evidence.json
├── report.md
└── raw/
    └── engine-output.json
```

## Evidence contract

The contract is intentionally owned by Music Pouch rather than by any research framework. See `src/mp_research/models.py`.

## Engine policy

No engine is the default winner yet. RS-002 benchmarks GPT Researcher, LangChain Open Deep Research, and Stanford STORM / Co-STORM against technical archaeology, market/product research, and exploratory unknown-unknown research.

## Architecture boundary

Research engines may recommend decisions. They may not accept ADRs.

ADR acceptance remains a human/DACI decision expressed by merging the ADR PR.
