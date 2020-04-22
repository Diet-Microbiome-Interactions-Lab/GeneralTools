"""
TESTFILE USED FOR TESTING!!!
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

mydict = {'dane': [1, 2, 3, 4],
		  'dillon': [5,6,7,8],
		  'jesse': [55, 66, 77, 88],
		  'nick': [11,22,33,44]}

l1 = mydict.keys()
print(l1)
l2 = []
for key, val in mydict.items():
	print(key)
	print(val[0])
	line = key + '\t' + str(val[0]) + '\t' + str(val[1])
	print(line)