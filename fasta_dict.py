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

# os.chdir('/Users/Dane/Documents/Lindemann/WhiteSAXApr20/\
# MaxBin2/MB_W1_BWA')

files = []
for f in os.listdir():
	if f.endswith(sys.argv[1]):
		files.append(f)


def gc_cont(string):
	string = string.upper()
	g = string.count('G')
	c = string.count('C')
	return (g + g)/len(string)


def read_fasta(file):
	fasta_dict = {}
	with open(file) as f:
		line = f.readline()
		while line:
			if line.startswith('>'):
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
									  # tetranucleotide_freq(nucleotides)]
									  ]
	return fasta_dict

def read_multiple_fasta(files):
	master_dict = {}
	for file in files:
		print(file)
		fasta_dict = read_fasta(file)
		print('Updating master dictionary...')
		master_dict.update(fasta_dict)
	print('Master dictionary updated!')
	return master_dict


def save_fa_dict(files, savename):
	dictionary = read_multiple_fasta(files)
	print('Reading in dictionary and writing to .csv...')
	with open(savename, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(dictionary) # First row (keys of dict)
		for values in zip(*dictionary.values()):
			writer.writerow(values)


if __name__ == "__main__":
	save_fa_dict(files, sys.argv[2])
