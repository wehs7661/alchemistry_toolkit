import sys
import argparse

def initialize():
    """
    An argument parser as an initializing function.
    """

    parser = argparse.ArgumentParser(
        description='This code analyzes the log file generated from expanded ensemble simulation or alchemicl metadynamics.')
    parser.add_argument('-l',
                        '--log',
                        type=str,
                        help='The filename(s) of the log file.')
    parser.add_argument('-p',
                        '--prefix',
                        type=str,
                        help='The common prefix of the input/output files.')
    parser.add_argument('-a',
                        '--avg_len',
                        type=float,
                        help='The length of the simulation over which the weights are averaged in the weights avererage calculation. -a 20 means that the weights of the last 20 ns before the weights are equilibrated/before the simulation ends (dependes on the flat -t) will be averaged.')
    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='stor_true',
                        help='Whether to turn on the verbose mode.')

    args_parse = parser.parse_args(args)

    # Below we deal with the cases where any arguments are not specified.
    # 1. Try to find 
