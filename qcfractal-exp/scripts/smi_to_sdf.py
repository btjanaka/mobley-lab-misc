#!/usr/bin/env python3
# Converts a SMILES file to a series of SDF files.
# Usage: python smi_to_sdf file.smi directory

import argparse
from pathlib import Path
from openeye import oechem
from openeye import oeomega


def parse_commandline_flags():
    """Parses all command line flags"""
    parser = argparse.ArgumentParser(
        description=(
            "Converts the molecules in the given SMILES file to SDF format "
            "and places them in the given output directory"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "smiles-file", metavar='file.smi', help="SMILES file to convert to SDF")
    parser.add_argument(
        "directory", metavar='directory', help="directory to store SDF files")

    return vars(parser.parse_args())


def fit_smiles_molecule(mol: oechem.OEMol):
    """Modifies the given molecule in-place to give it 3D coordinates"""
    omega = oeomega.OEOmega()
    omega.SetMaxConfs(1)
    omega.SetIncludeInput(True)
    omega.SetCanonOrder(True)
    omega.SetSampleHydrogens(True)
    omega.SetStrictStereo(True)
    omega.SetStrictAtomTypes(True)
    omega.SetIncludeInput(False)
    omega(mol)


def main():
    args = parse_commandline_flags()

    mol = oechem.OEMol()
    ifs = oechem.oemolistream(args["smiles-file"])
    dirpath = Path(args["directory"])
    while oechem.OEReadMolecule(ifs, mol):
        fit_smiles_molecule(mol)
        ofs = oechem.oemolostream(str(dirpath / f"{mol.GetTitle()}.sdf"))
        oechem.OEWriteMolecule(ofs, mol)
        ofs.close()


if __name__ == "__main__":
    main()
