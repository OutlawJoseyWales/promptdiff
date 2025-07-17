
# 📦 `promptdiff` v1 – Build Plan & Work Packet

**Goal**: Build a local-first CLI + dashboard tool to track and compare LLM output quality over time on gold-standard test files. Focus is on **file-level regression tracking**, **semantic diffing**, and **local, audit-friendly visualizations**.

---

## 🧠 Product Summary

`promptdiff` is a developer tool that helps teams:
- Track **per-file performance** of LLM pipelines
- Compare **outputs across prompt/flow versions**
- Visualize **semantic changes and regressions**
- Store and **view historical eval results** locally

No hosting. No API keys. No tracking.

---

## 🧩 Core Features (v1 Scope)

### ✅ 1. CLI Commands

```
promptdiff init
promptdiff record --flow flow_v1.py --testset tests/invoices/
promptdiff compare run_001 run_002
promptdiff dashboard
```

| Command | Description |
|--------|-------------|
| `init` | Scaffold a new testset directory with sample input/expected files |
| `record` | Run flow on a test set, evaluate output vs expected, save to `.promptdiff/runs/<run_id>/...` |
| `compare` | Compare two past runs: show differences in accuracy and output content |
| `dashboard` | Launch local web viewer to explore file history and diffs |

---

### ✅ 2. Testset Structure

```
/tests/invoices/
  invoice_001.pdf
  expected.json
  meta.yaml       # optional: task description, tags
```

- `expected.json`: ground-truth output (can be flat JSON or nested)
- `meta.yaml`: optional test metadata (category, tags, weights, etc.)

---

### ✅ 3. Result Storage

All run data saved locally in:
```
.promptdiff/
  runs/
    run_001/
      config.json          # run metadata (flow name, model, timestamp, prompt hash)
      invoice_001.json     # actual vs expected + score + diff
      invoice_002.json
```

Each file contains:
```json
{
  "input_file": "invoice_001.pdf",
  "expected": { ... },
  "actual": { ... },
  "score": 0.82,
  "diff": { ... },
  "timestamp": "2025-07-16T20:00:00Z"
}
```

---

### ✅ 4. Evaluation Logic

| Type | Details |
|------|---------|
| String/Text | Levenshtein distance or cosine similarity (optionally LLM-based scoring later) |
| JSON Objects | Field-by-field comparison; ignore ordering |
| Lists | Compare length + overlap (Jaccard) |
| Custom | Support custom comparator Python function (future) |

---

### ✅ 5. Diff Format

Store a diff object with:
```json
{
  "added_fields": ["invoice_date"],
  "removed_fields": ["total_due"],
  "changed_fields": {
    "vendor_name": {
      "old": "Tesla Motors",
      "new": "Tesla, Inc."
    }
  }
}
```

---

## 🖥️ Local Dashboard

Launch with:
```
promptdiff dashboard
```

| Page | Features |
|------|----------|
| Home | Select test set and flow version |
| File view | Shows all past runs on that file with scores |
| Diff view | Compare actual vs expected (side-by-side + highlights) |
| Timeline | Line chart of accuracy per file across runs |

Tech:
- Vite + React or Svelte
- Read-only UI that loads from `.promptdiff/runs/`
- No server or DB — reads from local filesystem

---

## 🛠️ Tech Stack (Recommended)

| Component | Stack |
|----------|-------|
| CLI | Python 3.10+, Typer |
| Data storage | JSON or Parquet in `.promptdiff/` |
| Dashboard | React + Tailwind + Vite (can bundle to static app) |
| Diff logic | `deepdiff`, `difflib`, `scikit-learn`, or custom |
| Optional | Pandas for summary metrics |

---

## 🗓️ Build Plan (10–15 hrs total)

| Phase | Deliverable |
|-------|-------------|
| ✅ Setup | Git repo, CLI scaffold, `.promptdiff/` folder structure |
| 1. CLI – init | `promptdiff init` to scaffold testset directory |
| 2. CLI – record | `promptdiff record` runs flow, evaluates outputs, saves results |
| 3. CLI – compare | `promptdiff compare` shows diffs and summary table |
| 4. CLI – report | Optional: markdown/HTML report for PR use |
| 5. Dashboard | File selector → timeline + diff view |
| 6. Internal use | Run on 1–2 testsets from real project |
| 7. Share | OSS license, internal demo, ReadMe polish |

---

## 🔐 Constraints

- **No hosted data** — must be installable and local-only
- **Enterprise-friendly** — zero vendor dependencies, clean MIT license
- **Easy to try** — one-liner install or `git clone && pip install .`

---

## 💡 Future Features (Not v1)

- Slack/GitHub PR output
- LLM-based output evaluators (`OpenAI`, `Claude`, etc.)
- CI integration (`promptdiff check`)
- Hosted dashboard w/ team accounts and eval feedback
- Test result scoring via heuristics or judgment prompts

---

## 📣 Internal Pitch (TL;DR)

> Promptdiff helps us track LLM output quality *per test file*, across prompt and flow versions, with clear diff views and local-first storage. It replaces ephemeral PR comments with a system of record for regression visibility — without changing your stack or leaking any data.
