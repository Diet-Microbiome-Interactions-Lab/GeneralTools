'''
Program design to filter a .BAM file based on alignments
matching a list of provided reference identifiers
Use example: map all reads to an assembly, and then once
you bin the contigs from each assembly, you can go back and
look at how each binset was aligned against the raw reads
'''

import sys
import argparse

parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-i", "--Input", help="Input .BAM file to filter",
                    default=sys.stdin, required=False)
parser.add_argument("-o", "--Output", help="Filtered output filename to read \
                    to", required=True)
parser.add_argument("-c", "--Contigs", help="File containing reference \
identifiers and the associated bin (each on its own line & tab-separated)",
                    required=True)
argument = parser.parse_args()


def get_contigs(contigfile):
    bin_dictionary = {}
    with open(contigfile) as contigs:
        line = contigs.readline()  # First line is header; skip
        line = contigs.readline()
        while line:
            c_name = line.split('\t')[1]
            bin_name = line.split('\t')[0]
            if bin_name in bin_dictionary:
                bin_dictionary[bin_name].append(c_name)
            else:
                bin_dictionary[bin_name] = [c_name]
    return bin_dictionary


def filter_bam(contigfile, input, output):
    bin_dictionary = get_contigs(contigfile)
    header_flag = False
    # Read from the stdin
    with open(output, 'w') as out:
        for line in argument.Input:
            print(line)
            if line.startswith('@'):
                print('Yes')
                out.write(line)
                header_flag = True
            else:
                if header_flag is False:
                    raise Exception('Error - No header information \
    provided. Please remember to use the -h option when using samtools.')
                else:
                    pass
                bam_reference = line.split('\t')[2]
                if bam_reference in bin_dictionary:
                    out.write(line)
                else:
                    pass


if __name__ == '__main__':
    filter_bam(argument.Contigs, argument.Input, argument.Output)
