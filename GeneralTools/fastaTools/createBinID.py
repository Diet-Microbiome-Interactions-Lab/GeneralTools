'''
Author: Dane
Date: ?
Purpose: Given an multi-fasta and a 1+ bin/fasta files, filter
the multi-fasta so only contains the sequences in/not in the BID file.

Example usage:
$python find_no_binners.py -b <1+_fasta_files.fasta> -a <assembly.fasta>

'''
import os
import sys
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser


def main(args):
    '''
    Add reference into a list index by node name (defline #)
    '''
    log_dic = {}
    # Step 1: Check fasta/bin file(s) and remove contigs from all_contigs
    with open(output, 'w') as out:
        for binfile in fasta:
            log_dic[binfile] = 0
            name = os.path.splitext(os.path.basename(binfile))[0]
            print(f"Now parsing {binfile}")
            assert (binfile.endswith('.fasta')
                    or binfile.endswith('.fa')), "Wrong extension"
            with open(binfile) as bf:
                for values in SimpleFastaParser(bf):
                    out.write(f"{name}\t{values[0]}\n")
                    log_dic[binfile] += 1

    # Optional logging
    if log:
        with open("createBinIDLog.txt", "w") as logfile:
            for bin_ in log_dic.keys():
                logfile.write(f"{bin_} contains {log_dic[bin_]} entries.\n")

    return 0


def parse_args():
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--Bins",
                        help="Bin fasta files from which to find nobinners",
                        required=True, nargs='*')
    parser.add_argument("-a", "--Assembly",
                        help="Assembly contig fasta file to compare bin files to",
                        required=False)
    parser.add_argument("-o", "--Output",
                        help="Output file to write to",
                        required=True)
    parser.add_argument("-l", "--Log",
                        help="Optional log file",
                        required=False, action='store_true',
                        default=False)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
