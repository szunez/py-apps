# Converter SPS to OLGA .ppl files
## Purpose
This program reads the output from an SPS simulation script, then writes these data in the OLGA .ppl format.  This program was intended to allow SPS transient profiles to be plotted in flotools, as a temporary measure.

## Execution
This program is run from a UNIX-type commandline interface (CLI), such as GitBash.  The expected input is a .txt file, which was generated from SPS.  Optionally, the output OLGA .ppl file can be assigned Case and Branch labels.  Additionally, horizontal (x) and vertical (y) distance units can be assigned.  Default units for x and y are ‘M’.

### Run
```
$ python get-ppl.py ./path/file.txt [ optional -c Case -b Branch ]
```
### Help
Once installed, the code can be run from command line.  To retrieve help information run the following command
```
$ python get-ppl.py --help
***************************************************************************************************
*     Welcome to get-PPL!, a Python 3.x command-line utility for working with OLGA output data    *
***************************************************************************************************
usage: python get-ppl.py sps_sim_data [--help][--debug][--case][--branch][--x_unit][--y_unit]

where: sps_sim_data is a path and filename of .txt output file [ ./data/P_liq.txt ]

options:
        [--help   [-h][-man] documentation]
        [--debug  [-d] write debug.log file]
        [--case   [-c] define a case name, default case name is 'fake']
        [--branch [-b] define a branch name, default case name is 'fake']
        [--x_unit [-x] specify units for profile distances]
        [--y_unit [-y] specify units for profile variable]
```
