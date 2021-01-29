'''
Author: Dane
Date: 05Jan21
Purpose: Pairwise compare all bins/mags between two lists to see how much
sequence content is exactly the same and output a matrix:
|Reference|Bin1|Bin2|Bin3|
|Bin1'    | 2  | 0  | 1  |
|Bin2'    | 0  | 3  | 0  |
|Bin3'    | 0  | 1  | 2  |


Example usage:
$ python filterAssembly.py <assembly.fasta> <bid.txt> <output.txt>

'''
import os
from Bio.SeqIO.FastaIO import SimpleFastaParser


def main(reflist, querylist, output):
    '''
    Write a matrix to compare the sequence identity shared between
    two sets of bins. This will pairwise compare all MAGs/.mfa files.
    '''
    header = []
    ref_dic = {}
    for ref in reflist:
        ref_name = os.path.splitext(os.path.basename(ref))[0]
        header.append(ref_name)
        ref_dic[ref_name] = []
        with open(ref) as ref:
            for values in SimpleFastaParser(ref):
                # defline = values[0]
                seq = values[1]
                ref_dic[ref_name].append(seq)  # Collect all seqs in fasta

    master_dic = {}
    for quer in querylist:
        quer_name = os.path.splitext(os.path.basename(quer))[0]
        master_dic[quer_name] = {}
        with open(quer) as quer:
            for values in SimpleFastaParser(quer):
                # defline = values[0]
                seq = values[1]
                for reference in ref_dic.keys():
                    # Make sure the nested dict exists
                    if reference in master_dic[quer_name]:
                        pass
                    else:
                        master_dic[quer_name][reference] = 0
                    # Count similarities
                    if seq in ref_dic[reference]:
                        master_dic[quer_name][reference] += 1
                    else:
                        pass

    print(master_dic)
    # Write the output matrix
    header = ["Index"] + header + ["\n"]
    header = '\t'.join(header)
    with open(output, 'w') as out:
        out.write(header)
        for quer in master_dic.keys():
            line = [str(master_dic[quer][val])
                    for val in master_dic[quer].keys()]
            writeline = [quer] + line + ['\n']
            writeline = '\t'.join(writeline)
            out.write(writeline)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-q", "--Query",
                        help="Query file directory", required=True,
                        nargs='*')
    parser.add_argument("-r", "--Reference",
                        help="Reference file directory", required=True,
                        nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output file to write to",
                        required=True)
    argument = parser.parse_args()
    main(argument.Query, argument.Reference, argument.Output)
