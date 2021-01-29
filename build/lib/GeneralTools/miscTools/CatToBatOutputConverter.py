#!/usr/bin/env python3

## Source: https://github.com/dutilh/CAT/issues/28
## addBinsCATfileForBAT.py - Add the bin names to the contigs from the CAT proteins
##

# The BAT tool can't use the predicted proteins from CAT, because the
# contigs lack the bin name.


from os import listdir
from os.path import join
import argparse
from sys import argv

parser = argparse.ArgumentParser(description="Filter missing contigs from CAT predicted proteins fasta for BAT")
parser.add_argument('-b','--bin_folder', dest='bin_dir', required=True,
                          type=str, help='Path to the directory containing the bins.')
parser.add_argument('-s','--bin_suffix',dest='bin_suffix', type=str, default='.fna',
                          help='Suffix of bins in bin folder (default: .fna).')

parser.add_argument('-p','--proteins_fasta', dest='predictedproteins_file',
                          required=True, type=str,
                          help='Path to existing predicted proteins fasta')
parser.add_argument('-d','--diamond_alignment', dest='diamond_file',
                          required=True, type=str,
                          help='Path to existing DIAMOND alignment table')

parser.add_argument('-P','--new_proteins_fasta', dest='new_predictedproteins_file',
                          required=True, type=str,
                          help='Path to new predicted proteins fasta')
parser.add_argument('-D','--new_diamond_alignment', dest='new_diamond_file',
                          required=True, type=str,
                          help='Path to new DIAMOND alignment table')

args = parser.parse_args(argv[1:])

bins = filter(lambda f: f.endswith(args.bin_suffix), listdir(args.bin_dir))

def getID(line):
    return line[1:].split(" ")[0].strip()

def getFASTAids(fastafile: str) -> list:
    with open(fastafile) as lines:
        lines = map(str.lstrip,lines)
        lines = filter(lambda l:l.startswith(">"),lines)
        ids = map(getID,lines)
        return list(ids)


bin_contigs = {fastaid:bin for bin in bins for fastaid in getFASTAids(join(args.bin_dir,bin))}

def getcontigID(orfid):
    return orfid.rsplit("_",1)[0]

with open(args.new_predictedproteins_file,"w") as out:
    with open(args.predictedproteins_file) as lines:
        lines = map(str.lstrip,lines)
        writeentry = False
        for line in lines:
            if line.startswith(">"):
                contigid = getcontigID(getID(line))
                writeentry = contigid in bin_contigs.keys()
                if writeentry:
                    _ = out.write(">")
                    _ = out.write(bin_contigs[contigid])
                    _ = out.write("_")
                    _ = out.write(line[1:])
            elif writeentry:
                _ = out.write(line)

with open(args.new_diamond_file,"w") as out:
    with open(args.diamond_file) as lines:
        for line in lines:
            orfid = line.split("\t")[0]
            contigid = getcontigID(orfid)
            if contigid in bin_contigs.keys():
                _ = out.write(bin_contigs[contigid])
                _ = out.write("_")
                _ = out.write(line)
