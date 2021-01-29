"""
Author: Dane
Date: NA
Purpose: Program designed to take in a binfile that has been
simplified via Anvi'os requirements and the original
assembly with orginal node names. It then outputs a new bin
identification file with original names.

Example usage:
$ python change_bin_nodenames.py -b <binfile.txt> \
-a <assembly.fasta> -o <new-binfile.txt>
"""
from Bio.SeqIO.FastaIO import SimpleFastaParser


def readBinID(binfile):
    '''
    Open up a bin identification file and grab the simplified
    contig name as the index.
    '''
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


def readAssembly(assemblyfile):
    assembly = {}
    with open(assemblyfile) as a:
        for values in SimpleFastaParser(a):
            defline = values[0]
            match = defline.split('_')[1]
            assembly[match] = defline
    return assembly


def changeNames(binfile, assembly, output):
    '''
    Given a simplified bin id file, change back to full names
    with the input of the original assembly with original
    names.
    '''
    bins = readBinID(binfile)
    origLen = len(bins)

    writeLen = 0
    with open(output, 'w') as out:
        with open(assembly) as a:
            for values in SimpleFastaParser(a):
                defline = values[0]
                match = defline.split('_')[1]
                try:
                    writeline = f"{defline}\t{bins[match]}\n"
                    out.write(writeline)
                    writeLen += 1
                except KeyError:
                    pass

    # Make sure you wrote all of the contigs.
    assert origLen == writeLen, "Did not write all contigs!"
    return 0


if __name__ == "__main__":
    import argparse
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--Bins", help="File containing bins",
                        required=True)
    parser.add_argument("-a", "--Assembly", help="Assembly file",
                        required=True)
    parser.add_argument("-o", "--Output", help="Updated bin list name",
                        required=False)
    argument = parser.parse_args()
    changeNames(argument.Bins, argument.Assembly, argument.Output)
