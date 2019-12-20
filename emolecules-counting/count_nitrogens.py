#!/usr/bin/env python3
# Outputs statistics about trivalent nitrogens in various molecules.
#
# Input:
#    - a list of directories, each directory containing mol2 files
#      corresponding to the molecules
# Output:
#    - a CSV in the format {filepath,num} listing the number of trivalent
#      nitrogens in each molecule
#    - a markdown file describing the number of molecules with 0 trivalent
#      nitrogens, 1 trivalent nitrogen, 2, trivalent nitrogens,...
#
# Usage:
#   count_nitrogens.py --dirs DIR1,DIR2,DIR3,... --complete CSV --summary MD
# Example:
#   count_nitrogens.py \
#     --dirs ./1,./2,./3 \
#     --complete complete.csv \
#     --summary results.md
#   # Reads molecules in directories ./1, ./2, and ./3, and writes number of
#   # trivalent nitrogens in each molecule to complete.md, and summary
#   # statistics to results.md

import argparse
import glob
import logging
import sys
from collections import defaultdict
from openeye import oechem
from tqdm import tqdm


def parse_commandline_flags() -> {str: "argument value"}:
    """Uses argparse to handle parsing of command line flags."""
    parser = argparse.ArgumentParser(
        description=
        "Outputs statistics about trivalent nitrogens in various molecules. "
        "See the source for more details.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "--dirs",
        default="",
        metavar="DIR1,DIR2,DIR3,..",
        help="Comma-separated list of directories of mol2 files")
    parser.add_argument(
        "--complete",
        default="./complete.csv",
        metavar="CSV",
        help="CSV file with trivalent nitrogens in each molecule")
    parser.add_argument("--summary",
                        default="./results.md",
                        metavar="MD",
                        help="Output markdown file")
    parser.add_argument(
        "--log",
        default="info",
        metavar="LEVEL",
        help=("logging level - one of DEBUG, INFO, WARNING, ERROR, and CRITICAL"
              " - See https://docs.python.org/3/howto/logging.html for more "
              "information"))

    args = vars(parser.parse_args())
    args["dirs"] = [] if args["dirs"] == "" else args["dirs"].split(",")

    # Print usage if there are no arguments or help is requested
    if len(sys.argv) == 1:
        parser.print_usage(sys.stderr)
        sys.exit(0)

    return args


def configure_logging(loglevel: str):
    """Configures Python's logging library"""
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {loglevel}")
    logging.basicConfig(format="%(levelname)s: %(message)s",
                        level=numeric_level)


def num_nitrogens_in_molecule(mol: oechem.OEMol):
    """
    Counts the number of trivalent nitrogens in the given molecule.
    """
    checker = oechem.OEIsInvertibleNitrogen()
    num_trivalent_nitrogens = 0
    for atom in mol.GetAtoms():
        if checker(atom):
            num_trivalent_nitrogens += 1
    return num_trivalent_nitrogens


def count_in_directories(dirs: [str], complete_csv: "file object") -> {
        int: int
}:
    """
    Counts trivalent nitrogens in mol2 molecules in each directory in
    dirs.

    Write data for each molecule in complete_csv.

    Returns a dictionary mapping the number of trivalent nitrogens to the number
    of molecules having that number.
    """
    counts = defaultdict(int)
    for mol2dir in dirs:
        logging.info("Counting nitrogens in molecules in %s", mol2dir)
        for mol2file in tqdm(glob.iglob(mol2dir + "/*.mol2")):
            istream = oechem.oemolistream(mol2file)
            istream.SetFormat(oechem.OEFormat_MOL2)
            mol = oechem.OEMol()
            oechem.OEReadMolecule(istream, mol)

            n = num_nitrogens_in_molecule(mol)
            counts[n] += 1

            complete_csv.write(f"{mol2file},{n}\n")
    return counts


def save_results(counts: {int: int}, filename: str):
    """Write summary statistics to the given file."""
    logging.info("Saving results to %s", filename)
    f = open(filename, "w")

    # Calculate additional statistics
    mean = sum(num * val for num, val in counts.items()) / sum(counts.values())
    total_molecules = sum(counts.values())
    molecules_with_more_than_0 = total_molecules - counts[0]

    # Header
    f.write("# Trivalent Nitrogen Counts in eMolecules\n")
    f.write("\n")

    # Summary
    f.write(f"Mean: {mean}\n")
    f.write("\n")

    # Table
    col_width = 15
    dashes = '-' * col_width
    f.write(f"| {'# Trivalent N':>{col_width}} | {'Count':>{col_width}} |\n")
    f.write(f"| {dashes} | {dashes} |\n")
    for num in sorted(counts):
        f.write(f"| {num:>{col_width}} | {counts[num]:>{col_width}} |\n")
    f.write(f"| {'total':>{col_width}} | {total_molecules:>{col_width}} |\n")
    f.write(
        f"| {'> 0':>{col_width}} | {molecules_with_more_than_0:>{col_width}} |\n"
    )

    f.close()


def main():
    args = parse_commandline_flags()
    configure_logging(args["log"])

    complete_csv = open(args["complete"], "w")
    complete_csv.write("filepath,count\n")

    counts = count_in_directories(args["dirs"], complete_csv)
    save_results(counts, args["summary"])

    complete_csv.close()


if __name__ == "__main__":
    main()
