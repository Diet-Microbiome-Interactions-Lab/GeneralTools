"""
Program designed to take in an assembly file and will output:
1.) New fasta files IF --FastaDirectory <location> is specified (and binID file)
Note: Fasta file names will be written in the format: <binID>.fasta
2.) New BinID file IF --Identity <filename> is specified, along with 
3.) Both IF both flags are raised


Example usage:
* Writing a new Bin ID file
$ python writeFastaFromBinID.py -a <assembly.fasta> -b <binID.txt> \
--Identity <sample.txt>
* Writing a new set of FASTA files
$ python writeFastaFromBinID.py -a <assembly.fasta> -b <binID.txt> \
--FastaDirectory <fastaLocation>

"""
import argparse
from Bio import SeqIO


def read_binfile(binfile):
    '''
    Function that reads in a binID file into a dictionary
    in the form: dic[nodeNum]=binID
    '''
    bins = {}
    with open(binfile) as b:
        line = b.readline()
        while line:
            match = line.split('\t')[0].split('_')[1]
            match = str(int(match))
            match = f"NODE_{match}_"
            bi = line.split('\t')[1].strip()
            bins[match] = bi
            line = b.readline()
    return bins


def write_fastas(binfile, assemblyfile, outdirectory):
    '''
    Function that writes a new FASTA file if the defline
    of the assembly matches a bin entry
    '''
    # Option A: Write new multi-fasta files to 'outdirectory'
    bindic = read_binfile(binfile)
    for record in SeqIO.parse(assemblyfile, "fasta"):
        match = record.id.strip('>')
        if match in bindic:
            outfile = f"{outdirectory}/{bindic[match]}.fasta"
            with open(outfile, 'a') as o:
                o.write(f">{record.id}\n{record.seq}\n")
    return 0


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-b", "--Bins", help="File containing bins",
                        required=True)
    parser.add_argument("-a", "--Assembly", help="Assembly file",
                        required=True)
    parser.add_argument("-f", "--FastaDirectory",
                        help="Output directory to write to",
                        required=True)
    argument = parser.parse_args()
    write_fastas(argument.Bins, argument.Assembly, argument.FastaDirectory)
