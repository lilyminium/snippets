#!/bin/bash

micromamba activate compare-esps
python generate-psi4-inputs.py CO
psi4 input.dat
python compare-esps.py --molfile mol.sdf --xyzfile final-geometry.xyz