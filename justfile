# Justfile
default:
	@just --summary

setup:
	uv venv
	uv sync

run:
	uv run promptdiff --help

test:
	uv run pytest

lint:
	uv run ruff src/ tests/

format:
	uv run ruff format src/ tests/

clean:
	rm -rf .venv .promptdiff __pycache__ .pytest_cache

repl:
	uv run python
