import sys

from Bio import SeqIO


def main(genbank, output):
    with open(genbank) as input_handle, open(output, "w") as output_handle:
        sequences = SeqIO.parse(input_handle, "genbank")
        count = SeqIO.write(sequences, output_handle, "fasta")
    print("Converted %i records" % count)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
