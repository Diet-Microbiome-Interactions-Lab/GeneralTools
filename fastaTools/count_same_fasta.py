''' Program that takes a group of .fasta files and returns a .tab-separated
spreasheet of each fasta entry and a column showing how many files that
same entry is the same in. If you add the flag --Compare, then the program
will compare the results of the shared fasta entries to that of another
fasta file.
This was designed to track how many entries were removed from bin sets after
refinement, and then those removed contigs were compared to the original
bin sets to see how many were removed vs. how many were originally binned.

Example usage:
$ python count_same_fasta.py -i <fasta_file_pattern> -o <outfile_name> \
-c <original_binset.
$ python count_same_fasta.py -i .fasta -o removed_contigs.txt \
-c original_maxbin_results.fasta
'''

import os
import sys
from collections import Counter
import argparse

''' Initialize the arguments to be entered into program '''

parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-i", "--Input", help="Input file pattern to find common \
    entries", required=True, default=sys.stdin)
parser.add_argument("-o", "--Output", help="Output file name",
                    required=True, default="")
parser.add_argument("-c", "--Compare", help="File to further compare what fasta \
    entries were originally in the bin pre-filtering",
                    required=False, default="")
parser.add_argument("-d", "--Directory", help="Directory containing FASTA files",
                    required=True, default="")
argument = parser.parse_args()

''' Grab all of the files matching the pattern in the current directory '''
files = []
mydir = os.getcwd(argument.Directory)
# Grab all files following pattern from first argument.
for f in os.listdir(mydir):
    if argument.Input in f:
        files.append(f)


def return_fasta_dic(file):
    """
    Open up a .fasta file and return the entries as a dictionary in the
    form of dic[defline]=seq
    """
    seq_dict = {rec.id: rec.seq for rec in SeqIO.parse(file, "fasta")}
    return seq_dict.keys()


def compile_multiple_fasta_dictionaries(files):
    ''' Compile dictionary data from all .fasta files
    into a list of dictionaries '''
    all_fastas = []
    for file in files:
        all_fastas.append(read_fasta(file))
    return all_fastas


def get_original_bins(binfile):
    '''
    Read in a file containing all contigs that were originally
    binned (1 name per line)
    '''
    contigs = []
    with open(binfile) as f:
        line = f.readline()
        while line:
            contigs.append(line.strip())
            line = f.readline()
    return contigs


if__name__ == "__main__":
    if argument.Compare:
        def write_fasta_counts(files, filename, org_file):
            falist = []
            originals = get_original_bins(org_file)
            o_counts = Counter(originals)
            dicts = compile_multiple_fasta_dictionaries(files)
            for d in dicts:
                falist = falist + list(d.keys())
            counts = Counter(falist)
            # Write the Counter dictionary object to a file.
            with open(filename, 'w') as file:
                header = ('Contig\tRemoved\tOriginal\tRatio\n')
                file.write(header)
                for key, value in counts.items():
                    ratio = round(value/(o_counts[key]*2), 2)
                    line = (key + '\t' + str(value) + '\t' +
            str(o_counts[key]*2) + '\t' + str(ratio) + '\n')
                    file.write(line)
        write_fasta_counts(files, argument.Output, argument.Compare)
    else:
        def write_fasta_counts(files, filename):
            falist = []
            dicts = compile_multiple_fasta_dictionaries(files)
            for d in dicts:
                falist = falist + list(d.keys())
            counts = Counter(falist)
            # Write the Counter dictionary object to a file.
            with open(filename, 'w') as file:
                header = ('Contig\tRemoved\n')
                file.write(header)
                for key, value in counts.items():
                    line = (key + '\t' + str(value) + '\n')
                    file.write(line)
