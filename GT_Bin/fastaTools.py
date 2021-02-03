#!/Users/ddeemer/.pyenv/versions/3.9.0/bin/python
import importlib
from inspect import signature
import sys
from GeneralTools import programs as avail_programs
from GeneralTools import main_help as main_help
from GeneralTools import warnings
from GeneralTools import argumentParser
# from GeneralTools.fastaTools.fastaStats import save_fa_dict as fastStats


# Put this somewhere else
def PrintHelp(program, avail_programs):
    print(f"Main help page for {program}")


def main(command):
    '''
    First thing is to test if the argument is in our dictionary
    '''

    help_flags = ['--help', '-h', '-H']
    print(command)
    if len(command) < 1:
        warnings.TooFewArgumentsWarning()
    else:
        program = command[0]
        if program in help_flags:
            print(main_help)
            return 0
        elif program in avail_programs:
            print(f"Found the program: {command[0]}...continuing\n")
            # print(f"Information: {avail_programs[program]}\n")
            if any(x in help_flags for x in command) or len(command) == 1:
                # Below, a potential for another class (help)
                # print(avail_programs[program][1]['help'])
                PrintHelp(program, avail_programs)
            else:  # Run parse the arguments and run!
                imp_mod = f"GeneralTools.fastaTools.{program}"
                current_program = importlib.import_module(imp_mod)
                # p_sig = signature(current_program.main)

                # Now we need a solution to feed the correct command to the program
                a = argumentParser.main(command[1:], program)
                # print(a)

                # current_program.main([arguments[1:]])
                return 0
        else:
            warnings.InvalidArgument(program)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    # print(arguments, avail_programs)
    main(arguments)
