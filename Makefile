SHELL := $(shell which bash) # set default shell

.SHELLFLAGS = -c # Run commands in a -c flag
.SILENT: ; # no need for @
.ONESHELL: ; # recipes execute in same shell
.NOTPARALLEL: ; # wait for this target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell
.PHONY: all # All targets are accessible for user
.DEFAULT: help # Running Make will run the help target

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dev:  ## Install dev dependencies & this library as editable for local development
	pip install flit && flit install --deps develop --symlink --extras all

build-docs:  ## Generate documentation
	mkdocs build

serve-docs:  ## Preview documentation with local development server
	mkdocs serve

black:  ## Run black formatter on all python source code
	black pubsub scripts tests

lint:  ## Run black formatter on all python source code
	flake8 pubsub scripts tests

test:  ## Run unit tests & report on coverage
	pytest tests/unit/ && coverage-badge -f -o coverage.svg

integration:  ## Run integration tests
	pytest tests/integration/ --no-cov

test-watch:  ## Run tests & report on coverage
	scripts/test_watch.py

shell:  ## Start a ptpython shell
	ptpython --history-file .shell_history

publish:  ## Publish package to PyPi
	flit publish

install:  ## Install package
	flit install

benchmark-message:  ## Run test & report on coverage
	scripts/benchmark_message.py