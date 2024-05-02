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
import sys

# from Fasta import Fasta
from BaseClasses import BioBase


# print(f'In the directory: {os.getcwd()}')
avail_programs = glob.glob('./*.py')
avail_programs = [os.path.basename(prg) for prg in avail_programs]
avail_programs = [prg.rsplit('.', 1)[0] for prg in avail_programs]
# print(f'Avaialble programs: {avail_programs}')

def find_file_type(args: list)  -> importlib:
    '''
    This function takes in a list of arguments and determines what type of file
    it is. It then returns the class that can handle that file.
    '''
    type_ = None
    for cnt, arg in enumerate(args):
        if arg.startswith('type:'):
            type_ = args[cnt + 1]
            break
    # print(f'File type: {type_}')
    return type_


if __name__ == "__main__":
    # print(f'Sys.argv: {sys.argv}')
    type_ = find_file_type(sys.argv)
    if type_:
        if type_ in avail_programs:
            import_string = f"GeneralTools.FileClasses.{type_}"
            # print(f'Importing current program: {import_string}')
            current_module = importlib.import_module(import_string)
            # print(f'Current program: {current_module}')
            CurrentClass = getattr(current_module, type_)
            # print(f'{type_}: {CurrentClass}')
            data = CurrentClass()
            if not data.valid:
                data.file_not_valid_report()
            data.run()

        else:
         print(f'Program not found in available programs: {avail_programs} to deal with file type: {type_} Exiting...')
    else:
        print(f'No file type provided. Exiting...')
    # base = BioBase()
    # print(f'\n\n\nFinished top-level init')
    # print(base.conf.show())
    # data = Fasta()  # TODO: Need some way to invoke different classes; perhaps on config?

    # print(f'Output -> Original: {data.file_name}')
    # print(f'Output -> Preferred Name: {data.preferred_file_path}')
    # print(f'Output -> Total seqs: {data.total_seqs}')
    # print(f'Output -> Total seqlen: {data.total_seq_length}')
    # print(f'Output -> Headers: {data.all_headers}')
    # print(f'Output -> Sorted headers: {data.sort_fastaKey()}')
    # print(f'Output -> Rules: {data.available_rules}')
    # print(f'Output -> GC Content: {data.gc_content_total}')
    # print(f'Output -> GC Content: {data.filter_seqlength()}')
    # print(f'Output -> GC Content: {data.n_largest_seqs(n=10)}')
    # print(f'fastaKey: {data.fastaKey}')



# print(Workflow.__file__)
# Initialize a new workflow
# workflow = Workflow()

# Load the Snakefile
# workflow.include("smartparser/master.smk")

# Access rules (indirect and limited)
# rules = workflow.get_rules()
# for rule in rules:
#     print(rule)