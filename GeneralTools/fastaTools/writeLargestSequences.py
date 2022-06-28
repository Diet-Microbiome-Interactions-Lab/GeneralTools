'''
Author: Dane Deemer
Program that takes a numeric value n and the name of a fasta
file and returns the top n largest entries (key=len(sequence))
$ python -i <myfile.fasta> -n <seqlength_to_filter_(int) > -o <output.fasta>
'''
import argparse
from Bio import SeqIO


def get_longest_seqs(file, n):
    fasta_dic = {}
    for record in SeqIO.parse(file, "fasta"):
        fasta_dic[record.id] = record.seq
    top_n = sorted(fasta_dic, key=lambda k: len(
        fasta_dic[k]), reverse=True)[0:n]

    return {entry: fasta_dic[entry] for entry in top_n}


def write_largest_seqs(file, n, output):
    longest_entries = get_longest_seqs(file, n)
    with open(output, 'w') as _out:
        for entry in longest_entries:
            _out.write(f'>{entry}\n{longest_entries[entry]}\n')
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta", help="Input fasta to be filtered",
                        required=True)
    parser.add_argument("-n", "--Length", help="Length to filter",
                        type=int, required=True)
    parser.add_argument("-o", "--Output", help="Output file name",
                        required=True)
    args = parser.parse_args()
    write_largest_seqs(args.Fasta, args.Length, args.Output)
