
'''
Author: Dane
Date: 01Dec20
Purpose: 2

Example usage:
$ python filterAssembly.py <assembly.fasta> <bid.txt> <output.txt>

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
    '''
    Open up a binID file (binid\tcontig\n) and create a list
    of all nodes that exist in it. If the file is reverse, e.g.,
    (contig\tbinid\n), then specify --field 0
    '''
    contiglist = [0] * ncontigs
    with open(binid) as b:
        line = b.readline().strip()
        while line:
            contig = int(line.split('\t')[int(field)].split('_')[1])
            contiglist[contig] = 1
            line = b.readline().strip()
    return contiglist


def filterFasta(assemblies, binid, output, ncontigs, field, reverse):
    """
    Parse each fasta defline and filter if in binID or write non-binners
    """

    contigList = readBinID(binid, ncontigs, field)

    with open(output, 'w') as o:
        for assembly in assemblies:
            with open(assembly) as f:
                for values in SimpleFastaParser(f):
                    defline = values[0]
                    index = int(values[0].split('_')[1])
                    if (reverse and contigList[index] == 0):
                        o.write('>' + defline + '\n')
                        o.write(values[1] + '\n')
                    elif (not reverse and contigList[index] == 1):
                        o.write('>' + defline + '\n')
                        o.write(values[1] + '\n')
                    else:
                        pass
    return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-a", "--Assembly",
                        help="Assembly(s) to filter", required=True,
                        nargs="*")
    parser.add_argument("-o", "--Output",
                        help="Output assembly to write", required=True)
    parser.add_argument("-i", "--Id_File",
                        help="File containing list of entries to filter",
                        required=True)
    parser.add_argument("-r", "--Reverse",
                        help="Get entries NOT in the binid file",
                        required=False, action='store_true',
                        default=False)
    parser.add_argument("-f", "--Field",
                        help="Field where contigs list is",
                        required=False, default=1)
    argument = parser.parse_args()
    # Count how many entries are in the fasta file
    with open(argument.Assembly[0], "r", encoding="utf-8", errors='ignore') as f:
        ncontigs = sum(bl.count(">") for bl in blocks(f)) + 1

    filterFasta(argument.Assembly, argument.Id_File, argument.Output,
                ncontigs, argument.Field, argument.Reverse)
