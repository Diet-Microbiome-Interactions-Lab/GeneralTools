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
from Bio import SeqIO


def main(reflist, querylist, output):
    '''
    Write a matrix to compare the sequence identity shared between
    two sets of bins. This will pairwise compare all MAGs/.mfa files.
    '''
    all_references = []
    references = {}
    for ref in reflist:
        ref_name = os.path.splitext(os.path.basename(ref))[0]
        all_references.append(ref_name)
        for record in SeqIO.parse(ref, "fasta"):
            references.setdefault(record.seq, [])
            references[record.seq].append(ref_name)

    master_dic = {}
    for quer in querylist:
        quer_name = os.path.splitext(os.path.basename(quer))[0]
        master_dic[quer_name] = {}

        for record in SeqIO.parse(quer, "fasta"):
            if record.seq in references:
                for ref_name in references[record.seq]:
                    master_dic[quer_name].setdefault(ref_name, 0)
                    master_dic[quer_name][ref_name] += 1

    print(master_dic)
    # # Write the output matrix
    # header = ["Index"] + header + ["\n"]
    # header = '\t'.join(header)
    # with open(output, 'w') as out:
    #     out.write(header)
    #     for quer in master_dic.keys():
    #         line = [str(master_dic[quer][val])
    #                 for val in master_dic[quer].keys()]
    #         writeline = [quer] + line + ['\n']
    #         writeline = '\t'.join(writeline)
    #         out.write(writeline)

    with open(output, 'w') as _out:
        header = 'Query\t' + '\t'.join(list(master_dic.keys())) + '\n'
        _out.write(header)
        for quer_name in master_dic.keys():
            for ref_name in all_references:
                writeline = [ref_name]
                master_dic[quer_name].setdefault(ref_name, 0)
                writeline.append(master_dic[quer_name][ref_name])
            writeline = '\t'.join(str(v) for v in writeline) + '\n'
            _out.write(writeline)


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
