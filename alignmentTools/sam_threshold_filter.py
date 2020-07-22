''' Program to parse a .SAM file and filter it for a user-defined
percent identity '''

import sys
import argparse
import re

''' Initialize the arguments to be entered '''
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-i", "--Input", help="Input .SAM file to filter",
                    default=sys.stdin)
parser.add_argument("-o", "--Output", help="Filtered output filename to read \
    to", default=sys.stdout)
parser.add_argument("-s", "--Readsize", help="Readsize of .fastq pairs")
parser.add_argument("-t", "--Threshold", help="Percent idenity threshold to \
    filter")
parser.add_argument("-md", "--mdColumn", help="Zero-based column number that \
    the MD score is in. Default value correlates to Bowtie2 field", default=17)
argument = parser.parse_args()


if argument.Input == sys.stdin:
    def filter_same_percent_identity(
            infile, outfile, readsize, threshold, md=17):
        ''' Function that filters a .SAM file based on a defined threshold '''
        low_identity = 0
        header_flag = False
        for line in argument.Input:
            if line.startswith('@'):
                sys.stdout.write(line)
                header_flag = True
            else:
                if header_flag is False:
                    raise Exception('Error - No header information \
provided. Please remember to use the -h option when using samtools view!')
                rline = line.split('\t')
                entry_matches = 0
                if len(rline) > 13:
                    matches = (
                        [int(i) for i in
                         re.findall(r'\d+', rline[17])]
                    )
                    for m in matches:
                        entry_matches = entry_matches + m
                    if (entry_matches / int(readsize)) > float(threshold):
                        sys.stdout.write(line)
                    else:
                        low_identity += 1
        return low_identity
else:
    def filter_same_percent_identity(
            infile, outfile, readsize, threshold, md=17):
        ''' Function that filters a .SAM file based on a defined threshold '''
        low_identity = 0
        header_flag = False
        with open(outfile, 'w') as outf:
            with open(infile) as inf:
                line = inf.readline()
                while line:
                    if line.startswith('@'):
                        outf.write(line)
                        header_flag = True
                    else:
                        if header_flag is False:
                            raise Exception(
                                'No header information provided please use \
option -h when using samtools view.')
                        else:
                            rline = line.split('\t')
                            entry_matches = 0
                            if len(rline) > 17:
                                matches = (
                                    [int(i) for i in
                                     re.findall(r'\d+', rline[17])]
                                )
                                for m in matches:
                                    entry_matches = entry_matches + m
                                if ((entry_matches / int(readsize)) >
                                     float(threshold)):
                                    outf.write(line)
                                else:
                                    low_identity += 1
                    line = inf.readline()
        return low_identity


if __name__ == '__main__':
    if argument.mdColumn:
        filter_same_percent_identity(argument.Input, argument.Output,
                                     argument.Readsize, argument.Threshold,
                                     md=argument.mdColumn)
    else:
        filter_same_percent_identity(argument.Input, argument.Output,
                                     argument.Readsize, argument.Threshold)
