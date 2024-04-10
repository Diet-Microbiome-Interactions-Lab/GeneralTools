#!/Users/ddeemer/Library/CloudStorage/OneDrive-purdue.edu/GeneralTools/.venv/bin/python
import glob
import importlib
import logging
import os
import sys

from caragols.lib import clix
from GeneralTools import fastaTools_programs as program_info
from GeneralTools import main_help
from GeneralTools.Utilities import warnings, shellOutput

# TODO  - Below, make a shared module to get available programs!
avail_programs = glob.glob('../GeneralTools/fastaTools/*.py')

avail_programs = [os.path.basename(prg) for prg in avail_programs]
avail_programs = [prg.rsplit('.', 1)[0] for prg in avail_programs]


class FastaTools(clix.App):
    DEFAULTS = {
        "log.level": logging.WARNING,
        "log.key": "toad_test",
        "report.form": "prose"
    }

    def __init__(self):
        clix.App.__init__(self, name="FastaTools", defaults=self.DEFAULTS)


def main(command):
    '''
    First thing is to test if the argument is in our dictionary
    arguments = sys.argv[1:]
    main(arguments)
    '''
    # app = FastaTools()
    # comargs = sys.argv[1:]
    # myapp.conf.sed(comargs)

    help_flags = ['--help', '-h', '-H']
    use_flags = ['--use', '--Use']
    if len(command) < 1:
        print(main_help, '\n')
        warnings.TooFewArgumentsWarning()
    else:
        program = command[0]
        if program in help_flags:
            shellOutput.printMainExecutableHelp(__file__)
            shellOutput.printAvailablePrograms(__file__, program_info)
            return 0
        elif program in ['--list', '-L', '--List']:
            shellOutput.printAvailablePrograms(sys.argv[0], program_info)
        elif program in avail_programs:
            # if any(x in use_flags for x in command) or len(command) == 1:
            #     try:
            #         shellOutput.printSubprogramHelp(program, avail_programs)
            #     except IndexError:
            #         print(
            #             f"No program information in __init__ file yet for {program}\n")
            # else:  # Run parse the arguments and run!
            imp_mod = f"GeneralTools.fastaTools.{program}"
            current_program = importlib.import_module(imp_mod)
            parser = current_program.parse_args()
            args = parser.parse_args(command[1:])
            current_program.main(args)

            return 0
        else:
            warnings.InvalidArgumentOrSubprogram(program)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    main(arguments)

# if __name__ == "__main__":
#     myapp = FastaTools()
#     comargs = sys.argv[1:]
#     myapp.conf.sed(comargs)

