#!/usr/bin/env python
# Script for converting .dat files to .sdf files.
# See README for usage.

import os
import sys
from openeye import oechem

# Constants

# SDF filename - same name as working directory
dir_name = os.getcwd().split('/')[-1]
DEFAULT_SDF = "unnamed.sdf" if dir_name == "" else dir_name + ".sdf"

# Tell the user how the program should be used
USAGE_MSG = "Proper Usage: qmmin.py in_filename [OUTPUT_SDF_FILENAME]"

# The beginning of the line with the final energy
FINAL_ENERGY_LINE = "Final energy is"

# The beginning of the line that signals the optimized geometry
FINAL_GEOMETRY_LINE = "Final optimized geometry and variables:"

# Number of lines to skip after seeing the FINAL_GEOMETRY line
EXCESS_GEOMETRY_LINES = 5

# The last line of the file should be this if the calculations succeeded
SUCCESS_LINE = "*** Psi4 exiting successfully. Buy a developer a beer!"

# The name of the field that stores the final energy in the SDF file
FINAL_ENERGY_FIELD_NAME = "FINAL_ENERGY"


def print_status(status: str):
    """Prints a short status message to stderr."""
    print(status, file=sys.stderr)


def parse_commandline_flags() -> (str, str):
    """Handles all parsing of command line flags.

    Returns:
        in_filename: name of the input data file to read from
        out_filename: name of the output sdf file to write to
    Raises:
        IndexError: there were not enough command line arguments (i.e. the input
        file was not provided)
        OSError: the input file is an invalid name
    """
    if len(sys.argv) == 1: raise IndexError(USAGE_MSG)
    in_filename = sys.argv[1]
    if not os.path.isfile(in_filename): raise OSError("Input file not found")
    out_filename = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_SDF
    return in_filename, out_filename


def parse_molecule(input_file: "open file") -> oechem.OEGraphMol:
    """Parses the molecule from the open input file. Assumes the FINAL_OPTIMIZED
    line has just been read in the file. Reads until the blank line after the
    molecule in the file.

    Returns:
        molecule: the molecule parsed from the input file
    """
    molecule = oechem.OEGraphMol()
    molecule.SetDimension(3)
    coords = []

    # Clear lines before molecule
    for i in range(EXCESS_GEOMETRY_LINES): input_file.readline()

    line = input_file.readline().strip()
    while line != "":
        tokens = line.split()
        molecule.NewAtom(eval(f"oechem.OEElemNo_{tokens[0]}"))
        coords.extend(map(float, tokens[1:]))
        line = input_file.readline().strip()
    molecule.SetCoords(coords)
    return molecule


def check_last_line(last_line: str, in_filename: str):
    """Checks if the last line of the file indicated success.

    If the last line did not indicate success, an error message is printed.
    However, the program is still allowed to run.
    """
    if last_line != SUCCESS_LINE:
        print_status((f"ERROR: last line of {in_filename} does not indicate "
                       "success. The program will still be allowed to run, "
                       "but results may not be as expected."))


def parse_input_file(in_filename: str) -> oechem.OEGraphMol:
    """Parses the input file for a molecule. The final energy is stored within
    the molecule.

    Returns:
        molecule: the molecule parsed from the input file
    """
    molecule = None
    final_energy = 0.0

    with open(in_filename, "r") as input_file:
        prev = ""  # Remember the previous line so the last line can be checked
        line = input_file.readline()

        while line != "": # Empty string from readline() indicates EOF
            line = line.strip()
            if line.startswith(FINAL_ENERGY_LINE):
                final_energy = float(line.split()[-1])
            if line.startswith(FINAL_GEOMETRY_LINE):
                molecule = parse_molecule(input_file)
                line = ""
            prev = line
            line = input_file.readline()
        check_last_line(prev, in_filename)

    oechem.OEAddSDData(molecule, FINAL_ENERGY_FIELD_NAME, str(final_energy))
    return molecule


def write_output_file(out_filename: str, molecule: oechem.OEGraphMol):
    """Writes the molecule to the output sdf file."""
    ofile = oechem.oemolostream(out_filename)
    ofile.SetFormat(oechem.OEFormat_SDF)
    oechem.OEWriteMolecule(ofile, molecule)
    ofile.close()


if __name__ == "__main__":
    in_filename, out_filename = parse_commandline_flags()
    print_status(f"Parsing {in_filename}")
    molecule = parse_input_file(in_filename)
    print_status(f"Writing data to {out_filename}")
    write_output_file(out_filename, molecule)
    print_status("Done")
