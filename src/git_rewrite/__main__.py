"""Simple CLI for the rewrite package.

Run with: python -m rewrite
"""
from .main import main

if __name__ == "__main__":
    # Click handles the argument parsing; disable pylint warning about missing args
    main()  # pylint: disable=no-value-for-parameter
