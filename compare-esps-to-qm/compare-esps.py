import click
import typing

from openff.units import unit
import numpy as np

AU_ESP = unit.atomic_unit_of_energy / unit.elementary_charge

def calculate_esp(
    grid_coordinates: unit.Quantity,  # N x 3
    atom_coordinates: unit.Quantity,  # M x 3
    charges: unit.Quantity,  # M
    with_units: bool = False,
) -> unit.Quantity:
    """Calculate ESP from grid"""
    ke = 1 / (4 * np.pi * unit.epsilon_0)
    
    grid_coordinates = grid_coordinates.reshape((-1, 3))
    atom_coordinates = atom_coordinates.reshape((-1, 3))
    displacement = grid_coordinates[:, None, :] - atom_coordinates[None, :, :]  # N x M x 3
    distance = (displacement ** 2).sum(axis=-1) ** 0.5  # N x M
    inv_distance = 1 / distance

    esp = ke * (inv_distance @ charges)  # N

    esp_q = esp.m_as(AU_ESP)
    if not with_units:
        return esp_q
    return esp


def load_geometry_from_xyz(xyzfile: str):
    arr = np.loadtxt(xyzfile, skiprows=2, usecols=(1, 2, 3))
    return arr * unit.angstrom


@click.command()
@click.option(
    "--molfile",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    help="Molecule file (SDF)",
)
@click.option(
    "--gridfile",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    default="grid.dat",
    help="ESP grid file (Angstrom)",
)
@click.option(
    "--espfile",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    default="grid_esp.dat",
    help="ESP file (Hartree/e) -- output of Psi4",
)
@click.option(
    "--xyzfile",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    default=None,
    help="XYZ file (Angstrom) -- likely called final-geometry.xyz",
)
def compare_esps(
    molfile: str = "mol.sdf",
    gridfile: str = "grid.dat",
    espfile: str = "grid_esp.dat",
    xyzfile: typing.Optional[str] = None
):
    from openff.toolkit import Molecule
    
    mol = Molecule.from_file(molfile, "SDF")
    if xyzfile is not None:
        mol._conformers = [load_geometry_from_xyz(xyzfile)]

    grid = np.loadtxt(gridfile)
    esp = np.loadtxt(espfile) * AU_ESP

    computed_esp = calculate_esp(
        grid * unit.angstrom,
        mol.conformers[0],
        mol.partial_charges,
        with_units=True
    )

    np.savetxt("computed-esp.dat", computed_esp.m_as(AU_ESP))

    esp_rmse = ((computed_esp - esp) ** 2).mean() ** 0.5
    print(f"ESP RMSE: {esp_rmse.m_as(AU_ESP):.4f} {AU_ESP}")


if __name__ == "__main__":
    compare_esps()