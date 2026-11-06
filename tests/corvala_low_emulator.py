"""Compatibility entry point for the current Corvala LOW cove checks."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("corvala_cove_emulator.py")), run_name="__main__")
