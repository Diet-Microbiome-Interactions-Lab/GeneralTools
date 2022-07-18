'''
Author: Dane
Date: 01Dec20
Purpose: Filter a multi-fasta file by a bin identification file.

Example usage:
$ python filterAssembly.py <assembly.fasta> <bid.txt> <output.txt>

'''
from .FastaClasses import BinID
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser


# First, count how many contigs are in the assembly to know how big
# to initialize the contig index.
def blocks(file, size=65536):
    while True:
        b = file.read(size)
        if not b:
            break
        yield b


# def readBinID(binid, ncontigs, field):
#     '''
#     Open up a binID file (binid\tcontig\n) and create a list
#     of all nodes that exist in it. If the file is reverse, e.g.,
#     (contig\tbinid\n), then specify --field 0
#     '''
#     contiglist = [0] * ncontigs
#     with open(binid) as b:
#         line = b.readline().strip()
#         while line:
#             contig = int(line.split('\t')[int(field)].split('_')[1])
#             contiglist[contig] = 1
#             line = b.readline().strip()
#     return contiglist


def main(args):
    """
    Parse each fasta defline and filter if in binID or write non-binners
    """
    assemblies, binid, output = args.Assembly, args.Bins, args.Output
    field, reverse = args.Field, args.Reverse
    with open(assemblies[0], "r", encoding="utf-8", errors='ignore') as f:
        ncontigs = sum(bl.count(">") for bl in blocks(f)) + 1

    contig_numbers = BinID(binid).contig_number()

    with open(output, 'w') as out:
        for assembly in assemblies:
            with open(assembly) as f:
                for values in SimpleFastaParser(f):
                    defline = values[0]
                    index = int(values[0].split('_')[1])
                    if index in contig_numbers:
                        out.write('>' + defline + '\n')
                        out.write(values[1] + '\n')
                    elif reverse:
                        if index not in contig_numbers:
                            out.write('>' + defline + '\n')
                            out.write(values[1] + '\n')
                    else:
                        pass
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-a", "--Assembly",
                        help="Assembly(s) to filter", required=True,
                        nargs="*")
    parser.add_argument("-o", "--Output",
                        help="Output assembly to write", required=True)
    parser.add_argument("-b", "--Bins",
                        help="File containing list of entries to filter",
                        required=True)
    parser.add_argument("-r", "--Reverse",
                        help="Get entries NOT in the binid file",
                        required=False, action='store_true',
                        default=False)
    parser.add_argument("-f", "--Field",
                        help="Field where contigs list is",
                        required=False, default=1)
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    main(args)
