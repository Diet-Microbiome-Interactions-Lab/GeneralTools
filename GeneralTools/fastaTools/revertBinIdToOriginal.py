"""
Author: Dane
Purpose: Program designed to take in a binfile that has been
simplified via Anvi'os requirements and the original
assembly with orginal node names. It then outputs a new bin
identification file with original names.

Example usage:
$ python change_bin_nodenames.py -b <binfile.txt> \
-a <assembly.fasta> -o <new-binfile.txt>
"""
import argparse
from Bio import SeqIO

from .FastaClasses import BinID


def grab_string_match(string):
    match = string.split('_')[1]
    return str(int(match))


def convert_bin_id(BinID):
    contig_to_bin = {}
    bin_dic = BinID.bin_dic
    for contig in bin_dic:
        bin_ = bin_dic[contig]
        match = grab_string_match(contig)
        contig_to_bin[match] = bin_
    return contig_to_bin


def main(args):
    binfile, fasta, output = args.Bins, args.Fasta, args.Output
    header = args.Header
    binid = BinID(binfile, header=header)
    simple_contig_to_bin = convert_bin_id(binid)
    total_bin_ids = len(simple_contig_to_bin)

    total_bins_written = 0
    with open(output, 'w') as _out:
        with open(fasta) as _file:
            for record in SeqIO.parse(_file, "fasta"):
                match = grab_string_match(record.id)
                try:
                    writeline = f"{record.id}\t{simple_contig_to_bin[match]}\n"
                    _out.write(writeline)
                    total_bins_written += 1
                except KeyError:
                    pass

    assert total_bin_ids == total_bins_written, "Did not write all contigs!"
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--Bins", help="Simplified bin id file",
                        required=True)
    parser.add_argument("--Header", help="Simplified bin id file",
                        required=False, default=False)
    parser.add_argument("-f", "--Fasta", help="Assembly file",
                        required=True)
    parser.add_argument("-o", "--Output", help="Updated bin list name",
                        required=False)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
