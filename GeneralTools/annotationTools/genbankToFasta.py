from Bio import SeqIO
import sys


def main(file, out):
    with open(file) as f:
        with open(out, 'w') as outfile:
            for record in SeqIO.parse(f, 'genbank'):
                outfile.write(
                    f'{record.id} {record.description}\n{record.seq}\n')
    return 0


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
