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
import os
from Bio import SeqIO


def return_fasta_dic(file):
    """
    Open up a .fasta file and return the entries as a dictionary in the
    form of dic[defline]=seq
    """
    seq_dict = {rec.id: rec.seq for rec in SeqIO.parse(file, "fasta")}
    return seq_dict


def compare_two_bins(file1, file2):
    '''
    Compare how many shared entries there are between two binsets,
    along with differences
    '''
    bin1 = return_fasta_dic(file1)
    bin2 = return_fasta_dic(file2)

    shared_len = 0
    bin1Unique_length = 0
    bin2Unique_length = 0

    sharedContigs = list(bin1.keys() & bin2.keys())
    sharedQuantity = len(sharedContigs)
    for contig in sharedContigs:
        shared_len += len(bin1[contig])

    # Difference: file1 but not file 2
    bin1Unique = list(bin1.keys() - bin2.keys())
    bin1Unique_quantity = len(bin1Unique)
    for value in bin1Unique:
        bin1Unique_length += len(bin1[value])

    # Difference: file 2 but not file 1
    bin2Unique = list(bin2.keys() - bin1.keys())
    bin2Unique_quantity = len(bin2Unique)
    for value in bin2Unique:
        bin2Unique_length += len(bin2[value])

    return [sharedQuantity, shared_len,
            bin1Unique_quantity, bin1Unique_length,
            bin2Unique_quantity, bin2Unique_length]


def write_comparisons(file1, file2, output):
    stats = compare_two_bins(file1, file2)
    f1 = os.path.basename(file1)
    f2 = os.path.basename(file2)
    with open(output, 'w') as o:
        header = "\t".join(["SQuant", "SLen",
                            f"{f1}_Quant",
                            f"{f1}_Len",
                            f"{f2}_Quant",
                            f"{f2}_Len", "\n"])
        o.write(header)
        writeline = "\t".join(str(stat) for stat in stats) + '\n'
        o.write(writeline)
    return 0


if __name__ == "__main__":
    import argparse
    # Arguments
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-1", "--In1", help="One of two files to compare to one another",
                        required=True)
    parser.add_argument("-2", "--In2", help="One of two files to compare to one another",
                        required=True)
    parser.add_argument("-o", "--Output", help="Output file name",
                        required=True, default="")
    argument = parser.parse_args()
    write_comparisons(argument.In1, argument.In2,
                      argument.Output)
