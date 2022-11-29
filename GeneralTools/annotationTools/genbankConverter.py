import argparse
from Bio import SeqIO


def main(args):
    file, out, format_ = args.Input, args.Output, args.Format
    with open(file) as f:
        with open(out, 'w') as outfile:
            for record in SeqIO.parse(f, 'genbank'):
                if format_ in ['fasta', 'fa', 'fna']:
                    outfile.write(
                        f'>{record.id}_{record.description}\n{record.seq}\n')
                elif format_ in ['faa', 'aa', 'amino_acid']:
                    for feature in record.features:
                        if feature.type == 'CDS':
                            try:
                                cds = feature.qualifiers['translation'][0]
                                seqname = feature.qualifiers['locus_tag'][0]
                                outfile.write(f'>{seqname}\n{cds}\n')
                            except KeyError:
                                pass
                                #print(f'No valid translation for {feature}')
    return 0


def parse_args():
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-i", "--Input",
                        help="Input genbank file.",
                        required=True)
    parser.add_argument("-f", "--Format",
                        help="Output format (fasta or faa)",
                        required=True)
    parser.add_argument("-o", "--Output",
                        help="Output faa file.",
                        required=True)
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    main(args)
