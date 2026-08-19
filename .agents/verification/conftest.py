"""
Pytest configuration for Riemann Microscope mathematical verification suite.
"""
import sys
from pathlib import Path

# Ensure .agents is in Python path for verification imports
agents_dir = Path(__file__).resolve().parent.parent
if str(agents_dir) not in sys.path:
    sys.path.insert(0, str(agents_dir))
