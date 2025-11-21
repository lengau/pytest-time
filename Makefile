ifdef $(CI)
apt = apt-get --yes
else
apt = apt-get
endif

.PHONY: help
help: ## Show this help.
	@printf "%-30s %s\n" "Target" "Description"
	@printf "%-30s %s\n" "------" "-----------"
	@fgrep " ## " $(MAKEFILE_LIST) | fgrep -v grep | awk -F ': .*## ' '{$$1 = sprintf("%-30s", $$1)} 1'

.PHONY: format
format: install-yamlfmt
	ruff format .
	ruff check --fix .
	uv run --group lint docstrfmt .
	uv run --group lint codespell --toml pyproject.toml --write-changes .
	yamlfmt .

.PHONY: lint-ruff
lint-ruff:
	ruff format --check --diff .
	ruff check .

.PHONY: lint-docs
lint-docs:
	uv run --group lint docstrfmt --check .

.PHONY: lint
lint: lint-ruff lint-types lint-docs
	uv run --group lint codespell --toml pyproject.toml
	uv run --group lint yamllint .
	uv run --group lint rstcheck -r .

.PHONY: lint-types
lint-types:
	uv run --group lint pyright
	uv run --group lint mypy
	# Check type compatibility with pre-3.10 python
	VIRTUAL_ENV=.venv-3.9 uv run --group=lint --python=3.9 mypy

.PHONY: lint-actions
lint-actions: install-actionlint
	actionlint

.PHONY: test
test:
	uv run pytest

.PHONY: test-oldest
test-oldest:
	uv run --isolated --frozen --resolution=lowest --python-preference=only-system pytest

.PHONY: docs
docs:
	make -C docs html

.PHONY: docs-auto
docs-auto: ## Auto-build docs
	make -C docs auto

.PHONY: install-test-deps
install-test-deps:
ifneq ($(shell which apt-get),)
	sudo $(apt) install libxml2-dev libxslt1-dev clang
else
	$(warning Unknown how to install dependencies on this system. Please install the equivalents of the following debian packages:)
	$(info libxml2-dev libxslt1-dev clang)
endif

.PHONY: install-actionlint
install-actionlint:
ifneq ($(shell which actionlint),)
	@# Actionlint already installed
else ifneq ($(shell which go),)
	go install github.com/rhysd/actionlint/cmd/actionlint@latest
else
	$(error Please install go to use actionlint)
endif

.PHONY: install-yamlfmt
install-yamlfmt:
ifneq ($(shell which yamlfmt),)
else ifneq ($(shell which go),)
	go install github.com/google/yamlfmt/cmd/yamlfmt@latest
else
	$(error Please install go to use yamlfmt)
endif
