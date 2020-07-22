"""
Function that requires: 1+ .FASTA files and
writes a csv files containing: .fasta description,
what file it came from (bin), length, and GC content

Example use:
$ python fasta_dict.py .fasta <savename.csv>
"""
from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser
import argparse


def gc_cont(string):
    """
    Function to be used inside of 'read_fasta' in order to obtain
    gc_content of a string
    """
    string = string.upper()
    g = string.count('G')
    c = string.count('C')
    leng = float(len(string))
    gc = float((g + c))
    return round(gc / leng, 3)


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
        master_dict[str(file)] = fasta_dict
    return master_dict


def save_fa_dict(files, output):
    """
    A function to write .csv values of .fasta output
    """
    dictionary = read_multiple_fasta(files)
    header = 'File\tContig\tLength\tGC_Content\n'
    with open(output, 'w') as o:
        o.write(header)  # First row (keys of dict)
        for file in dictionary:
            for defline, stats in dictionary[file].items():
                line = [file, defline] + [str(stat) for stat in stats]
                line = '\t'.join(line) + '\n'
                o.write(line)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--FASTA",
                        help="FASTA files to parse",
                        required=True, nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output file to write to",
                        required=True)
    argument = parser.parse_args()
    save_fa_dict(argument.FASTA, argument.Output)
