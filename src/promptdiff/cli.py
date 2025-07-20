from __future__ import annotations

import json
import os
from pathlib import Path

import typer

app = typer.Typer(help="Promptdiff CLI")


@app.command()
def init(testset: Path = typer.Argument(Path("tests/sample"), help="Test set directory")) -> None:
    """Scaffold a new testset directory with sample files."""
    testset_path = Path(testset)
    testset_path.mkdir(parents=True, exist_ok=True)

    (testset_path / "expected.json").write_text(json.dumps({}, indent=2))
    (testset_path / "meta.yaml").write_text("# optional metadata\n")
    typer.echo(f"Initialized testset at {testset_path}")


@app.command()
def record(flow: str, testset: str) -> None:
    """Run flow on a test set and save results (placeholder)."""
    typer.echo(f"Recording results for flow {flow} on {testset}")


@app.command()
def compare(run_a: str, run_b: str) -> None:
    """Compare two past runs (placeholder)."""
    typer.echo(f"Comparing {run_a} to {run_b}")


@app.command()
def dashboard() -> None:
    """Launch local dashboard (placeholder)."""
    typer.echo("Launching dashboard...")


if __name__ == "__main__":
    app()

