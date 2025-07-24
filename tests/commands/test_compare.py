from promptdiff.commands.compare import compare_runs


def test_compare_runs(capsys):
    compare_runs("run_a", "run_b")
    captured = capsys.readouterr()
    assert "Comparing run_a to run_b" in captured.out
