'''
Author: Dane
Date: 01Dec20
Purpose: Given an multi-fasta and a bin identification file, filter
the multi-fasta so only contain the sequences in the BID file.

Example usage:
$ python filterAssembly.py <assembly.fasta> <bid.txt> <output.txt>
'''


'''
Notes:
Find a way to auto initialize a a list of size (max(contignumber))
'''

import sys
from Bio.SeqIO.FastaIO import SimpleFastaParser


def readBinID(binid):
    contiglist = [0] * 329249
    with open(binid) as b:
        line = b.readline().strip()
        while line:
            contig = int(line.split('\t')[1].split('_')[1])
            contiglist[contig] = 1
            line = b.readline().strip()
    return contiglist


def filterFasta(assembly, binid, output):
    """
    Open up a .fasta file and return a dictionary containing the header
    as the key and length as the value
    """

    contigList = readBinID(binid)

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
    from datetime import datetime
    start = datetime.now()
    filterFasta(sys.argv[1], sys.argv[2], sys.argv[3])
    with open('log.txt', 'a') as log:
        log.write(f"{datetime.now() - start}\n")
