'''
Author: Dane Deemer
Program designed to take in a .uniGcode file from constrains
default output and write a new file that contains: how many
variants per conserved marker gene, the total nucleotide
length of each marker gene, and the proportion of variants
divided by total nucleotides.
Options allow for writing a whole directory of 
Example usage:
$ python constrainsUniGCodeParser.py -f results/uniGcode/eubRect.uniGcode
OR
$ python constrainsUniGCodeParser.py -f results/uniGcode/*.uniGcode
'''

import os


def readUniGCode(file):
	'''
	Keep track of how many locations (per conserved marker protein)
	contain variants in a uniGcode file, along with the proportion of
	variants/total nucleotides.
	'''
	pidCounter = {}
	with open(file) as f:
		for i in range(3):
			line = f.readline()  # Skip 2 headers
		while line:
			line = line.strip().split('\t')
			pid = line[0]
			pos = int(line[1])
			nucleotides = line[3:]
			nt_length = len(set(nucleotides))
			if nt_length > 1:
				if pid in pidCounter:
					pidCounter[pid][0] += 1
					pidCounter[pid][1] = pos
					pidCounter[pid][2] = pidCounter[pid][0]/pos
				else:
					pidCounter[pid] = [1, pos, 1/pos]
			else:
				if pid in pidCounter:
					pidCounter[pid][1] = pos
					pidCounter[pid][2] = pidCounter[pid][0]/pos
				else:
					pidCounter[pid] = [0, pos, 0]
			line = f.readline()
	return pidCounter


def writePIDs(file, output):
	'''
	Function that writes a .output file given a .uniGcode
	file. Format is tab-delimited with columns:
	PID, Variants, Total Nucleotides, Proportion
	'''
	pids = readUniGCode(file)
	with open(output, 'w') as o:
		o.write(f"PID\tVariants\tTotal\tProportion\n")
		for key, value in pids.items():
			vals = '\t'.join([str(val) for val in value])
			o.write(f"{key}\t{vals}\n")
	return 0


def writeMultiplePIDs(files):
	'''
	Function that loops through a directory and parses all
	uniGcode files to output .output files.
	'''
	for file in files:
		if file.endswith(('.uniGcode')):
			output = file.rsplit('.', 1)[0] + '.output'
			print(f"File: {file}\tOutput: {output}\n")
			writePIDs(file, output)
		else:
			print(f"Invalid file type for: {file}")
	return 0


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Parser")
	parser.add_argument("-f", "--File",
		                help="uniGcode file or files to parse.",
		                required=False, nargs="*")
	arg = parser.parse_args()
	if arg.File:
		writeMultiplePIDs(arg.File)
	else:
		print("Please use argument -f to specify what \
			  uniGcode files you would like to parse.")
