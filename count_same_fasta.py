''' Program that takes 2+ input fasta files and writes
a tab-delimited outputful file with each identifier in one
column and how many shared files it shows in another column
Example usage:
$ python count_same_fasta.py <dir_of_fasta_files> <outputfile>
'''

import os
import sys
from collections import Counter

files = []
mydir = os.getcwd()
# Grab all files following pattern from first argument.
for f in os.listdir(mydir):
    if sys.argv[1] in f:
        files.append(f)


def read_fasta(file):
    """ Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values """
    fasta_dict = {}
    with open(file) as f:
        line = f.readline()
        while line:
            if line.startswith('>') or line.startswith('NODE'):
                header = line.strip('>')
                header = header.strip()
                line = f.readline()
                nucleotides = ''
                file_id = ''
            else:
                nucleotides = nucleotides + line.strip()
                line = f.readline()
                file_id = file.strip()
                fasta_dict[header] = [file_id,
                                      nucleotides
                                      ]
    return fasta_dict


def compile_multiple_fasta_dictionaries(files):
    ''' Compile dictionary data from all .fasta files
    into a list of dictionaries '''
    all_fastas = []
    for file in files:
        all_fastas.append(read_fasta(file))
    return all_fastas


def write_fasta_counts(files, filename):
    falist = []
    dicts = compile_multiple_fasta_dictionaries(files)
    for d in dicts:
        falist = falist + list(d.keys())
    counts = Counter(falist)
    # Write the Counter dictionary object to a file.
    with open(filename, 'w') as file:
        for key, value in counts.items():
            line = (key + '\t' + str(value) + '\n')
            file.write(line)


if __name__ == "__main__":
    write_fasta_counts(files, sys.argv[2])
