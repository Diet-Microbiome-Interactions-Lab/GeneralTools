'''
Program to filter .FASTA files based on sequences
that are at least N nucleotides long

Example usage:
$ python filterSeqlength.py <input.fasta> <length_threshold> <output.fasta>
'''

import sys
from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser

def filter_fasta(file, size, output):
    """
    Open up a .fasta file and return a dictionary containing the header
    as the key and length as the value
    """
    with open(output, 'w') as o:
        with open(file) as f:
            for values in SimpleFastaParser(f):
                defline = values[0]
                length = len(values[1])
                if length > int(size):
                    o.write(defline)
                    o.write(values[1])
                else:
                    pass
    return 0


if __name__ == "__main__":
    filter_fasta(sys.argv[1], sys.argv[2], sys.argv[3])
