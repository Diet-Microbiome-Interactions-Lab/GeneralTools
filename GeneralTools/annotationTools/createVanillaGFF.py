'''
Author: Dane
Date: 11Feb21
Purpose: Create a blank GFF file from a multi-fasta file
Example usage:
$ python createVanillaGFF.py -f infile.fasta -o outfile.gff
'''
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser


def main(args):
    '''
    Program designed to take in a BAM file and output a GFF file
    containing the information of contigs
    '''
    print('Running')
    file = args.File
    output = args.Output
    source = args.Source
    feature = args.Feature

    with open(output, 'w') as o:
        with open(file) as f:
            for values in SimpleFastaParser(f):
                seqname = values[0]
                end = str(len(values[1]))
                source = str(source)
                start = '0'
                score = '40'
                strand = "."
                frame = "."
                attribute = ' '
                writeline = '\t'.join([seqname, source, feature, start, end,
                                       score, strand, frame, attribute]) + '\n'
                o.write(writeline)
    return 0


def program_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--File",
                        help="Bam file to parse.",
                        required=True,)
    parser.add_argument("-o", "--Output",
                        help="Output GFF file name.",
                        required=True)
    parser.add_argument("-r", "--Feature", default='contig',
                        help="Feature type",
                        required=False)
    parser.add_argument("-s", "--Source", default='bowtie2',
                        help="Source of alignment",
                        required=False)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
