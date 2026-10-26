"""Compatibility entry point for the overhead gym builder."""
import importlib.util
from pathlib import Path
_p=Path(__file__).with_name('overhead_lock_geometry.py')
_s=importlib.util.spec_from_file_location('overhead_lock_geometry',_p)
_g=importlib.util.module_from_spec(_s);_s.loader.exec_module(_g)
globals().update({k:v for k,v in vars(_g).items() if not k.startswith('_')})
if __name__ in ('__main__','<run_path>'):build()
