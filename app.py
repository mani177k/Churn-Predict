# Root-level entry point for Streamlit Cloud deployment
# This file simply re-runs the main dashboard app located in the dashboard/ folder

import runpy
import os
import sys
from pathlib import Path

# Ensure the project root is in sys.path so all internal imports resolve
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Run the actual dashboard app
runpy.run_path(str(ROOT_DIR / "dashboard" / "app.py"), run_name="__main__")
