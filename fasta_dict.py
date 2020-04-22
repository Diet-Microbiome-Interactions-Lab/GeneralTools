"""
Function that requires: 1+ .FASTA files and
writes a csv files containing: .fasta description,
what file it came from (bin), length, and GC content

Example use:
$ python fasta_dict.py .fasta <savename.csv>
"""
import os
import csv
import sys

files = []
mydir = os.getcwd()
for f in os.listdir(mydir):
	if f.endswith(sys.argv[1]):
		files.append(f)


def gc_cont(string):
	""" Function to be used inside of 'read_fasta' in order to obtain
	gc_content of a string """
	string = string.upper()
	g = string.count('G')
	c = string.count('C')
	leng = float(len(string))
	gc = float((g + c))
<output_dir>
	return round(gc/leng, 3)


def read_fasta(file):
	""" Open up a .fasta file and return a dictionary containing the header
	as the key and [filename, length, & gc_cont] as values """
	fasta_dict = {}
	with open(file) as f:
		line = f.readline()
		while line:
			if line.startswith('>') or line.startswith('NODE'):
				header = line.strip('>')
				header = header.strip()
				line = f.readline()
				nucleotides = ''
				file_id = ''
			else:
				nucleotides = nucleotides + line.strip()
				line = f.readline()
				file_id = file.strip()
				fasta_dict[header] = [file_id,
									  len(nucleotides),
									  gc_cont(nucleotides)
									  # This is where more information
									  # can be added.
									  ]
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
	header = 'Contig\tBin\tLength\tGC.Content\n'
	print('Reading in dictionary and writing to .csv...')
	with open(savename, 'w') as csvfile:
		csvfile.write(header)  # First row (keys of dict)
		for key, val in dictionary.items():
			line = (key + '\t' + str(val[0]) + 
						  '\t' + str(val[1]) +
						  '\t' + str(val[2]) + '\n')
			csvfile.write(line)


if __name__ == "__main__":
	save_fa_dict(files, sys.argv[2])
