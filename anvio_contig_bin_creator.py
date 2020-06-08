'''
Program designed to take a directory containing all bin files and output a tab-delimited
file containing contig names in the first column and their associated bin number in the
second column.
The output is in a format that can be directly imported into an Anvio database using:
$ anvi-import-collection <output-from-this-program.txt> -c $CONTIG_DB -p $PROFILE \
--contig-mode --collection-name "Whatever name you choose!"

Example usage:
$ python anvio_contig_bin_creator.py <bin-file-format> <output-file-name>
$ python anvio_contig_bin_creator.py fasta contigs-to-be-imported.txt
'''

''' Initialize the arguments to be entered '''
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-d", "--Directory", help="Directory containing files",
                    required=True)
parser.add_argument("-o", "--Output", help="Output file name",
                    required=True)
argument = parser.parse_args()



import os
import sys

files = []
mydir = os.getcwd()
for f in os.listdir(mydir):
    if f.endswith(argument.Directory):
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
    save_fa_dict(files, argument.Output)
