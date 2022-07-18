
'''
Author: Dane
Date: NA
Purpose: Program designed to take in 1+ multifasta files and outputting a tab-delimited
file recording the total nucleotide length, total fasta entries (e.g., contigs), and
the file name. For example, the output would be formatted:
Nucleotides\tContigs\tFile
120000\t10\tSampleA.fasta
80000\t6\tSampleB.fasta

Example usage:
$ python calcBinsetLengths.py -b MySampleBins/*.fasta -o mySampleBinsSizes.txt
'''
import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser


def calcBinSizeAndLength(fasta):
    total_length = 0
    total_count = 0
    with open(fasta) as fasta_file:
        for entry in SimpleFastaParser(fasta_file):
            total_length += len(entry[1])
            total_count += 1
    return total_length, total_count


def main(args):
    fastas, output = args.Fasta, args.Output
    with open(output, 'w') as out:
        out.write(f"Nucleotides\tContigs\tFile\n")
        for fasta in fastas:
            name = os.path.basename(fasta)
            total_length, total_count = calcBinSizeAndLength(fasta)
            out.write(f"{total_length}\t{total_count}\t{name}\n")
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta", help="Fasta files (1+)",
                        required=True, nargs="*")
    parser.add_argument("-o", "--Output", help="Output file",
                        required=True)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
