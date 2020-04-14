# QMMin.py

This tool converts a .dat file from QM calculations into a .sdf file containing
the final optimized geometry and the final energy.

## Usage
The following is the format for the commands given to qmmin.py.

```
qmmin.py in_filename [output_sdf_filename]
```

### Parameters
* `in_filename`: the name of the .dat file that came from the QM
  calculations.
* `output_sdf_filename`: the name of the .sdf file where the geometry and
  final energy will be written. Note that `output_sdf_filename` will not be
  checked to see if it ends in `.sdf`. If no filename is passed in,
  `output_sdf_filename` will default to the name of the current working
  directory. If that directory is `/`, then the name will simply be
  `unnamed.sdf`.

### Examples
```
qmmin.py output.dat
```
```
qmmin.py output.dat my_file.sdf
```
