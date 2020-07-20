''' Program to filter .FASTA files based on sequences
that are at least N nucleotides long

Example usage:
$ python filter_seqlength.py <input.fasta> <length_threshold> <output.fasta>
'''

import sys


def filter_fasta(file, size, output):
    """ Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values """
    fasta_dict = {}
    with open(output, 'w') as o:
        with open(file) as f:
            line = f.readline()
            while line:
                if line.startswith('>') or line.startswith('NODE'):
                    header = line
                    nucleotides = ""
                    line = f.readline()
                    while (line and not line.startswith('>')):
                        nucleotides = nucleotides + line.strip()
                        line = f.readline()
                    if len(nucleotides) > int(size):
                        o.write(header)
                        o.write(nucleotides)
                    else:
                        pass
                else:
                    line = f.readline()
    return fasta_dict


if __name__ == "__main__":
    filter_fasta(sys.argv[1], sys.argv[2], sys.argv[3])
