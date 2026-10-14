#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python verify_homotopy_preserving_observations.py | tee verify_homotopy_preserving_observations_local.out
python verify_refinement_subclasses.py | tee verify_refinement_subclasses_local.out
python verify_repair_forest_theorem.py | tee verify_repair_forest_theorem_local.out
