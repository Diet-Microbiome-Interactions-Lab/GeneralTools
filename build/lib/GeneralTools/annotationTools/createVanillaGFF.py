'''
Create a blank GFF file from an assembly .FASTA file
Example usage:
$python createVanillaGFF.py -f infile.fasta -o outfile.gff
'''


import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser

# Arguments v
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-f", "--File",
                    help="Bam file to parse.",
                    required=True,)
parser.add_argument("-o", "--Output",
                    required=True,
                    help="Output GFF file name.")
arg = parser.parse_args()
# Arguments ^


def createGFF(file, output):
    '''
    Program designed to take in a BAM file and output a GFF file
    containing the information of contigs
    '''
    with open(output, 'w') as o:
        with open(file) as f:
            for values in SimpleFastaParser(f):
                seqname = values[0]
                end = seqname.split('_')[3]
                source = "bowtie2"
                feature = "contig"
                start = '0'
                score = '40'
                strand = "."
                frame = "."
                attribute = ' '
                writeline = '\t'.join([seqname, source, feature, start, end,
                                       score, strand, frame, attribute]) + '\n'
                o.write(writeline)
    return 0


if __name__ == "__main__":
    createGFF(arg.File, arg.Output)
