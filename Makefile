.PHONY: help
help: ## Show this help.
	@printf "%-30s %s\n" "Target" "Description"
	@printf "%-30s %s\n" "------" "-----------"
	@fgrep " ## " $(MAKEFILE_LIST) | fgrep -v grep | awk -F ': .*## ' '{$$1 = sprintf("%-30s", $$1)} 1'

.PHONY: autoformat
autoformat:
	uv run black .
	ruff check --fix --respect-gitignore .
	uv run codespell --toml pyproject.toml --write-changes .

.PHONY: lint
lint: lint-types
	uv run black --check --diff .
	ruff check --respect-gitignore .
	uv run codespell --toml pyproject.toml
	uv run yamllint .
	uv run rstcheck -r .

.PHONY: lint-types
lint-types:
	uv run pyright
	uv run mypy


.PHONY: test
test:
	uv run pytest

.PHONY: test-oldest
test-oldest:
	uv run --isolated --frozen --resolution=lowest --python-preference=only-system pytest