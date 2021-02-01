#!/Users/ddeemer/.pyenv/versions/3.9.0/bin/python
import importlib
import sys
from GeneralTools import programs as avail_programs
from GeneralTools import main_help as main_help
# from GeneralTools.fastaTools.fastaStats import save_fa_dict as fastStats


def main(arguments, args=avail_programs):
    '''
    First thing is to test if the argument is in our dictionary
    '''

    help_flags = ['--help', '-h', '-H']

    if len(arguments) < 1:
        print('Not enough arguments provided!')
    else:
        if arguments[0] in help_flags:
            print(main_help)
            return 0
        elif arguments[0] in avail_programs:
            print(f"Argument: {arguments[0]}")
            print(f"Values: {avail_programs[arguments[0]]}")
            if any(x in help_flags for x in arguments):
                print(avail_programs[arguments[0]][1]['help'])
            else:
                # _test = f"GeneralTools.fastaTools.{arguments[0]}"
                full_module = f"GeneralTools.fastaTools.{arguments[0]}"
                current_program = importlib.import_module(full_module)
                current_program.main([arguments[1]], arguments[2])
                return 0
        else:
            print('Not a valid program. See help.')


if __name__ == '__main__':
    arguments = sys.argv[1:]
    print(f"Printing all arguments: {arguments}")
    # print(arguments, avail_programs)
    main(arguments)
