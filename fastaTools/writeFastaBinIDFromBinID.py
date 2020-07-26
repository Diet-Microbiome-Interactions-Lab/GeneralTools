"""
Program designed to take in a bin id file and an assembly
file and will output:
1.) New fasta files IF --FastaDirectory <location> is specified
Note: Fasta file names will be written in the format: <binID>.fasta
2.) New BinID file IF --Identity <filename> is specified
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


def write_fastas(binfile, assemblyfile, outdirectory=False, ident=False):
    '''
    Function that writes a new FASTA file the defline
    of the assembly matches a bin entry
    '''
    if outdirectory is not False:
        id_dic = {}
        bindic = read_binfile(binfile)
        for record in SeqIO.parse(assemblyfile, "fasta"):
            match = record.id.split('length')[0]
            if match in bindic:
                outfile = f"{outdirectory}/{bindic[match]}.fasta"
                with open(outfile, 'a') as o:
                    o.write(f">{record.id}\n{record.seq}\n")
                    id_dic[str(record.id)] = bindic[match]
    if ident is not True:
        with open(str(ident), 'w') as o:
            for node, bins in id_dic.items():
                o.write(f">{node}\t{bins}\n")
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
                        required=False)
    parser.add_argument("-i", "--Identity",
                        help="Optional argument to write new binID file",
                        required=False)
    argument = parser.parse_args()
    if (argument.Identity and argument.FastaDirectory):
        write_fastas(argument.Bins, argument.Assembly,
                     ident=argument.Identity,
                     outdirectory=argument.FastaDirectory)
    elif argument.Identity:
        write_fastas(argument.Bins, argument.Assembly,
                     ident=argument.Identity)
    else:
        write_fastas(argument.Bins, argument.Assembly,
                     outdirectory=argument.FastaDirectory)
