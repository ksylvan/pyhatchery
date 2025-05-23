"""
Allows PyHatchery to be run as a module using `python -m pyhatchery`.
"""

import sys

from .cli import cli

if __name__ == "__main__":
    sys.exit(cli.main())
