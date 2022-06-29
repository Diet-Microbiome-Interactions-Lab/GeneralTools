"""
Author: Dane
Date: NA
Purpose: Function that requires: 1+ .FASTA files and
writes a tab-delimited files containing:
fasta description, what file it came from (bin), length, and GC content.
If the option --Bin is used, it will also create a shortened
file with statistics for each bin (instead of for each contig).
Example use:
$ python fasta_dict.py .fasta <savename.csv>
"""
from Bio.SeqIO.FastaIO import SimpleFastaParser
import argparse
import os


def gcContent(string):
    """
    Function to be used inside of 'read_fasta' in order to obtain
    gcContentent of a string
    """
    string = string.upper()
    g = string.count('G')
    c = string.count('C')
    return round((g + c) / len(string), 3)


def basic_fasta_stats(file):
    fasta_dict = {}
    with open(file) as f:
        for values in SimpleFastaParser(f):
            defline, sequence = values[0:2]
            length = len(sequence)
            gc = gcContent(sequence)
            fasta_dict[defline] = [length, gc]
    return fasta_dict


def prettyName(filename):
    return os.path.basename(os.path.splitext(filename)[0])


def loopFastaAndWriteStats(files):
    master_dict = {}
    for file in files:
        fasta_dict = basic_fasta_stats(file)
        filename_key = prettyName(file)
        master_dict[filename_key] = fasta_dict
    return master_dict


def main(args):
    files = args.Fasta
    output = args.Output
    bin_ = args.Bin
    all_fasta_file_stats = loopFastaAndWriteStats(files)

    with open(output, 'w') as out:
        if not bin_:
            header = 'File\tContig\tLength\tGC_Content\n'
            out.write(header)
            for fasta_file in all_fasta_file_stats:
                count, total_length, GC = 0, 0, 0
                for defline, stats in all_fasta_file_stats[fasta_file].items():
                    if bin_:
                        count += 1
                        total_length += stats[0]
                        GC += stats[1]
                    else:
                        writeline = f"{fasta_file}\t{defline}\t{stats[0]}\t{stats[1]}\n"
                        out.write(writeline)
                if bin_:
                    GC = GC / count
                    writeline = f"{file}\t{fasta_count}\t{total_length}\t{GC}\n"
                    out.write(writeline)
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Fasta files to parse (can be multiple)",
                        required=True, nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output file to write to",
                        required=True)
    parser.add_argument("-b", "--Bin",
                        help="Get information on a bin-by-bin level",
                        action='store_true', required=False)
    return parser


if __name__ == "__main__":
    print('Running in main!!!')
    parser = parse_args()
    args = parser.parse_args()
    print(args)
    main(args)
