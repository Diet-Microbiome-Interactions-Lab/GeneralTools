from Bio.SeqIO.FastaIO import SimpleFastaParser


def processDefline(defline, split, val):
    tmp = defline.split(split)[val]
    return f'{tmp}.fasta'


def main(fasta, delim, block):
    with open(fasta) as f:
        for values in SimpleFastaParser(f):
            defline = values[0]
            seq = values[1]
            output = processDefline(defline, delim, block)
            with open(output, 'a') as out:
                out.write(f'>{defline}\n{seq}\n')
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Assembly to filter", required=True)
    parser.add_argument("-d", "--Delimiter",
                        help="Delimiter to split defline", required=True)
    parser.add_argument("-b", "--Block",
                        help="Which numerical block is the filename?",
                        required=True, type=int)
    arg = parser.parse_args()
    main(arg.Fasta, arg.Delimiter, arg.Block)
