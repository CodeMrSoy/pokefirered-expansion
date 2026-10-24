#!/usr/bin/env python3
"""Run release-ROM regressions; keep every log and report all failures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    'randomizer_regressions', 'window_lighting_assets', 'quantum_title_emulator',
    'qol_intro_running_emulator', 'avatar_wardrobe_emulator',
    'pokeglass_grid_emulator', 'pokeglass_stats_emulator',
    'pokeglass_shell_emulator', 'pokeglass_transition_emulator',
    'pokeglass_party_text_emulator', 'pokeglass_party_visual_emulator',
    'pokeglass_storage_emulator', 'pokeglass_storage_visual_emulator', 'pokeglass_pokedex_emulator',
    'rom_cleanup_inventory', 'rom_cleanup_storage_emulator',
    'rom_cleanup_migration_emulator', 'rom_cleanup_old_save_emulator',
    'rom_cleanup_maps_emulator', 'quantum_qol_emulator',
    'window_lighting_emulator', 'pokeglass_party_return_emulator',
    'rom_cleanup_world_integrity', 'rom_cleanup_safety_emulator',
    'rom_cleanup_progression_emulator', 'field_tools_emulator', 'field_tool_rewards_emulator', 'field_item_case_emulator',
)

def main():
    output = ROOT/'build/thorough-validation'
    output.mkdir(parents=True, exist_ok=True)
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for test in TESTS:
        start = time.monotonic()
        with (output/(test+'.log')).open('w') as log:
            try:
                result = subprocess.run([sys.executable, str(ROOT/'tests'/(test+'.py'))],
                                        cwd=ROOT, env=env, stdout=log,
                                        stderr=subprocess.STDOUT, timeout=480)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
                log.write('\nTimed out after 480 seconds.\n')
        results.append(dict(test=test, exit_code=code, seconds=round(time.monotonic()-start,2)))
        (output/'results.json').write_text(json.dumps(results, indent=2)+'\n')
        print(f'{"PASS" if code == 0 else "FAIL"} {test}', flush=True)
    failures = sum(row['exit_code'] != 0 for row in results)
    print(f'{len(results)-failures}/{len(results)} passed; logs: {output}', flush=True)
    return bool(failures)

if __name__ == '__main__':
    sys.exit(main())
