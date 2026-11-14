#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 tools/ai/assign_quantum_profiles.py --check
python3 tests/quantum_ai_profiles.py
# TEST_SOURCES avoids unrelated, outdated trainer_control tests. Include the
# normal runner files automatically; preserve the legacy replay save layout.
make check TEST_SOURCES="${AI_TEST_SOURCES:-test/battle/ai/quantum_ai.c}" \
    TESTLDFLAGS=--gc-sections TESTS="${AI_TEST_PREFIX:-Quantum AI}" "$@"
