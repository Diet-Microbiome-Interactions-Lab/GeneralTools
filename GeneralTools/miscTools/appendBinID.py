'''
Author: Dane
Program that will append the bin identification a new field in a file
delimited by a specified character. User must specify which field will
be used for comparison and the delimiter.

Example usage:
$ python appendBinID.py
'''
import argparse


def get_bin_dic(reference, delim='\t', ref_contig=1, ref_bin=0):
    '''
    Given a reference file - i.e., a file linking a contig name to a
    specific bin - append the bin information to the query file
    '''
    ref_contig, ref_bin = int(ref_contig), int(ref_bin)
    ref_dic = {}
    cnt = 0
    with open(reference) as ref:
        line = ref.readline().strip().split(delim)
        while line and line[0] != '':
            contig = line[ref_contig]
            bins = line[ref_bin]
            ref_dic[contig] = bins
            cnt += 1
            line = ref.readline().strip().split(delim)
    print(cnt)

    return ref_dic


def main(reference, query, output, delim='\t', ref_contig=1, ref_bin=0, que_contig=0):
    '''
    Pass
    '''
    matches = 0
    ref_dic = get_bin_dic(reference, delim, ref_contig, ref_bin)
    with open(output, 'w') as o:
        with open(query) as i:
            line = i.readline().strip().split(delim)  # Skip header
            writeline = '\t'.join(line) + '\t' + 'Bin' + '\n'
            o.write(writeline)
            line = i.readline()
            while line:
                line = line.strip().split(delim)
                query_contig = line[que_contig]
                if query_contig in ref_dic:
                    matches += 1
                    line.append(ref_dic[query_contig])
                    writeline = '\t'.join(line) + '\n'
                    o.write(writeline)
                else:
                    pass
                line = i.readline()
    print(matches)
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-r", "--Reference",
                        help="Reference file", required=True)
    parser.add_argument("-q", "--Query",
                        help="Query file", required=True)
    parser.add_argument("-o", "--Output",
                        help="Output file", required=True)
    parser.add_argument("-d", "--Delimiter",
                        help="Delimiter", required=False,
                        default="\t")
    parser.add_argument("-c", "--ReferenceContig",
                        help="Reference contig number", required=False,
                        default=1)
    parser.add_argument("-b", "--ReferenceBin",
                        help="Reference bin number", required=False,
                        default=0)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
