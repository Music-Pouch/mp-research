# Music Pouch Research Runner

`mp-research` is the execution layer for Music Pouch research spikes.

It converts a research brief, or a GitHub research-spike issue routed through the GitHub Actions workflow, into a normalized evidence bundle that can be reviewed, compared, promoted into durable research, and used to propose an ADR.

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

## FREE GAME

Music Pouch ships an open baseline first.

That means the default path should stay useful without paid API credits wherever practical:

- local or self-hosted LLMs before paid-only lock-in;
- DuckDuckGo or other open retrievers before hard-wiring a proprietary search bill;
- the same evidence bundle contract no matter which provider runs the research;
- paid providers supported as upgrades, not requirements.

Today that baseline is GPT Researcher + Ollama + Qwen + DuckDuckGo.

## Quick start

### Free local baseline

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[gpt-researcher]"
cp .env.example .env

mp-research \
  --engine gpt-researcher \
  --brief examples/briefs/technical-archaeology.md \
  --out runs
```

The checked-in `.env.example` defaults to the FREE GAME path:

```dotenv
RETRIEVER=duckduckgo
OPENAI_API_KEY=ollama
OPENAI_API_BASE=http://127.0.0.1:11434/v1
OPENAI_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_BASE_URL=http://127.0.0.1:11434
FAST_LLM=ollama:qwen3:4b
SMART_LLM=ollama:qwen3:4b
STRATEGIC_LLM=ollama:qwen3:4b
EMBEDDING=ollama:nomic-embed-text
```

Before running, start Ollama and pull the local models you want to use:

```bash
ollama pull qwen3:4b
ollama pull nomic-embed-text
```

### Optional paid providers

Paid providers remain supported. Override the free defaults in `.env` with your preferred model and retriever settings, for example OpenAI plus Tavily:

```dotenv
OPENAI_API_KEY=your-key
TAVILY_API_KEY=your-key
RETRIEVER=tavily
FAST_LLM=openai:gpt-5-mini
SMART_LLM=openai:gpt-5
STRATEGIC_LLM=openai:o4-mini
EMBEDDING=openai:text-embedding-3-small
```

## GitHub Actions flow

The hosted workflow preserves the existing issue -> brief -> evidence bundle path:

```text
Music Pouch issue
      -> workflow_dispatch
      -> brief markdown
      -> GPT Researcher
      -> runs/<job-id>/
```

Workflow behavior:

- If `OPENAI_API_KEY` is set, the workflow uses your configured paid or compatible provider settings.
- If `OPENAI_API_KEY` is not set, the workflow starts Ollama on the runner, pulls `qwen3:4b` plus `nomic-embed-text`, and uses `duckduckgo`.
- `TAVILY_API_KEY` is optional. `duckduckgo` is the default retriever unless you override it.

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
