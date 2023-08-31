# Comparing ESPs generated from charges to QM

This snippet compares the ESPs projected onto a grid with the QM ESP.

An example environment is provided in `environment.yaml`.
The actual environment used to execute example files is
provided in `environment-actual.yaml`.

```bash
>>> micromamba activate compare-esps
>>> python generate-psi4-inputs.py CO
>>> psi4 input.dat
>>> python compare-esps.py --molfile mol.sdf --xyzfile final-geometry.xyz
ESP RMSE: 0.0022 hartree / elementary_charge
```

`generate-psi4-inputs.py` generates Psi4 input files for computation.
Importantly, it also generates `mol.sdf` and `grid.dat`.
The `mol.sdf` is where we store the conformer and charges for use in
`compare-esps.py`. The `grid.dat` stores the grid on which the ESP is computed.

If you obtain grids, charges, or ESPs in a different format, please
modify `compare-esps.py` for your own use.