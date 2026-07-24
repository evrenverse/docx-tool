.PHONY: audit build check eval format install release-check test typecheck

install:
	uv sync --all-groups --locked

format:
	uv run ruff format .

typecheck:
	uv run mypy src

test:
	uv run pytest --cov=docx_tool --cov-branch --cov-report=term-missing

eval:
	uv run python evals/run_evals.py

build:
	uv build
	uv run twine check dist/*

audit:
	uv export --no-dev --locked --no-emit-project -o requirements-audit.txt
	uv run pip-audit -r requirements-audit.txt

check:
	uv run ruff format --check .
	uv run ruff check .
	$(MAKE) typecheck
	$(MAKE) test
	$(MAKE) eval

release-check: check build
