'''
Author: Dane
Date: 29Oct21
Purpose: Write a bin identification file from 1+ fasta files

Example usage:
$python find_no_binners.py -b <1+_fasta_files.fasta>

'''
import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser


def main(args):
    output, fasta = args.Output, args.Fasta
    with open(output, 'w') as out:
        for binfile in fasta:
            name = os.path.splitext(os.path.basename(binfile))[0]
            assert binfile.endswith(
                ('.fasta', '.fa', '.fna')), "Wrong extension"
            with open(binfile) as bf:
                for values in SimpleFastaParser(bf):
                    out.write(f"{values[0]}\t{name}\n")
    return 0


def parse_args():
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Fasta files to write bin IDs from.",
                        required=True, nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output bin ID file to write to",
                        required=True)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
