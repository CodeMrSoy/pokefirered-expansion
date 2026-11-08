"""Compatibility entry point: full-flood tide tests supersede partial tide fixtures."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("corvala_tides_emulator.py")), run_name="__main__")
