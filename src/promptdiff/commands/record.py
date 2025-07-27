from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Tuple

import typer


def _parse_possible_json(text: str) -> Any:
    """Return JSON object if ``text`` is valid JSON else stripped string."""
    try:
        return json.loads(text)
    except Exception:
        return text.strip()


def _diff_json(expected: Dict[str, Any], actual: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
    """Compute diff and score for two JSON objects."""
    added = [k for k in actual.keys() if k not in expected]
    removed = [k for k in expected.keys() if k not in actual]
    changed: Dict[str, Dict[str, Any]] = {}
    match_count = 0
    for key in expected.keys() & actual.keys():
        if expected[key] != actual[key]:
            changed[key] = {"old": expected[key], "new": actual[key]}
        else:
            match_count += 1
    total = len(expected.keys())
    score = match_count / total if total else 1.0
    diff: Dict[str, Any] = {}
    if added:
        diff["added_fields"] = sorted(added)
    if removed:
        diff["removed_fields"] = sorted(removed)
    if changed:
        diff["changed_fields"] = changed
    return diff, score


def _diff_text(expected: str, actual: str) -> Tuple[Dict[str, Any], float]:
    """Diff two strings using difflib ratio."""
    import difflib

    score = difflib.SequenceMatcher(None, expected, actual).ratio()
    if expected == actual:
        return {}, score
    diff_lines = list(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            lineterm="",
        )
    )
    return {"text_diff": diff_lines}, score


def _compute_diff(expected: Any, actual: Any) -> Tuple[Dict[str, Any], float]:
    if isinstance(expected, dict) and isinstance(actual, dict):
        return _diff_json(expected, actual)
    if isinstance(expected, str) and isinstance(actual, str):
        return _diff_text(expected, actual)
    # Fallback to string comparison
    return _diff_text(str(expected), str(actual))


def record_results(
    flow: str,
    testset: str,
    prompt_template: str | None = None,
    prompt_file: str | None = None,
    prompt_vars: str | None = None,
) -> None:
    """Run ``flow`` on ``testset`` and save structured results."""

    flow_path = Path(flow)
    testset_path = Path(testset)

    run_id = datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    run_dir = Path(".promptdiff") / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    expected_path = testset_path / "expected.json"
    expected_data: Dict[str, Any] = {}
    if expected_path.exists():
        expected_data = json.loads(expected_path.read_text())

    timestamp = datetime.utcnow().isoformat()

    config: Dict[str, Any] = {
        "flow": str(flow_path),
        "testset": str(testset_path),
        "timestamp": timestamp,
        "args": {
            "flow": flow,
            "testset": testset,
        },
    }

    if prompt_template or prompt_file:
        prompt_info: Dict[str, Any] = {}
        content = ""
        if prompt_template:
            content = prompt_template
            prompt_info["template"] = prompt_template
        if prompt_file:
            prompt_path = Path(prompt_file)
            content = prompt_path.read_text()
            prompt_info["prompt_file"] = str(prompt_path)
            prompt_info["prompt_text"] = content
        if prompt_vars:
            vars_path = Path(prompt_vars)
            if vars_path.exists():
                try:
                    prompt_info["prompt_variables"] = json.loads(vars_path.read_text())
                except Exception:
                    prompt_info["prompt_variables"] = vars_path.read_text()
            else:
                try:
                    prompt_info["prompt_variables"] = json.loads(prompt_vars)
                except Exception:
                    prompt_info["prompt_variables"] = prompt_vars
        prompt_info["prompt_hash"] = sha256(content.encode()).hexdigest()
        config.update(prompt_info)

    (run_dir / "config.json").write_text(json.dumps(config, indent=2))

    input_files = [
        p
        for p in testset_path.iterdir()
        if p.is_file() and p.name not in {"expected.json", "meta.yaml"}
    ]

    for input_file in sorted(input_files):
        result: Dict[str, Any] = {
            "input_file": input_file.name,
            "expected": expected_data.get(input_file.name),
            "actual": None,
            "score": None,
            "diff": None,
            "timestamp": datetime.utcnow().isoformat(),
            "error": None,
        }

        proc = subprocess.run(
            [sys.executable, str(flow_path), str(input_file)],
            capture_output=True,
            text=True,
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        if proc.returncode != 0:
            result["actual"] = _parse_possible_json(stdout)
            result["error"] = stderr or f"Process exited with {proc.returncode}"
        else:
            actual = _parse_possible_json(stdout)
            result["actual"] = actual
            expected = result["expected"]
            if expected is not None:
                diff, score = _compute_diff(expected, actual)
                result["diff"] = diff
                result["score"] = score

        result_path = run_dir / f"{input_file.stem}.json"
        result_path.write_text(json.dumps(result, indent=2))

    typer.echo(f"Saved results to {run_dir}")
