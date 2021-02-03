'''
General warnings to display
'''
import sys
from GeneralTools import programs as avail_programs


def TooFewArgumentsWarning():
    sys.stdout.write('Not enough arguments provided.\n')
    sys.stdout.write('See below for a list of all available programs:\n')
    sys.stdout.write('\n'.join([prg for prg in avail_programs.keys()]) + '\n')
    return 0


def InvalidArgument(arg):
    sys.stdout.write('Unrecognized first positional argument.\n')
    sys.stdout.write(f'{arg} was provided and not recognized.\n')
    sys.stdout.write(f'Too see all arguments, type ...(fill later)\n')
    return 0
