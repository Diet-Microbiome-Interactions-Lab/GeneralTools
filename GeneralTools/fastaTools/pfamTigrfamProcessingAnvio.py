'''
Program is designed to take outputs from running HMMER querying TIGRFAMs
and PFAMs on an Anvio gene call file and adding functional information
to the files. The end product is a .txt file containing TIGRFAM and PFAM
information in an acceptable format for importing into an Anvio database.

Requirements: TIGRFAM.INFO files, which can be downloaded via:
$ wget ftp://ftp.jcvi.org/pub/data/TIGRFAMs/TIGRFAMs_15.0_INFO.tar.gz

Example usage:

$ python pfam_tigrfam_processing_anvio.py -t <tigrfam_genes.tsv> \
-p <pfam_genes.tsv> -d <path/to/TIGR.INFO/files> -o <output_file>

Real Example:
$ python pfam_tigrfam_processing_anvio.py -t genes.TIGR.tsv \
-p genes.Pfam.tsv -d TIGR/ -o tigr_pfam_results.txt

'''

import os
import argparse
import codecs

''' Initialize the arguments to be entered '''
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-t", "--TIGR", help="TIGR output file from running \
    HMMER. This should end in .tsv", required=True)
parser.add_argument("-p", "--PFAM", help="Pfam output file from running \
    HMMER. This should end in .tsv", required=True)
parser.add_argument("-d", "--Directory", help="Directory in which all of \
    the TIGR*****.INFO files are in", required=True)
parser.add_argument("-o", "--Output", help="File to save output to",
                    required=True)
argument = parser.parse_args()


def merge_tigr_pfam(tigrfile, pfile, direct, output):
    with open(output, 'w') as testfile:
        header = 'gene_callers_id\tsource\taccession\tfunction\te_value\n'
        testfile.write(header)
        with open(tigrfile) as f:
            # Skip comments
            line = f.readline()
            while line:
                if line.startswith('#'):
                    line = f.readline()
                else:
                    line = line.split()
                    gene_id = line[0]
                    access = line[3]
                    e_val = line[4]
                    for tfile in os.listdir(direct):
                        if tfile.startswith(access):
                            with codecs.open(os.path.join(direct, tfile), 'r',
                                             encoding='utf-8',
                                             errors='ignore') as tf:
                                for i in range(3):
                                    de = tf.readline().strip().strip('DE ')
                                for i in range(9):
                                    cc = tf.readline().strip().strip('CC')
                                function = de + ': ' + cc
                    newline = '\t'.join([gene_id, 'TIGRFAM',
                                         access, function, e_val])
                    testfile.write(newline + '\n')
                    line = f.readline()
        # Now append information for Pfam to the end
        with open(pfile) as pf:
            # Skip comments
            line = pf.readline()
            while line:
                if line.startswith('#'):
                    line = pf.readline()
                else:
                    line = line.split()
                    gene_id = line[0]
                    access = line[3]
                    e_val = line[4]
                    function = line[2]
                    newline = '\t'.join([gene_id, 'Pfam',
                                         access, function, e_val])
                    testfile.write(newline + '\n')
                    line = pf.readline()


if __name__ == "__main__":
    merge_tigr_pfam(argument.TIGR, argument.PFAM,
                    argument.Directory, argument.Output)
