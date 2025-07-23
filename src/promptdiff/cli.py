from __future__ import annotations

from pathlib import Path

import typer

from .commands import (
    compare_runs,
    init_testset,
    launch_dashboard,
    record_results,
)

app = typer.Typer(help="Promptdiff CLI")


@app.command()
def init(
    testset: Path = typer.Argument(Path("tests/sample"), help="Test set directory"),
) -> None:
    """Scaffold a new testset directory with sample files."""
    init_testset(testset)


@app.command()
def record(flow: str, testset: str) -> None:
    """Run flow on a test set and save results (placeholder)."""
    record_results(flow, testset)


@app.command()
def compare(run_a: str, run_b: str) -> None:
    """Compare two past runs (placeholder)."""
    compare_runs(run_a, run_b)


@app.command()
def dashboard() -> None:
    """Launch local dashboard (placeholder)."""
    launch_dashboard()


if __name__ == "__main__":
    app()

