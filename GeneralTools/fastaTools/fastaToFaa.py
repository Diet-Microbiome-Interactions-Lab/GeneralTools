'''
'''
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.Seq import Seq


def main(args):
    fasta_file, output = args.Fasta, args.Output
    with open(output, 'w') as out:
        with open(fasta_file) as f:
            for values in SimpleFastaParser(f):
                defline = values[0]
                sequence = values[1]
                amino_acids = Seq(sequence).translate()
                out.write(f">{defline}\n{amino_acids}\n")


def parse_args():
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Input fasta file.",
                        required=True)
    parser.add_argument("-o", "--Output",
                        help="Output faa file.",
                        required=True)
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    main(args)
