"""
Program to compare two bin sets and write a new .fasta file of contigs
that were removed from the original set.
Requires:
<original_binset_dir>
<filtered_binset_dir>
<output_dir>
"""

from Bio import SeqIO
import os
import sys
import csv


""" First part is grabbing every .fasta file specified from both directories
and placing them into separate lists to be fed in the rest of the functions.
"""
original_bins = []
for file in os.listdir(sys.argv[1]):
	if file.endswith('.fasta'):
		file = os.path.join(sys.argv[1], file)
		original_bins.append(file)
filtered_bins = []
for file in os.listdir(sys.argv[2]):
	if file.endswith('fasta'):
		file = os.path.join(sys.argv[2], file)
		filtered_bins.append(file)


def get_fasta_dict(filename):
	''' Obtain a dictionary object for each .fasta file
	that contains key/header - value/sequence pair '''
	seq_dict = {rec.id : rec.seq for rec in SeqIO.parse(filename, "fasta")}
	return seq_dict

def read_multiple_fasta(files):
	""" Increase functionality of 'read_fasta' by allowing a list of multiple
	.fasta files to be read in, returning a master dictionary concat all dicts.
	Note: this will not work if multiple .fasta files contain same identifier
	"""
	master_dict = {}
	for file in files:
		print(file)
		fasta_dict = get_fasta_dict(file)
		print('Updating master dictionary...')
		master_dict.update(fasta_dict)
	print('Master dictionary updated!')
	return master_dict


def find_removed_contigs(bin1, bin2):
	''' Function to find contigs present in one bin set
	and not in another '''
	removed = {}
	b1 = read_multiple_fasta(bin1)
	b2 = read_multiple_fasta(bin2)
	# values = {k: bin2[k] for k in set(bin2) - set(bin1)}
	rem = set(b1) ^ set(b2)
	for val in rem:
		removed[val] = b1[val]
	return removed

def write_removed_contigs_file(bin1, bin2, filename):
	''' Function to write contigs not present in bin2 to
	a new .fasta file.
	Note: ">" identifiers are removed!'''
	removed_dict = find_removed_contigs(bin1, bin2)
	with open(filename, 'w') as fastafile:
		for key, value in removed_dict.items():
			fastafile.write(key)
			fastafile.write('\n')
			fastafile.write(str(value))
			fastafile.write('\n')

if __name__ == '__main__':
	write_removed_contigs_file(original_bins, filtered_bins, sys.argv[3])