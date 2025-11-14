rewrite — minimal Python package scaffold

This is a minimal Python package scaffold using the "src/" layout and modern packaging (pyproject.toml + setuptools). It includes pytest for testing, mypy for type checking, and ruff for linting. It's also configured for `uv` for fast dependency management.

## Installation

### With pip

Install the package in editable mode with dev dependencies:

    pip install -e ".[dev]"

### With uv (recommended)

Install with uv for fast, reproducible builds:

    uv sync
    uv run rewrite

## Running the CLI

With pip (after installation):

    rewrite

With uv:

    uv run rewrite

This calls the `main()` entry point defined in `src/rewrite/__main__.py`.

## Development

### With pip

Run tests:

    pytest -q

Run type checker:

    mypy src tests

Run linter:

    ruff check src tests

### With uv

Run tests:

    uv run pytest -q

Run type checker:

    uv run mypy src tests

Run linter:

    uv run ruff check src tests

## Requirements

- Python 3.14+
- setuptools, wheel (for building)
- pytest, mypy, ruff (for development)
- Optional: uv for faster dependency management


