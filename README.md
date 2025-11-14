rewrite — amend any commit in git history

`rewrite` is a git utility that lets you amend any commit in your repository by adding the currently staged changes to it, with automatic rebasing of any descendants.

It works like `git commit --amend`, but instead of only amending HEAD, you specify which commit to amend via its hash.

## How it works

1. Stage your changes with `git add`
2. Run `rewrite <commit-id>` where `<commit-id>` is the commit you want to amend
3. The changes are combined with that commit and the rest of the tree is rebased automatically
4. If there are conflicts, git will pause the rebase for you to resolve them

## Installation

### With pip

Install the package in editable mode with dev dependencies:

    pip install -e ".[dev]"

### With uv (recommended)

Install with uv for fast, reproducible builds:

    uv sync
    uv run rewrite

## Using rewrite

### Basic usage

Amend a specific commit with staged changes:

    git add <files>
    rewrite <commit-id>

### Examples

Amend the commit `abc1234` with currently staged changes:

    rewrite abc1234

Use abbreviated commit hash (first 7 characters):

    rewrite abc1234

Amend with a new commit message:

    rewrite abc1234 -m "New commit message"

### With uv

    uv run rewrite <commit-id>

## Running the CLI

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


