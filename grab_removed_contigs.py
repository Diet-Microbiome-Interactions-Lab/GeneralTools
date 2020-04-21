"""
Program to compare two bin sets and
understand which contigs were removed
from the original set.
Requires:
<original_binset>
<filtered_binset>
<output_dir>
"""

import os
import sys
print(os.getcwd())

def read_fasta(fasta_file):
	fa_dict = {}
	value = ''
	with open(fasta_file) as fa:
		line = fa.readline()
		while line:
			if line.startswith('>'):
				key = line.strip()
				line = fa.readline()
			else:
				value = value + line.strip()
				fa_dict[key] = value
				line = fa.readline()
	return fa_dict

def find_removed_contigs(bin1, bin2):
	b1 = read_fasta(bin1)
	b2 = read_fasta(bin2)
	# values = {k: bin2[k] for k in set(bin2) - set(bin1)}
	return b1, b2

print(find_removed_contigs('sample.txt', 'sample2.txt'))