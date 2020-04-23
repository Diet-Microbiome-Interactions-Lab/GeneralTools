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
from collections import Counter
import os
import sys
import csv

mydict = {'daners': 'string1.5',
		  'dillon': 'string2',
		  'jesse': 'string3.5',
		  'nicholas': 'string4'}

mydict2 = {'dane': 'string1',
		  'dillon': 'string2',
		  'jesse': 'string3',
		  'nick': 'string4'}

mydict3 = {'daned': 'string1.51',
		  'dillon': 'string2',
		  'jessead': 'string3',
		  'nick': 'string4'}

a = list(mydict.keys())
b = list(mydict2.keys())
c = []
c = c + a
cnter = Counter(c)
print(cnter)
for i in cnter.keys():
	print(i)

