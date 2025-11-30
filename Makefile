# We exclude a make install command, because the cookiecutter already automatically does all that

.PHONY: style
style:
	- uv run ruff check --fix
	- uv run ruff format

.PHONY: install
install:
	- uv sync
	- uv run pre-commit install

.PHONY: check
check:
	- uv run pre-commit run --all-files

test:
	- uv run pytest tests/

coverage:
	- uv run pytest -s --cov-report html --cov=app tests/

build:
	- uv build

.PHONY: clean
clean:
	- uv run python -c "import shutil; [shutil.rmtree(f, ignore_errors=True) for f in [ 'test-output.xml', 'dist', 'build', '.pytest_cache', 'logs','.coverage','htmlcov']]"
	- uv run python -c "import os, pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
