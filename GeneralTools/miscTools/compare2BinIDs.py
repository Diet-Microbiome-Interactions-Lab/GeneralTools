    '''
    Given two bin identification files, count how many contigs overlap.
    Within that contig overlap, count how many are in the same bin vs.
    how many end up in different bins.
    '''
    import sys


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


    if __name__ == '__main__':
        a = main(sys.argv[1], sys.argv[2])
        print(a)
