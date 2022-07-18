# ARGUMENT -F --FASTADIRECTORY
# ARGUMENT -H --HEADER
"""
Author: Dane Deemer
Program designed to take in an assembly file and a bin identification file and
output a series of multi-fasta files (one corresponding to each bin in
the bin identification file).

Example usage:
$ python writeFastaFromBinID.py --Fasta <file.fasta> --Bins <binID.txt> \
--Output <output_location>
"""
import argparse
from Bio import SeqIO
import os

from .FastaClasses import BinID


def main(args):
    binfile, assemblyfile = args.Bins, args.Fasta
    outdirectory, header = args.Output, args.Header
    try:
        os.mkdir(outdirectory)
    except FileExistsError:
        pass

    binid = BinID(binfile, header=header)
    bin_dic = binid.bin_dic
    for record in SeqIO.parse(assemblyfile, "fasta"):
        match = record.id.strip('>')
        if match in bin_dic:
            outfile = f"{outdirectory}/Bin.{bin_dic[match]}.fasta"
            with open(outfile, 'a') as _out:
                _out.write(f">{record.id}\n{record.seq}\n")
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta", help="Assembly file",
                        required=True)
    parser.add_argument("-b", "--Bins", help="File containing bins",
                        required=True)
    parser.add_argument("-o", "--Output",
                        help="Output directory to write to",
                        required=True)
    parser.add_argument("--Header",
                        required=False, default=False)
    return parser


if __name__ == "__main__":
    """ Arguments """
    parser = parse_args()
    args = parser.parse_args()
    main(args)
