from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console

from mp_research.io import load_brief, persist_bundle
from mp_research.models import EngineName, RunMetadata
from mp_research.registry import get_adapter

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def run(
    engine: EngineName = typer.Option(..., help="Research engine to execute."),
    brief: Path = typer.Option(..., exists=True, dir_okay=False, readable=True),
    out: Path = typer.Option(Path("runs"), help="Run artifact directory."),
):
    """Execute one research brief with an explicit engine."""
    load_dotenv()
    research_brief = load_brief(brief)
    metadata = RunMetadata(engine=engine)
    adapter = get_adapter(engine)

    console.print(f"[bold]Running[/bold] {engine.value}: {research_brief.title}")
    bundle = asyncio.run(adapter.run(research_brief, metadata))
    run_dir = persist_bundle(bundle, out)
    console.print(f"[green]Artifacts written:[/green] {run_dir}")


if __name__ == "__main__":
    app()
