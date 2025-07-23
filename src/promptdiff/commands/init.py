from __future__ import annotations

import json
from pathlib import Path

import typer


def init_testset(testset: Path) -> None:
    """Scaffold a new testset directory with sample files."""
    testset_path = Path(testset)
    testset_path.mkdir(parents=True, exist_ok=True)

    (testset_path / "expected.json").write_text(json.dumps({}, indent=2))
    (testset_path / "meta.yaml").write_text("# optional metadata\n")
    typer.echo(f"Initialized testset at {testset_path}")
