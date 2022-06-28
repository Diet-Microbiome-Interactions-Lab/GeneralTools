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

import FastaClasses


def write_fastas(binfile, header, assemblyfile, outdirectory):
    try:
        os.mkdir(outdirectory)
    except FileExistsError:
        pass

    BinID = FastaClasses.BinID(binfile, header=header)
    bin_dic = BinID.bin_dic
    for record in SeqIO.parse(assemblyfile, "fasta"):
        match = record.id.strip('>')
        if match in bin_dic:
            outfile = f"{outdirectory}/Bin.{bin_dic[match]}.fasta"
            with open(outfile, 'a') as _out:
                _out.write(f">{record.id}\n{record.seq}\n")
    return 0


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta", help="Assembly file",
                        required=True)
    parser.add_argument("-b", "--Bins", help="File containing bins",
                        required=True)
    parser.add_argument("-o", "--Output",
                        help="Output directory to write to",
                        required=True)
    parser.add_argument("-h", "--Header",
                        required=False, default=False)
    args = parser.parse_args()
    write_fastas(args.Bins, args.Fasta, args.FastaDirectory, args.Header)
