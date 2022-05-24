from Bio.SeqIO.FastaIO import SimpleFastaParser
import argparse
import os


def main(args):
    files, output = args.Fastas, args.Output
    print(f'Writing to {output}...\n')
    with open(output, 'w') as out:
        for file in files:
            print(file)
            base = os.path.basename(file)
            base = file.replace('.fasta', '')
            print(f'Working on {base}')
            with open(file, encoding='latin-1') as f:
                line = f.readline()
                while line:
                    if line.startswith('>'):
                        line = line.strip()
                        line = f'{line}-{base}\n'
                    out.write(line)
                    line = f.readline()


def parse_args():
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fastas",
                        help="Input fasta file.",
                        required=True, nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output faa file.",
                        required=True)
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    main(args)
