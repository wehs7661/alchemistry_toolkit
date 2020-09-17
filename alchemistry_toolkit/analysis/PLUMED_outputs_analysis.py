import sys
print(sys.version)
import numpy as np
import argparse
sys.path.append('../')
from alchemistry_toolkit.utils import * 
from alchemistry_toolkit.estimators.free_energy_estimator import FreeEnergy_HILLS

def initialize():
    """
    An argument parser as an initializing function.
    """
    parser = argparse.ArgumentParser(
        description='This code analyzes PLUMED outputs, including performing free energy calculations by running sum_hills on the HILLS file, visualizing the sampling in the configurational space using the COLVAR file or plotting the Gaussian height as a function of time.')
    parser.add_argument('-f',
                        '--hills',
                        type=str,
                        help='The file name of the PLUMED HILLS file.')
    parser.add_argument('-c',
                        '--colvar',
                        help='The file name of the PLUMED COLVAR file.')

    args_parse = parser.parse_args()

    # Below we deal the the cases where any arguments are not specified.
    n_hills, n_colvar = 0, 0  # max should be 1
    if args_parse.hills is None:
        for file in os.listdir('.'):
            if 'HILLS' in file:
                n_hills += 1
                args_parse.hills = file
        if n_hills > 1:
            raise InputFileError('Warning: More than one files contain "HILLS" in their filenames! Please explicitly specify the one of interest.')
        if n_hills == 0:
            raise InputFileError('Warning: No files found to have "HILLS" in their filenames! Please explicitly specify the HILLS file of interest.')

    if args_parse.colvar is None:
        for file in os.listdir('.'):
            if 'COLVAR' in file:
                n_colvar += 1
                args_parse.colvar = file
        if n_colvar > 1:
            raise InputFileError('Warning: More than one files contain "COLVAR" in their filenames! Please explicitly specify the one of interest.')
        if n_colvar == 0:
            raise InputFileError('Warning: No files found to have "COLVAR" in their filenames! Please explicitly specify the COLVAR files of interest.')

    return args_parse

def logger(*args, **kwargs):
    print(*args, **kwargs)
    with open("Results_plumed_outputs_analysis.txt", "a") as f:
        print(file=f, *args, **kwargs)

def main():
    args = initialize()
    logger('============ PLUMED_output_analysis.py ============')
    logger('Part 1: Data analysis of the HILLS file')
    logger('1-1: Free energy calculation based on averaing the deposited hills in the HILLS file')
    t_0 = float(input('Please input the "window time" in ps: '))
    cmd_1 = input('Please input the PLUMED sum_hills without the flag specifying the name of the input HILLS file: ')
    estimator = FreeEnergy_HILLS(args.hills)
    #delta_f_avg = estimator.deltaF_average(t_0, cmd_1)






    # Part 2: Data analysis of the COLVAR file
