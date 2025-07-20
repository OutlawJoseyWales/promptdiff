from pathlib import Path

from typer.testing import CliRunner

from promptdiff.cli import app


runner = CliRunner()


def test_init(tmp_path: Path) -> None:
    testdir = tmp_path / "myset"
    result = runner.invoke(app, ["init", str(testdir)])
    assert result.exit_code == 0
    assert (testdir / "expected.json").exists()
    assert (testdir / "meta.yaml").exists()

