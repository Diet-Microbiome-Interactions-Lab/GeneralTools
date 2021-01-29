'''
Author: Dane
This script is designed to take in a BinID file that has the output
from writeFlaggedContigsNewBinID.py (such that it has bin labels for
Removed) and a directory containing the bins for a sample. The output
consists of multiple new .fasta files labeled:
<oldFastaName>.TaxonRemoved.fasta

Example usage:
$ python writeTaxonRemovedFastas.py
'''
import os
from Bio import SeqIO
import argparse


def get_removed_contig_names(binidfile):
    '''
    Open up binid file and read into a dictionary in the form:
    dict[Node] = BinX
    '''
    mylist = []
    with open(binidfile) as f:
        line = f.readline()
        while line:
            node = line.split('\t')[0].strip('>')
            if not node.startswith('NODE'):
                raise Exception('Nodes should start with: NODE')
            mylist.append(node)
            line = f.readline()
    return mylist


def write_new_fastas(binid, directory):
    '''
    Function that goes through a specified directory and reads
    every .fasta file, checking whether the defline is contained
    in the bin identification file. It then writes only files with
    a bin number and passes nodes labeled as Removed. Final output
    contains subsetted .fasta files
    '''
    idlist = get_removed_contig_names(binid)
    for file in os.listdir(directory):
        if file.endswith('.fasta'):
            file = os.path.join(directory, file)
            for record in SeqIO.parse(file, 'fasta'):
                # Create variable that'll match an entry in idlist
                match = record.id.strip('>')
                if match in idlist:
                    if idlist[match] == 'NoBin':
                        raise Exception('Should NOT be writing this defline!')
                    else:
                        writefile = f"{str(file).split('/')[-1]}" \
                                    f".TaxonRemoved.fasta"
                        with open(writefile, 'a') as o:
                            o.write(f"{record.id}\n{record.seq}\n")
                else:
                    pass
    return 0


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--BinID",
                        help="Bin identification file for the sample",
                        required=True)
    parser.add_argument("-d", "--Directory",
                        help="Directory containing original bins",
                        required=True)
    argument = parser.parse_args()
    write_new_fastas(argument.BinID, argument.Directory)
