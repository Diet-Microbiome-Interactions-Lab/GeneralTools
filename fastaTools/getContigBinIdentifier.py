'''
Program designed to take a directory containing all bin files and output a
tab-delimited file containing contig names in the first column and their
associated bin number in the second column.
The output is in a format that can be directly imported into an Anvio database
using:
$ anvi-import-collection <output-from-this-program.txt> -c $CONTIG_DB -p \
$PROFILE --contig-mode --collection-name "Whatever name you choose!"
Example usage:
$ python getContigBinIdentifer.py <bin-file-format> <output-file-name>
$ python getContigBinIdentifer.py fasta contigs-to-be-imported.txt
'''

import os
import argparse
from Bio import SeqIO


def return_deflines(file):
    """ Open up a .fasta file and return the defline values in a list """
    seq_dict = {rec.id: rec.seq for rec in SeqIO.parse(file, "fasta")}
    return seq_dict.keys()

def read_multiple_fasta(files):
    """ Increase functionality of 'read_fasta' by allowing a list of multiple
    .fasta files to be read in, returning a master dictionary.
    Note: this will not work if multiple .fasta files contain same identifier
    """
    master_dict = {}
    for file in files:
        '''
        The line below may need to be changed depending on how
        the bin files are name!
        '''
        bin_id = os.path.basename(file)
        bin_id = str(file).split('.')[0]
        deflines = return_deflines(file)
        master_dict[bin_id] = deflines
    return master_dict


def write_fa_dict(files, savename):
    """ A function to write .csv values of .fasta output """
    master = read_multiple_fasta(files)
    header = f"Contig\tBin\n"
    with open(savename, 'w') as o:
        o.write(header)  # First row (keys of dict)
        for bin_id, deflines in master.items():
            for defline in deflines:
                bin_id = os.path.basename(bin_id)
                line = f"{bin_id}\t{defline}\n"
                o.write(line)


if __name__ == "__main__":
    ''' Initialize the arguments to be entered '''
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-d", "--Directory", help="Directory containing files",
                        required=True)
    parser.add_argument("-o", "--Output", help="Output file name",
                        required=True)
    argument = parser.parse_args()
    files = []
    mydir = os.getcwd()
    for f in os.listdir(argument.Directory):
        if (f.endswith('.fasta') or f.endswith('.fa')):
            files.append(os.path.join(argument.Directory, f))
    write_fa_dict(files, argument.Output)
