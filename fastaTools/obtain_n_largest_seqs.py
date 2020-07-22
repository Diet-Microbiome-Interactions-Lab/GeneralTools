'''
Program that takes a numeric value n and the name of a fasta
file and returns the top n largest sequences
$ python <myfile.fasta> <seqlength_to_filter_(int)> <output.fasta>
'''

import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
from operator import itemgetter


def get_fasta_dic(file):
    """ Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values """
    fasta_dic = {}
    with open(output, 'w') as o:
        with open(file) as f:
            for values in SimpleFastaParser(f):
                fasta_dic[values[0]] = values[1]
        # Filter for top N entries in dictionary
    return fasta_dic


def return_largest_seqs(file, n, output):
    fasta_dic = read_fasta(file)
    top_n = {}
    with open(output, 'w') as o:
        for k in sorted(fasta_dic, key=lambda k: len(fasta_dic[k]), reverse=True)[0:n]:
            o.write(k)
            o.write(fasta_dic[k])
    return 0


if __name__ == "__main__":
    ''' Initialize the arguments to be entered '''
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-i", "--Input", help="Input fasta to be filtered",
                    required=True)
    parser.add_argument("-n", "--Length", help="Length to filter",
                    required=True)
    parser.add_argument("-o", "--Output", help="Output file name",
                    required=True)
    argument = parser.parse_args()
    write_largest_fastas(argument.Input, argument.Length, argument.Output)
