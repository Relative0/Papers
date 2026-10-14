#!/bin/sh
set -eu
python verify_u1_u6.py
python verify_u3_abstract_independent.py
python verify_cartesian_independent.py
python verify_u4_octahedral_f2.py
python verify_u4_octahedral_Q.py
python verify_chain_adaptive.py
python verify_chain_adaptive_independent.py
