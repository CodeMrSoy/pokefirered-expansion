"""Rebuild the Captain's Trial, then apply its native-tile Nordic shipyard art pass."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[2]
runpy.run_path(str(R/'tools/havora/build_captains_trial_base.py'))
runpy.run_path(str(R/'tools/havora/style_captains_trial.py'))
runpy.run_path(str(R/'tools/havora/build_fixed_transfer_gym.py'))
