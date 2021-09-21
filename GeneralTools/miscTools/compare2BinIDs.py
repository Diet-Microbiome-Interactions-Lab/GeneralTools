'''
Given two bin identification files, count how many contigs overlap.
Within that contig overlap, count how many are in the same bin vs.
how many end up in different bins.
'''
import argparse


def read_binfile(binfile):
    '''
    Function that reads in a binID file into a dictionary
    in the form: dic[nodeNum]=binID
    '''
    bin_dic = {}
    with open(binfile) as b:
        line = b.readline()
        while line:
            contig = line.split('\t')[1].strip()
            bin_num = line.split('\t')[0]
            bin_dic[contig] = bin_num
            line = b.readline()
    return bin_dic


def main(bin1, bin2):
    '''
    Compare two bin files
    '''
    b1 = read_binfile(bin1)
    b2 = read_binfile(bin2)
    matches = 0
    misplaced = 0
    intersection = b1.keys() & b2.keys()
    shared = len(intersection)
    for contig in intersection:
        if b1[contig] == b2[contig]:
            matches += 1
            print(f"Match:\t{contig}")
        else:
            misplaced += 1
            print(f"Mismatch:\t{contig}")
    return f"Matches: {matches}\nMisplaced: {misplaced}\nTotal: {shared}\n\n"


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-1", "--Bin1",
                        help="Bin 1", required=True)
    parser.add_argument("-2", "--Bin2",
                        help="Bin 2", required=True)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    a = main(args)
    print(a)
