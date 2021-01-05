'''
Author: Dane Deemer
Date: NA
Purpose: Program design to filter a .BAM file based on alignments
matching a list of provided reference identifiers
Use example: map all reads to an assembly, and then once
you bin the contigs from each assembly, you can go back and
look at how each binset was aligned against the raw reads.

Example usage:
$ python filterBamByReference.py -c <contiglist.txt> -i <input.bam> \
-o <output.out>
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


def filterHeader(bam, contigList):
    '''
    Filter the BAM header to append to the output from filterBam
    '''
    header = {}
    header['SQ'] = []
    head = str(bam.header).split('\n')
    for value in head:
        if value.startswith('@SQ'):
            index = int(value.split('\t')[1].split('_')[1])
            if contigList[index] == 1:
                node = value.split('\t')[1].split(':')[1]
                ln = int(value.split('\t')[2].split(':')[1])
                cur_dic = {'LN': ln, 'SN': node}
                header['SQ'].append(cur_dic)
        elif value.startswith('@HD'):
            tag = value.split('\t')[0].strip('@')
            version = value.split('\t')[1].split(':')[1]
            header[tag] = {'VN': version}
        else:
            pass
    return header


def filterBam(inBam, outBam, contigs, keep_bin=False):
    '''
    Filter a bam file based on a bin identification file.
    '''
    contigList = readBinID(contigs, keep_bin)

    bam = pysam.AlignmentFile(inBam)
    header = filterHeader(bam, contigList)
    obam = pysam.AlignmentFile(outBam, 'wb', header=header)

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
