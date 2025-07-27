import json
from promptdiff.commands.record import record_results


def test_record_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    flow = tmp_path / "flow.py"
    flow.write_text(
        """
import sys, json, pathlib
path = sys.argv[1]
name = pathlib.Path(path).name
if name == "fail.txt":
    print('boom', file=sys.stderr)
    sys.exit(1)
content = open(path).read().strip()
if name == "json.txt":
    print(json.dumps({'foo': content}))
else:
    print(content)
"""
    )

    testset = tmp_path / "testset"
    testset.mkdir()
    (testset / "json.txt").write_text("bar")
    (testset / "fail.txt").write_text("ignore")
    expected = {"json.txt": {"foo": "bar"}, "fail.txt": "ignore"}
    (testset / "expected.json").write_text(json.dumps(expected))

    record_results(str(flow), str(testset))

    runs = list((tmp_path / ".promptdiff" / "runs").iterdir())
    assert len(runs) == 1
    run_dir = runs[0]
    assert (run_dir / "config.json").exists()

    success_res = json.loads((run_dir / "json.json").read_text())
    assert success_res["score"] == 1.0
    assert success_res["error"] is None

    fail_res = json.loads((run_dir / "fail.json").read_text())
    assert fail_res["error"]

