'''
Author: Dane
Date: 01Dec20
Program design to filter a .BAM file based on alignments
matching a list of provided reference identifiers
Use example: map all reads to an assembly, and then once
you bin the contigs from each assembly, you can go back and
look at how each binset was aligned against the raw reads
'''

import sys
import argparse
import pysam


def readBinID(binid, keep_bin=False):
    contigList = [0] * 400000
    with open(binid) as b:
        line = b.readline().strip()
        while line:
            if keep_bin:
                bin_name = line.split('\t')[0]
                if bin_name in keep_bin:
                    contig = int(line.split('\t')[1].split('_')[1])
                    contigList[contig] = 1
            else:
                contig = int(line.split('\t')[1].split('_')[1])
                contigList[contig] = 1
            line = b.readline().strip()
    return contigList


def filterBam(inBam, outBam, contigs, keep_bin=False):
    contigList = readBinID(contigs, keep_bin)
    bam = pysam.AlignmentFile(inBam)
    obam = pysam.AlignmentFile(outBam, 'wb', template=bam)

    for b in bam.fetch(until_eof=True):
        try:
            index = int(b.reference_name.split('_')[1])
        except AttributeError:
            pass
        if contigList[index] == 1:
            obam.write(b)

    bam.close()
    obam.close()
    return 0


if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-i", "--Input",
                        help="Input .BAM file to filter.",
                        default=sys.stdin, required=False)
    parser.add_argument("-o", "--Output",
                        help="Output .BAM file to write to.",
                        required=True)
    parser.add_argument("-c", "--Contigs", help="File containing reference \
    identifiers and the associated bin (each on its own line & tab-separated)",
                        required=True)
    parser.add_argument("-k", "--Keep",
                        help="Keep only contigs in the specified bins.",
                        nargs="*", required=False, default=False)
    argument = parser.parse_args()
    filterBam(argument.Input, argument.Output,
              argument.Contigs, keep_bin=argument.Keep)
    msg = f"{datetime.now() - start}\n"
    with open('log.txt', 'a') as log:
        log.write(msg)
