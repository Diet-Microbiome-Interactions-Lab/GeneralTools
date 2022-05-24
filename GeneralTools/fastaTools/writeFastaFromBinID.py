"""
Program designed to take in an assembly file and a bin identification file and
will output a series of multi-fasta files (one corresponding to each bin in
the bin identification file).


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
import os


def read_binfile(binfile, header):
    '''
    Function that reads in a binID file into a dictionary
    in the form: dic[nodeNum]=binID
    '''
    bin_dic = {}
    with open(binfile) as b:
        if header:
            next(b)
        line = b.readline().strip()
        while line:
            contig = line.split('\t')[0]
            bin_num = line.split('\t')[1]
            bin_dic[contig] = bin_num
            line = b.readline().strip()
    return bin_dic


def write_fastas(binfile, header, assemblyfile, outdirectory):
    try:
        os.mkdir(outdirectory)
    except FileExistsError:
        pass
    # Option A: Write new multi-fasta files to 'outdirectory'
    bindic = read_binfile(binfile, header)
    for record in SeqIO.parse(assemblyfile, "fasta"):
        match = record.id.strip('>')
        if match in bindic:
            outfile = f"{outdirectory}/Bin.{bindic[match]}.fasta"
            with open(outfile, 'a') as o:
                o.write(f">{record.id}\n{record.seq}\n")
    return 0


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-a", "--Assembly", help="Assembly file",
                        required=True)
    parser.add_argument("-b", "--Bins", help="File containing bins",
                        required=True)
    parser.add_argument("-f", "--FastaDirectory",
                        help="Output directory to write to",
                        required=True)
    parser.add_argument("-h", "--Header",
                        required=False, default=False)
    args = parser.parse_args()
    write_fastas(args.Bins, args.Assembly, args.FastaDirectory, args.Header)
