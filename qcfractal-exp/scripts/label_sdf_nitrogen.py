#!/usr/bin/env python3
# Script to find the indices of nitrogens and their neighbors and output them as
# a csv file
# Usage: python label_sdf_nitrogen.py [DIRECTORY] [FILENAME]

import sys
import json
from glob import iglob
from pathlib import Path

from openeye import oechem


def parse_commandline_flags() -> {str: "argument"}:
    args = {}
    if len(sys.argv) != 3:
        print("Usage: python label_sdf_nitrogen.py [DIRECTORY] [FILENAME]")

    args["directory"] = sys.argv[1]
    args["filename"] = sys.argv[2]

    return args


# Custom exception for the case when there is no nitrogen
class NoNitrogenException(Exception):
    pass


def find_nitrogen(mol):
    """Returns the trivalent nitrogen atom in a molecule"""
    for atom in mol.GetAtoms():
        if oechem.OEIsInvertibleNitrogen()(atom):
            return atom, atom.GetIdx()
    raise NoNitrogenException()


def main():
    args = parse_commandline_flags()

    final_indices = {}

    for filepath in iglob(f"{args['directory']}/*.sdf"):
        print(filepath)
        ifs = oechem.oemolistream(filepath)
        mol = oechem.OEMol()
        oechem.OEReadMolecule(ifs, mol)
        nitrogen, index = find_nitrogen(mol)
        indices = [index
                  ] + [nbor.GetIdx() for nbor in list(nitrogen.GetAtoms())]

        filename = filepath.split('/')[-1]
        final_indices[filename] = indices

    json.dump(final_indices, open(args["filename"], "w"))


if __name__ == "__main__":
    main()
