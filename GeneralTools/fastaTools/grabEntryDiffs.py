"""
Program to compare two bin sets and write a new .fasta file of contigs
that were removed from the original set.
Requires:
<original_binset_dir>
<filtered_binset_dir>
<output_dir>
$ python grab_removed_contigs.py <original_binset> <filtered_binset> \
<output_file>
"""
import argparse
from Bio import SeqIO


def main(args):
    '''
    Compare 2 fasta files for differences
    '''
    # Step 1: Check fasta/bin file(s) and remove contigs from all_contigs
    fasta1, fasta2, output = args.One, args.Two, args.Output
    with open(output, 'w') as out:
        one = {rec.id: rec.seq for rec in SeqIO.parse(fasta1, "fasta")}
        two = {rec.id: rec.seq for rec in SeqIO.parse(fasta2, "fasta")}
        diff = set(one) ^ set(two)
        out.write(f"Differences between {fasta1} and {fasta2}:\n")
        diffs = [f"{val}\n" for val in diff]
        for d in diffs:
            out.write(d)


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-1", "--One",
                        help="File 1",
                        required=True)
    parser.add_argument("-2", "--Two",
                        help="File 2",
                        required=True)
    parser.add_argument("-o", "--Output",
                        help="Output",
                        required=True)
    return parser


if __name__ == '__main__':
    """ Arguments """
    parser = parse_args()
    args = parser.parse_args()
    main(args)
