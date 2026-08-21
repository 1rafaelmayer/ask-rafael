"""Package init, and the only place the environment is loaded.

This runs before any submodule is imported, which matters: `agent.py` reads
configuration at import time, so a later `load_dotenv` would be too late.

In production there is no .env and no python-dotenv installed — Vercel injects
the variables directly — so the import is optional by design rather than by
accident. `override=False` keeps a real environment variable winning over a
stale file, the same rule the MCP server this grew out of uses.
"""

from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # production: the platform supplies the environment
    pass
else:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
