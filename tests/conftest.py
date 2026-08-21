import sys
from pathlib import Path

# The app is deployed from a checkout, not installed (see pyproject).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
