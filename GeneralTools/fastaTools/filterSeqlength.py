'''
Author: Dane
Date: 18Dec20
Purpose: Program to filter .FASTA files based on sequences that are at
least N nucleotides long

Example usage:
$ python filterSeqlength.py <input.fasta> <length_threshold> <output.fasta>
'''
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser


def main(args):
    """
    Open up a .fasta file and return a dictionary containing the header
    as the key and length as the value
    """
    file, size, output = args.Assembly, args.Length, args.Output
    with open(output, 'w') as o:
        with open(file) as f:
            for values in SimpleFastaParser(f):
                defline = values[0]
                length = len(values[1])
                if length > int(size):
                    o.write('>' + defline + '\n')
                    o.write(values[1] + '\n')
                else:
                    pass
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-a", "--Assembly",
                        help="Assembly to filter", required=True)
    parser.add_argument("-l", "--Length",
                        help="Length to filter fasta by", required=True)
    parser.add_argument("-o", "--Output",
                        help="Output filtered fasta file to write to",
                        required=True)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
