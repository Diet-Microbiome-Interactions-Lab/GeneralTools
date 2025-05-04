"""
Author: Dane Deemer
Obtain tetranucleotide frequency for a
given string within a nucleotide sequnce

Example usage:
$ python tetranucleotideFreq.py 'MYSTRING'
"""
import argparse
# A comment to test the import

def main(args):
    sequence = args.Sequence
    nuc = ["A", "T", "G", "C"]
    mer_list = []
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    mer = nuc[i] + nuc[j] + nuc[k] + nuc[l]
                    mer_list.append(mer)
    sequence = sequence.upper()
    length = len(sequence)
    freq_hash = {}
    for i in range(0, length - 3):
        mer = sequence[i:i + 4]
        if mer not in freq_hash:
            freq_hash[mer] = 0
        freq_hash[mer] = freq_hash[mer] + 1
    return freq_hash


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-s", "--Sequence",
                        help="Sequence to extract TNF",
                        required=True)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
