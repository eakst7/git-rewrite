#!/usr/bin/env python3
"""Check that the tracked manpage is up-to-date.

This script generates a temporary manpage (using the same logic as
tools/generate_man.py) and compares it to the committed `man1/git-rewrite.1`.
It exits non-zero if they differ (so it can be used in pre-commit).
"""
from __future__ import annotations

import filecmp
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
MAN = ROOT / "man1" / "git-rewrite.1"


def run_check() -> int:
    if not MAN.exists():
        print(f"Tracked manpage {MAN} not found.", file=sys.stderr)
        return 2

    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()

    gen_script = TOOLS / "generate_man.py"
    if not gen_script.exists():
        print(f"Generator script {gen_script} missing.", file=sys.stderr)
        return 3

    # Prefer the repository virtualenv python when available so generated
    # manpages match the environment developers use. Fall back to system
    # python if not found.
    venv_python = ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        python = str(venv_python)
    else:
        python = shutil.which("python") or sys.executable

    try:
        subprocess.run([python, str(gen_script), str(tmp_path)], check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Manpage generation failed: {exc}", file=sys.stderr)
        return 4

    same = filecmp.cmp(tmp_path, MAN, shallow=False)
    if same:
        print("Manpage is up-to-date.")
        tmp_path.unlink()
        return 0

    print("Manpage is out-of-date. Diff:")
    try:
        diff = subprocess.run(["diff", "-u", str(MAN), str(tmp_path)], capture_output=True, text=True, check=False)
        print(diff.stdout)
    except subprocess.SubprocessError:
        print("Could not produce diff; files differ.")

    # leave the tmp file for inspection
    print(f"Generated manpage left at: {tmp_path}")
    return 1


if __name__ == "__main__":
    sys.exit(run_check())
