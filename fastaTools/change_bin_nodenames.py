"""
Program designed to take in a binfile that has been
simplified via Anvi'os requirements and the original
assembly with orginal node names. It then outputs
a new bin identification file with original names.

Example usage:
$ python change_bin_nodenames.py -b <binfile.txt>
-a <assembly.fasta> -o <new-binfile.txt>
"""

import argparse


def read_bins(binfile):
    bins = {}
    with open(binfile) as b:
        line = b.readline()
        while line:
            match = line.split('\t')[0].split('_')[1]
            match = str(int(match))
            bi = line.split('\t')[1].strip()
            bins[match] = bi
            line = b.readline()
    return bins


def read_assembly(assemblyfile):
    assembly = {}
    with open(assemblyfile) as a:
        line = a.readline()
        while line:
            if line.startswith('>'):
                match = str(line.split('_')[1])
                node = line.strip()
                assembly[match] = node
            else:
                pass
            line = a.readline()
    return assembly


def change_names(binfile, assembly, output):
    bins = read_bins(binfile)
    assembly = read_assembly(assembly)
    with open(output, 'w') as o:
        for b in bins.keys():
            if b in assembly:
                writeline = f"{assembly[b]}\t{bins[b]}\n"
                o.write(writeline)
            else:
                pass
    return 'Done'


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--Bins", help="File containing bins",
                        required=True)
    parser.add_argument("-a", "--Assembly", help="Assembly file",
                        required=True)
    parser.add_argument("-o", "--Output", help="Updated bin list name",
                        required=False)
    argument = parser.parse_args()
    change_names(argument.Bins, argument.Assembly, argument.Output)
