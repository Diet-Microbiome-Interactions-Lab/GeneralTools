'''
Author: Dane
Function: Takes contig reference file and fasta files of bins, and finds contigs that were not binned
Can use either a directory containing fasta files (bin files) or a bin identification file.
Input: python find_no_binners.py -b <list of bin fasta files> -r <reference contig fasta file>
Output: nobinners_<reference contig fasta file>

'''
import argparse
from Bio import SeqIO
import os
import random


def nobinners(fasta, reference):
    '''
    Reference is a dictionary in the form: dict[contig]=sequence.
    This function removes all contigs that are also found in a bin
    file. Input can either be a list of fasta files (bin directory)
    or a bin identification file.
    '''
    # Part 1: Read reference contigs into list
    all_contigs = {}
    with open(reference) as r:
        line = r.readline()
        while line:
            if line.startswith('>'):
                all_contigs[line.strip()] = ''
            line = r.readline()
    # Step 2: Check fasta/bin file(s) and remove contigs from all_contigs
    for binfile in fasta:
        print(f"Now parsing {binfile}")
        if (binfile.endswith('.fasta') or binfile.endswith('.fa')):
            for seq_record in SeqIO.parse(binfile, "fasta"):
                try:
                    del all_contigs[(str('>') + seq_record.id)]
                except ValueError:
                    print(
                        f"The contig ({seq_record.id}) was not found in the reference file provided")
                    print(
                        f"FYI, reference FASTA ident lines are formatted as: {all_contigs[0]}")
                    return 1
        elif binfile.endswith('.txt'):
            with open(binfile) as i:
                line = i.readline().split('\t')
                assert len(line) == 2, "Incorrect number of fields!"
                line = i.readline().split('\t')
                try:
                    float(line[0])
                except ValueError:
                    return "Bin identification file does not contain bin number in field 1"
                while (line and len(line) > 1):
                    try:
                        contig = line[1].strip()
                    except IndexError:
                        print(line)
                    if not contig.startswith('>'):
                        contig = '>' + contig
                    try:
                        del all_contigs[contig]
                    except KeyError:
                        print(
                            f"The contig ({contig}) was not found in the reference file provided")
                        # Print a random reference defline to highlight the format
                        print(
                            f"FYI, reference FASTA ident lines are formatted as: {random.choice(list(all_contigs.keys()))}")
                        return 1
                    line = i.readline().split('\t')
    return all_contigs


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--Bins", help="Bin fasta files from which to find nobinners",
                        required=True, nargs='*')
    parser.add_argument("-r", "--Reference", help="Reference contig fasta file to compare bin files to",
                        required=True)
    argument = parser.parse_args()
    contigs = nobinners(argument.Bins, argument.Reference)
    nobinners = "nobinners_" + os.path.basename(str(argument.Reference))
    with open(nobinners, 'w') as handle:
        for contig in contigs.keys():
            handle.write(f"NoBin\n{contig.strip('>')}\\n")
