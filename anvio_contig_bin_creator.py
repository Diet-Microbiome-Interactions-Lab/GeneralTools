

import os
import sys

files = []
mydir = os.getcwd()
for f in os.listdir(mydir):
    if f.endswith(sys.argv[1]):
        files.append(f)


def read_fasta(file):
    """ Open up a .fasta file and return a dictionary containing the header
    as the key and [filename, length, & gc_cont] as values """
    fasta_dict = {}
    with open(file) as f:
        line = f.readline()
        while line:
            if line.startswith('>') or line.startswith('NODE'):
                header = line.strip()
                line = f.readline()
                file_id = ''
            else:
                line = f.readline()
                file_id = str(file.strip())
                fasta_dict[header] = 'Bin_' + file_id.split('.')[1]
    return fasta_dict

def read_multiple_fasta(files):
    """ Increase functionality of 'read_fasta' by allowing a list of multiple
    .fasta files to be read in, returning a master dictionary.
    Note: this will not work if multiple .fasta files contain same identifier
    """
    master_dict = {}
    for file in files:
        print(file)
        fasta_dict = read_fasta(file)
        print('Updating master dictionary...')
        master_dict.update(fasta_dict)
    print('Master dictionary updated!')
    return master_dict


def save_fa_dict(files, savename):
    """ A function to write .csv values of .fasta output """
    dictionary = read_multiple_fasta(files)
    header = 'Contig\tBin\n'
    print('Reading in dictionary and writing to .txt...')
    with open(savename, 'w') as csvfile:
        csvfile.write(header)  # First row (keys of dict)
        for key, val in dictionary.items():
            line = (key + '\t' + str(val) + '\n')
            csvfile.write(line)


if __name__ == "__main__":
    save_fa_dict(files, sys.argv[2])