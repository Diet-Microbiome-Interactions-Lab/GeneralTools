''' 
Author: Dane
Date: NA
Purpose: Program that takes two fasta files that will be compared for matching
entries.
This was designed to track how many entries were removed from bin sets after
refinement, and then those removed contigs were compared to the original
bin sets to see how many were removed vs. how many were originally binned.
Example usage:
$ python count_same_fasta.py -1 <firstFile> -2 <secondFile> -o <outfile_name>
'''
import argparse
import os
from Bio import SeqIO


def readFasta(file):
    seq_dict = {rec.id: rec.seq for rec in SeqIO.parse(file, "fasta")}
    return seq_dict


def calcBinSameness(binA, binB):
    shared_contigs = list(binA.keys() & binB.keys())
    shared_quantity = len(shared_contigs)
    shared_len = 0
    for contig in shared_contigs:
        shared_len += len(binA[contig])
    return shared_quantity, shared_len


def calcBinDifference(binA, binB):
    binA_unique_length = 0

    unique_binA = list(binA.keys() - binB.keys())
    binA_unique_quantity = len(unique_binA)
    for value in unique_binA:
        binA_unique_length += len(binA[value])
    return binA_unique_quantity, binA_unique_length


def compare_two_bins(file1, file2):
    binA = readFasta(file1)
    binB = readFasta(file2)

    shared_quantity, shared_len = calcBinSameness(binA, binB)

    binA_unique_quantity, binA_unique_length = calcBinDifference(binA, binB)
    binB_unique_quantity, binB_unique_length = calcBinDifference(binB, binA)

    return [shared_quantity, shared_len,
            binA_unique_quantity, binA_unique_length,
            binB_unique_quantity, binB_unique_length, ]


def main(args):
    file1, file2, output = args.In1, args.In2, args.Output
    stats = compare_two_bins(file1, file2)
    f1 = os.path.basename(file1)
    f2 = os.path.basename(file2)
    with open(output, 'w') as out:
        header = f"SQuant\tSLen\t{f1}_Quant\t{f1}_Len\t{f2}_Quant\t{f2}_Len\n"
        out.write(header)
        writeline = "\t".join(str(stat) for stat in stats) + '\n'
        out.write(writeline)
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-1", "--In1", help="One of two files to compare to one another",
                        required=True)
    parser.add_argument("-2", "--In2", help="One of two files to compare to one another",
                        required=True)
    parser.add_argument("-o", "--Output", help="Output file name",
                        required=True, default="")
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
