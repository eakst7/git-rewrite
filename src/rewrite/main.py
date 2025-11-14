"""CLI entry point for the rewrite package."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

import click


@click.command()
@click.argument("commit_id", required=True)
@click.option(
    "-m",
    "--message",
    default=None,
    help="New commit message (if not provided, keeps original message)",
)
def main(commit_id: str, message: str | None) -> None:
    """Amend a specific commit with the currently staged changes.

    COMMIT_ID is the commit hash (full or abbreviated) to amend.

    The tree will be rebased if necessary to preserve history after the amended commit.

    Example:
        rewrite abc1234
    """
    try:
        # Verify we're in a git repository
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            check=True,
            capture_output=True,
            text=True,
        )

        # Get the full commit hash
        result = subprocess.run(
            ["git", "rev-parse", commit_id],
            check=True,
            capture_output=True,
            text=True,
        )
        full_commit_id = result.stdout.strip()

        # Check if there are staged changes
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            click.echo("No staged changes to commit.", err=True)
            sys.exit(1)

        # Check if the commit to amend is in the history
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", full_commit_id, "HEAD"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            click.echo(
                f"Commit {commit_id} is not an ancestor of HEAD.",
                err=True,
            )
            sys.exit(1)

        # Get the parent commit
        result = subprocess.run(
            ["git", "rev-parse", f"{full_commit_id}^"],
            check=True,
            capture_output=True,
            text=True,
        )
        parent_commit = result.stdout.strip()

        # Create a fixup commit
        fixup_message = f"fixup! {full_commit_id}"
        subprocess.run(
            ["git", "commit", "-m", fixup_message],
            check=True,
        )

        # Get the list of commits to rebase: from parent to current HEAD
        result = subprocess.run(
            ["git", "log", "--oneline", f"{parent_commit}..HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )

        # Create a rebase script that will autosquash
        script_lines: list[str] = []
        for line in result.stdout.strip().split("\n"):
            if line:
                script_lines.append(f"pick {line}")

        # Rebase interactively with autosquash
        env = os.environ.copy()
        env["GIT_EDITOR"] = "true"  # Don't open editor

        try:
            subprocess.run(
                ["git", "rebase", "-i", "--autosquash", parent_commit],
                env=env,
                check=True,
            )

            if message:
                # If a new message was provided, amend the commit message
                subprocess.run(
                    ["git", "show", "-s", "--format=%B", full_commit_id],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                # Create a sed script to replace the message
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    delete=False,
                    suffix=".sh",
                ) as f:
                    script_file = f.name
                    # Use filter-branch to update the commit message
                    f.write(
                        f'#!/bin/bash\n'
                        f'if [ $GIT_COMMIT = $(git rev-parse {full_commit_id}) ]; then\n'
                        f'    echo "{message}"\n'
                        f'else\n'
                        f'    cat\n'
                        f'fi\n'
                    )

                os.chmod(script_file, 0o755)

                try:
                    subprocess.run(
                        [
                            "git",
                            "filter-branch",
                            "-f",
                            "--msg-filter",
                            script_file,
                            f"{parent_commit}..HEAD",
                        ],
                        check=True,
                    )
                finally:
                    os.unlink(script_file)

            click.echo(f"Successfully amended commit {full_commit_id}")

        except subprocess.CalledProcessError:
            click.echo("Rebase failed. Please resolve conflicts and try again.", err=True)
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        if "unknown revision" in str(e) or e.returncode == 128:
            click.echo(f"Error: Could not find commit '{commit_id}'", err=True)
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        click.echo("Error: git not found. Make sure git is installed.", err=True)
        sys.exit(1)


