'''
Program that takes a numeric value n and the name of a fasta
file and returns the top n largest entries (key=len(sequence))
$ python -i <myfile.fasta> -n <seqlength_to_filter_(int)> -o <output.fasta>
'''
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
from operator import itemgetter


def get_fasta_dic(file):
    """ Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values """
    fasta_dic = {}
    with open(file) as f:
        for values in SimpleFastaParser(f):
            fasta_dic[values[0]] = values[1]
    return fasta_dic


def write_largest_seqs(file, n, output):
    '''
    Function that takes in a fasta dic and writes a .fasta file
    containing only the top n length sequences.
    '''
    fasta_dic = get_fasta_dic(file)
    top_n = {}
    with open(output, 'w') as o:
        for k in sorted(fasta_dic, key=lambda k: len(fasta_dic[k]), reverse=True)[0:int(n)]:
            line1 = f">{k}\n"
            o.write(line1)
            line2 = f"{fasta_dic[k]}\n"
            o.write(line2)
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
    write_largest_seqs(argument.Input, argument.Length, argument.Output)
