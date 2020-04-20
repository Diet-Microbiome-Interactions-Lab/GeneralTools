import os
import matplotlib.pyplot as plt

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
				header = line.strip()
				line = f.readline()
				nucleotides = ''
				file_id = ''
			else:
				nucleotides = nucleotides + line.strip()
				line = f.readline()
				file_id = file.strip()
				fasta_dict[header] = [file_id,
									  len(nucleotides),
									  gc_cont(nucleotides)]
	return fasta_dict
