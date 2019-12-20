# eMolecules Counting

It is useful to have statistics about the prevalence of trivalent nitrogens in
the eMolecules database, as we can judge the importance of our work on trivalent
nitrogens and improper angles in smirnoff99Frosst. Here, I adapt various parts
of [DANCE](https://github.com/btjanaka/dance) to count the number of molecules
with 0 trivalent nitrogens, 1 trivalent nitrogen, 2 trivalent nitrogens, etc.

## Manifest

- `count_nitrogens.py` - counts the nitrogens in eMolecules
- `count_nitrogens.slurm` - SLURM script for running `count_nitrogens.py` on the
  eMolecules database on Green Planet
- `results.md` - results from running `count_nitrogens.py` on eMolecules
  molecules minimized with smirnoff99Frosst
  - These molecules originate from the 1 September 2016 version of eMolecules
    and are stored on Green Planet as mol2 files in several directories
    - Specifically, the directories are
      `/data15/mobley_temp/kyud/Forcefield_Project/eMolecule/minimized_files/eMolecules_*/SMIRNOFF/`
