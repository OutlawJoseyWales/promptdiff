from promptdiff.commands.init import init_testset


def test_init_testset(tmp_path, capsys):
    init_testset(tmp_path)
    assert (tmp_path / "expected.json").exists()
    assert (tmp_path / "meta.yaml").exists()
    captured = capsys.readouterr()
    assert f"Initialized testset at {tmp_path}" in captured.out
