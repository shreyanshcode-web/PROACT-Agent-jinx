"""Agent entrypoint.

This module serves as the CLI bootstrap for the Jinx agent runtime. It
delegates orchestration to ``jinx.orchestrator.main()`` and provides a thin
exception boundary suitable for production usage.

Design goals
------------
* Keep the entrypoint minimal and dependency-light.
* Provide predictable behavior on interrupts.
* Ensure non-zero exit codes on unexpected exceptions.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import warnings
# Suppress SyntaxWarning: invalid escape sequence which appears in some libraries/regexes
warnings.filterwarnings("ignore", category=SyntaxWarning)

# Add the project root to the Python path
project_root = str(Path(__file__).parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Environment variables from .env won't be loaded.")

def _run() -> int:
    """Execute the agent runtime.

    Returns
    -------
    int
        Process exit code. ``0`` on success, non-zero on handled errors.
    """
    try:
        # Import here to avoid circular imports
        from jinx.orchestrator import main as jinx_main
        return jinx_main() or 0
    except ImportError as e:
        print(f"Import error: {e}", file=sys.stderr)
        print("Please make sure all dependencies are installed.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        return 130  # Conventional exit code for SIGINT
    except Exception as exc:  # pragma: no cover - safety net
        # Last-resort guard to avoid silent crashes.
        print(f"Fatal error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(_run())