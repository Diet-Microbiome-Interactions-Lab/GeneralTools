'''
This is an exploratory script that takes in an input file and determines
which snakemake rules can be ran on it. Ideally it'd be able to parse a
library of snakemake files and provide some natural-language descriptions
of what the process looks like.

The natural language description of the pipeline would be hard-coded
since we know what input and output to expect.
'''
import argparse
import glob
import importlib
import os
import pkgutil
import sys

# from Fasta import Fasta
from GeneralTools.FileClasses.BaseClasses import BioBase
from GeneralTools.caragols.logger import LOGGER

package_spec = importlib.util.find_spec("GeneralTools.FileClasses")
package_path = package_spec.submodule_search_locations[0]

raw_programs = [f.rsplit('.', 1)[0] for f in os.listdir(package_path) if f.endswith('.py') and not f.startswith('__')]
avail_programs = [(f, f.lower()) for f in raw_programs]

def find_file_type(args: list)  -> importlib:
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
    matched = False
    type_ = find_file_type(sys.argv)
    if type_:
        LOGGER.info(f'Found type: {type_}, we can work with this...')
        for program, program_lower in avail_programs:
            if type_ == program or type_ == program_lower:
                matched = True
                LOGGER.info(f'Matched {program} or {program_lower} to {type_}')
                import_string = f"GeneralTools.FileClasses.{program}"
                current_module = importlib.import_module(import_string)
                CurrentClass = getattr(current_module, program)
                
                data = CurrentClass()
                if not data.valid:
                    data.file_not_valid_report()
                data.run()
            else:
                pass
        if not matched:
            LOGGER.error(f'Program not found in available programs to deal with file type: {type_} Exiting...\n\n')
    else:
        LOGGER.error(f'No file type provided. Please specify via the command line\nfileflux type: <file_type>\nExiting...')


if __name__ == "__main__":
    # print(f'Sys.argv: {sys.argv}')
    cli()

