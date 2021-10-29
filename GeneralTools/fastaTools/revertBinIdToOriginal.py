"""
Author: Dane
Date: NA
Purpose: Program designed to take in a binfile that has been
simplified via Anvi'os requirements and the original
assembly with orginal node names. It then outputs a new bin
identification file with original names.

Example usage:
$ python change_bin_nodenames.py -b <binfile.txt> \
-a <assembly.fasta> -o <new-binfile.txt>
"""
import argparse

from Bio.SeqIO.FastaIO import SimpleFastaParser


def grabStringMatch(string):
    match = string.split('_')[1]
    return str(int(match))


def readBinID(binfile, header=False):
    contig_to_bin = {}
    with open(binfile) as bfile:
        line = bfile.readline()
        if header:
            line = bfile.readline().strip()
        while line:
            contig, bin_ = line.split('\t')
            match = grabStringMatch(contig)
            contig_to_bin[match] = bin_
            line = bfile.readline().strip()
    return contig_to_bin


def main(args):
    binfile, assembly, output = args.BinID, args.Assembly, args.Output
    simple_contig_to_bin = readBinID(binfile)
    total_bin_ids = len(simple_contig_to_bin)

    total_bins_written = 0
    with open(output, 'w') as out:
        with open(assembly) as a:
            for values in SimpleFastaParser(a):
                defline = values[0]
                match = grabStringMatch(defline)
                try:
                    writeline = f"{defline}\t{simple_contig_to_bin[match]}\n"
                    out.write(writeline)
                    total_bins_written += 1
                except KeyError:
                    pass

    assert total_bin_ids == total_bins_written, "Did not write all contigs!"
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--BinID", help="Simplified bin id file",
                        required=True)
    parser.add_argument("-a", "--Assembly", help="Assembly file",
                        required=True)
    parser.add_argument("-o", "--Output", help="Updated bin list name",
                        required=False)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
