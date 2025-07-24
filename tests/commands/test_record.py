from promptdiff.commands.record import record_results


def test_record_results(capsys):
    record_results("flow_v1.py", "tests/invoices")
    captured = capsys.readouterr()
    assert "Recording results for flow flow_v1.py on tests/invoices" in captured.out
