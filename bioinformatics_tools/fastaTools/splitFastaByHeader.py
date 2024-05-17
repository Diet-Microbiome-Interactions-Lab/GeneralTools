import argparse
from Bio import SeqIO


def processDefline(defline, split, block):
    tmp = defline.split(split)[block]
    return f'{tmp}.fasta'


def main(args):
    fasta, delim, block = args.Fasta, args.Delimiter, args.Block
    for record in SeqIO.parse(fasta, "fasta"):
        output = processDefline(record.id, delim, block)
        with open(output, 'a') as _out:
            _out.write(f'>{record.id}\n{record.seq}\n')
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Fasta file to filter", required=True)
    parser.add_argument("-d", "--Delimiter",
                        help="Delimiter to split defline", required=False,
                        default='.')
    parser.add_argument("-b", "--Block",
                        help="Which numerical block is the filename?",
                        required=False, type=int, default=0)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
