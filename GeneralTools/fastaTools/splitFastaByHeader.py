from Bio import SeqIO


def processDefline(defline, split, val):
    tmp = defline.split(split)[val]
    return f'{tmp}.fasta'


def main(fasta, delim, block):
    for record in SeqIO.parse(fasta, "fasta"):
        output = processDefline(record.id, delim, record.seq)
        with open(output, 'a') as _out:
            _out.write(f'>{record.id}\n{record.seq}\n')
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Fasta file to filter", required=True)
    parser.add_argument("-d", "--Delimiter",
                        help="Delimiter to split defline", required=True)
    parser.add_argument("-b", "--Block",
                        help="Which numerical block is the filename?",
                        required=True, type=int)
    arg = parser.parse_args()
    main(arg.Fasta, arg.Delimiter, arg.Block)
