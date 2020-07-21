'''
Title: find_no_binners.py
Function: Takes contig reference file and fasta files of bins, and finds contigs that were not binned
Input: python find_no_binners.py -b <list of bin fasta files> -r <reference contig fasta file>
Output: nobinners_<reference contig fasta file>

'''
#!/usr/bin/env python3
import argparse
from Bio import SeqIO
import os
import sys

def nobinners(fasta, reference):
    for seq_record in SeqIO.parse(fasta, "fasta"):
        del reference[seq_record.id]
    return reference

if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--Bins", help="Bin fasta files from which to find nobinners",
                        required=True, nargs='*')
    parser.add_argument("-r", "--Reference", help="Reference contig fasta file to compare bin files to",
                        required=True)
    argument = parser.parse_args()
    reference = SeqIO.to_dict(SeqIO.parse(argument.Reference, 'fasta'))
    for binfile in argument.Bins:
        nobinners(binfile, reference)
    nobinners = "nobinners_" + argument.Reference
    with open(nobinners, 'w') as handle:
        SeqIO.write(reference.values(), handle, 'fasta')
