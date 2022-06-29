from Bio.SeqIO.FastaIO import SimpleFastaParser
import argparse
import os


def main(args):
    fastas, output, ext = args.Fasta, args.Output, args.Extension
    with open(output, 'w') as out:
        for file in fastas:
            base = os.path.basename(file)
            base = base.strip(ext)
            with open(file) as f:
                for entry in SimpleFastaParser(f):
                    out.write(f'>{entry[0]}-{base}\n{entry[1]}\n')


def parse_args():
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Input fasta file.",
                        required=True, nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output faa file.",
                        required=True)
    parser.add_argument("-e", "--Extension",
                        required=False, default="\\.fasta")
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    main(args)
