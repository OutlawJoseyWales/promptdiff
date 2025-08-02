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
def record(
    flow: Path = typer.Argument(..., help="Flow script to run"),
    testset: Path = typer.Argument(..., help="Test set directory"),
    prompt_template: str | None = typer.Option(
        None, help="Prompt template string", show_default=False
    ),
    prompt_file: Path | None = typer.Option(
        None, help="Path to a file containing the prompt", show_default=False
    ),
    prompt_vars: str | None = typer.Option(
        None, help="Prompt variables as JSON or path", show_default=False
    ),
) -> None:
    """Run flow on a test set and save results."""
    record_results(
        str(flow),
        str(testset),
        prompt_template=prompt_template,
        prompt_file=str(prompt_file) if prompt_file else None,
        prompt_vars=prompt_vars,
    )


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

