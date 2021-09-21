'''
'''
import sys
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.Seq import Seq


def convert(file, output):
    with open(output, 'w') as out:
        with open(file) as f:
            for values in SimpleFastaParser(f):
                defline = values[0]
                sequence = values[1]
                amino_acids = Seq(sequence).translate()
                out.write(f">{defline}\n{amino_acids}\n")


if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
