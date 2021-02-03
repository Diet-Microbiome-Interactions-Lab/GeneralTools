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
from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser
import argparse
import os


def gc_cont(string):
    """
    Function to be used inside of 'read_fasta' in order to obtain
    gc_content of a string
    """
    string = string.upper()
    g = string.count('G')
    c = string.count('C')
    return round((g + c) / len(string), 3)


def basic_fasta_stats(file):
    """
    Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values
    """
    fasta_dict = {}
    with open(file) as f:
        for values in SimpleFastaParser(f):
            defline = values[0]
            length = len(values[1])
            gc = gc_cont(values[1])
            fasta_dict[defline] = [length, gc]
    return fasta_dict


def read_multiple_fasta(files):
    """
    Increase functionality of 'read_fasta' by allowing a list of multiple
    .fasta files to be read in, returning a master dictionary.
    Note: this will not work if multiple .fasta files contain same identifier
    """
    master_dict = {}

    for file in files:
        fasta_dict = basic_fasta_stats(file)
        master_dict[os.path.basename(str(file))] = fasta_dict

    return master_dict


def main(files, output, bin=False):
    """
    A function to write .txt values of .fasta output
    """
    dictionary = read_multiple_fasta(files)

    with open(output, 'w') as o:
        if not bin:
            header = 'File\tContig\tLength\tGC_Content\n'
            o.write(header)  # First row (keys of dict)
            for file in dictionary:
                for defline, stats in dictionary[file].items():
                    line = [file, defline] + [str(stat) for stat in stats]
                    line = '\t'.join(line) + '\n'
                    o.write(line)
        if bin:
            header = 'Bin\tCount\tLength\tGC_Content\n'
            o.write(header)
            for file in dictionary:
                total_length = 0
                GC = 0
                count = 0
                for defline, stats in dictionary[file].items():
                    count += 1
                    total_length += stats[0]
                    GC += stats[1]
                GC = GC / count
                writeline = "\t".join(
                    [file, str(count), str(total_length), str(GC)]) + "\n"
                o.write(writeline)
    return 0


if __name__ == "__main__":
    print('Running in main!!!')
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--FASTA",
                        help="FASTA files to parse (can be multiple)",
                        required=True, nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output file to write to",
                        required=True)
    parser.add_argument("-b", "--Bin",
                        help="Get information on a bin-by-bin level",
                        action='store_true', required=False)
    argument = parser.parse_args()
    main(argument.FASTA, argument.Output, bin=argument.Bin)
