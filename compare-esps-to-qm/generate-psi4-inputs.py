import click


TEMPLATE = """\
molecule mol {{
    0 1
{coordinates}
    units angstrom
    no_com
    no_reorient
}}

set {{
  basis 6-31g*
  dft_spherical_points 434
  dft_radial_points 85
  dft_pruning_scheme robust
}}

Ewfn = prop('hf', properties = ['GRID_ESP', 'GRID_FIELD'], return_wfn=True)
mol.save_xyz_file('final-geometry.xyz', 1)
"""


@click.command()
@click.argument("smiles")
def generate_general_inputs(smiles: str):
    import numpy as np
    from openff.units import unit
    from openff.toolkit import Molecule
    from openff.recharge.grids import GridGenerator, GridSettings

    mol = Molecule.from_smiles(smiles, allow_undefined_stereo=True)
    mol.generate_conformers(n_conformers=1)
    mol.assign_partial_charges("am1bcc")
    mol.to_file("mol.sdf", "SDF")
    print("Molecule saved to mol.sdf")
    xyz = mol.conformers[0].m_as(unit.angstrom)

    settings = GridSettings()
    grid = GridGenerator.generate(mol, mol.conformers[0], settings)
    esp_grid = grid.m_as(unit.angstrom)
    np.savetxt("grid.dat", esp_grid)
    print("ESP grid saved to grid.dat")

    coordinate_rows = []
    for i in range(mol.n_atoms):
        symbol = mol.atoms[i].symbol
        x, y, z = xyz[i]
        row = f"    {symbol:<2s} {x: 12.8f} {y: 12.8f} {z: 12.8f}"
        coordinate_rows.append(row)
    
    coordinates = "\n".join(coordinate_rows)
    with open("input.dat", "w") as f:
        f.write(TEMPLATE.format(coordinates=coordinates))
    print("Psi4 input saved to input.dat")


if __name__ == "__main__":
    generate_general_inputs()