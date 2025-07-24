from promptdiff.commands.dashboard import launch_dashboard


def test_launch_dashboard(capsys):
    launch_dashboard()
    captured = capsys.readouterr()
    assert "Launching dashboard..." in captured.out
