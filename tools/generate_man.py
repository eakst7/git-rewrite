#!/usr/bin/env python3
"""Generate the manpage for git-rewrite.

This script **requires** the external program ``help2man``. If ``help2man``
cannot be found in ``PATH`` the script will abort with an error message.

Usage:
    python tools/generate_man.py man1/git-rewrite.1
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def generate_man(output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    help2man = shutil.which("help2man")
    if not help2man:
        print("error: 'help2man' not found in PATH – this script requires help2man.", file=sys.stderr)
        return 1

    # Use help2man to generate a proper manpage from the module entrypoint.
    # We pass the module runner (python -m git_rewrite) as the program to help2man.
    try:
        subprocess.run(
            [help2man, "-o", str(output), sys.executable, "-m", "git_rewrite"],
            check=True,
        )
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"help2man failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/generate_man.py <output-path>", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])
    sys.exit(generate_man(out))
