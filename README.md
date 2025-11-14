git-rewrite — amend any commit in git history

`git-rewrite` is a git utility that lets you amend any commit in your repository by adding the currently staged changes to it, with automatic rebasing of any descendants.

It works like `git commit --amend`, but instead of only amending HEAD, you specify which commit to amend via its hash.

## How it works

1. Stage your changes with `git add`
2. Run `git-rewrite <commit-id>` where `<commit-id>` is the commit you want to amend
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
    git-rewrite <commit-id>

### Examples

Amend the commit `abc1234` with currently staged changes:

    git-rewrite abc1234

Use abbreviated commit hash (first 7 characters):

    git-rewrite abc1234

Amend with a new commit message:

    git-rewrite abc1234 -m "New commit message"

### With uv

    uv run git-rewrite <commit-id>

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

## Manpage and git integration

git provides a help system that looks for a manual page named `git-<command>`.
To make `git rewrite --help` show useful documentation, install the packaged
manpage included in this project (`man1/git-rewrite.1`). There are two easy ways:

1) Install with pip (user-wide, installs script + manpage):

    pip install --user .

   This places the `git-rewrite` script under `~/.local/bin` and the manpage under
   `~/.local/share/man/man1` (assuming your Python/pip honors user installs). Make
   sure `~/.local/bin` is in your PATH and `~/.local/share/man` is in your MANPATH
   (most systems include it by default).

2) Manual install of the manpage (if you prefer editable installs):

    install -Dm644 man1/git-rewrite.1 ~/.local/share/man/man1/git-rewrite.1

   If necessary, update the man database (on some systems):

    mandb ~/.local/share/man || true

Notes about usage
- Direct invocation (always shows the Click help):

    git-rewrite <commit-id>

- Git subcommand form (preferred integration):

    git rewrite <commit-id>

  Git finds executables named `git-<command>` in your PATH and exposes them as
  `git <command>`. When you run `git rewrite --help`, Git will display the
  system manpage if available. If you want to force the subcommand to receive
  options (skip Git's help handling), use `--` to separate arguments:

    git rewrite -- --help

  or call the program directly:

    git-rewrite --help

Add a symlink to make the command available system-wide (optional):

    ln -s $(which git-rewrite) ~/.local/bin/git-rewrite

This project installs a basic manpage; feel free to expand it with more
examples, environment notes, or packaging instructions.


