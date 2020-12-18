
'''
Author: Dane
Date: 01Dec20
Purpose: Given an multi-fasta and a bin identification file, filter
the multi-fasta so only contain the sequences in the BID file.

Example usage:
$ python filterAssembly.py <assembly.fasta> <bid.txt> <output.txt>

Notes:
In the future, add functionality to specify the delimiter for the
bin identification file.
'''
from Bio.SeqIO.FastaIO import SimpleFastaParser


# First, count how many contigs are in the assembly to know how big
# to initialize the contig index.
def blocks(file, size=65536):
    while True:
        b = file.read(size)
        if not b:
            break
        yield b


def readBinID(binid, ncontigs, field):
    contiglist = [0] * ncontigs
    with open(binid) as b:
        line = b.readline().strip()
        while line:
            contig = int(line.split('\t')[int(field)].split('_')[1])
            contiglist[contig] = 1
            line = b.readline().strip()
    return contiglist


def filterFasta(assembly, binid, output, ncontigs, field):
    """
    Open up a .fasta file and return a dictionary containing the header
    as the key and length as the value
    """

    contigList = readBinID(binid, ncontigs, field)

    with open(output, 'w') as o:
        with open(assembly) as f:
            for values in SimpleFastaParser(f):
                defline = values[0]
                index = int(values[0].split('_')[1])
                if contigList[index] == 1:
                    o.write('>' + defline + '\n')
                    o.write(values[1] + '\n')
                else:
                    pass
    return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-a", "--Assembly",
                        help="Assembly to filter", required=True)
    parser.add_argument("-o", "--Output",
                        help="Output assembly to write", required=True)
    parser.add_argument("-i", "--Id_File",
                        help="File containing list of entries to filter",
                        required=True)
    parser.add_argument("-f", "--Field",
                        help="Field where contigs list is",
                        required=False, default=1)
    argument = parser.parse_args()
    # Count how many entries are in the fasta file
    with open(argument.Assembly, "r", encoding="utf-8", errors='ignore') as f:
        ncontigs = sum(bl.count(">") for bl in blocks(f)) + 1

    filterFasta(argument.Assembly, argument.Id_File, argument.Output,
                ncontigs, argument.Field)
