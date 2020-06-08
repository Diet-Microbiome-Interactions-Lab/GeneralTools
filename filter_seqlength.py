''' Program to filter .FASTA files based on sequences
that are at least N nucleotides long

Example usage:
$ python2 filter_seqlength.py <input.fasta> <length_threshold> <output.fasta>
'''

import sys


def read_fasta(file):
    """ Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values """
    fasta_dict = {}
    with open(file) as f:
        line = f.readline()
        while line:
            if line.startswith('>') or line.startswith('NODE'):
                header = line.strip()
                line = f.readline()
                nucleotides = ''
            else:
                nucleotides = nucleotides + line.strip()
                line = f.readline()
                fasta_dict[header] = nucleotides
    return fasta_dict


def filter_fasta(file, length):
    fa = read_fasta(file)
    for key in fa.keys():
        if len(fa[key]) < length:
            fa.pop(key)
    return fa


def write_fasta(file, length, output):
    filtered = filter_fasta(file, int(length))
    with open(output, 'w') as o:
        for key, value in filtered.items():
            o.write(key)
            o.write('\n')
            o.write(value)
            o.write('\n')


if __name__ == "__main__":
    write_fasta(sys.argv[1], sys.argv[2], sys.argv[3])
