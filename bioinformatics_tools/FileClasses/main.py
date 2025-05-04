'''
This is an exploratory script that takes in an input file and determines
which snakemake rules can be ran on it. Ideally it'd be able to parse a
library of snakemake files and provide some natural-language descriptions
of what the process looks like.

The natural language description of the pipeline would be hard-coded
since we know what input and output to expect.
'''
import argparse
import getpass
import glob
import importlib
import os
from pathlib import Path
import pkgutil
import sys

# from Fasta import Fasta
import bioinformatics_tools
from bioinformatics_tools.FileClasses.BaseClasses import BioBase
from bioinformatics_tools.caragols.logger import LOGGER, config_logging_for_app

package_spec = importlib.util.find_spec("bioinformatics_tools.FileClasses")
package_path = package_spec.submodule_search_locations[0]

raw_programs = [f.rsplit('.', 1)[0] for f in os.listdir(package_path) if f.endswith('.py') and not f.startswith('__')]
raw_programs = [x for x in raw_programs if x != 'main']
avail_programs = [(f, f.lower()) for f in raw_programs]

def find_file_type(args: list) -> None | str:
    '''
    This function takes in a list of arguments and determines what type of file
    it is. It then returns the class that can handle that file.
    '''
    type_ = None
    for cnt, arg in enumerate(args):
        if arg.startswith('type:'):
            type_ = args[cnt + 1]
            type_ = type_.lower()
            break
    return type_


def cli():
    config_logging_for_app()
    startup_info = {
        'cwd': Path.cwd(),
        'user': getpass.getuser(),
        'argv': sys.argv,
        'package_version': bioinformatics_tools.__version__
    }
    LOGGER.debug(f'\nStartup:\n{startup_info}', extra={'startup_info': startup_info}) # user, cwd, sys.argv, app version

    matched = False
    type_ = find_file_type(sys.argv)
    LOGGER.debug(f'Recognize file type: {type_}')
    if type_:
        for program, program_lower in avail_programs:
            if type_ == program or type_ == program_lower:
                matched = True
                LOGGER.debug(f'Matched {program} or {program_lower} to {type_}')
                LOGGER.info(f'✅ Recognized type ({type_}) and matched to module')
                import_string = f"bioinformatics_tools.FileClasses.{program}"
                LOGGER.info(f'Importing {import_string}')
                current_module = importlib.import_module(import_string)
                CurrentClass = getattr(current_module, program)
                
                # Controlling the execution of the class
                data = CurrentClass()  # Shows config
                if not data.valid:
                    LOGGER.debug(f'File provided failed validation test')
                    data.file_not_valid_report()
                # Executing the Class
                data.run()
                # Finishing the Class
            else:
                pass
        if not matched:
            LOGGER.error(f'Program not found in available programs to deal with file type: {type_} Exiting...\n\n')
    else:
        if any(arg in sys.argv for arg in ("help", "Help", "HELP")):
            LOGGER.info('🆘 Help requested')
            LOGGER.info('The following file types are recognized and can be specified via the command line\n\033[92mfileflux type: <file_type>\033[0m')
            help_string = 'Available file types:\n'
            for program, program_lower in avail_programs:
                help_string += f'  {program} or {program_lower}\n'
            LOGGER.info(help_string)
        else:
            LOGGER.error(f'No file type provided. Please specify via the command line\nfileflux type: <file_type>\nExiting...')


if __name__ == "__main__":
    # print(f'Sys.argv: {sys.argv}')
    cli()
