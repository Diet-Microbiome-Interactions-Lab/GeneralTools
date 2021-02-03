
from inspect import signature
import sys
from GeneralTools import programs as avail_programs


def main(command, program):
    '''
    Given a list of arguments, parse and test
    '''
    program_info = avail_programs[program]

    print(command)

    # if len(arguments) > max(program_info[1]['argRange']):
    #     sys.stdout.write('Too many arguments!\n')
    # elif len(arguments) < min(program_info[1]['argRange']):
    #     sys.stdout.write('Too many arguments!\n')
    # else:
    #     print('Arguments within range')
