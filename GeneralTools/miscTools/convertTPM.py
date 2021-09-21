'''
Program designed to normalized a count file, such as created
from HTSeq-count, from absolute values to transcripts per million
(TPM). This also requires a .GFF file that gives the length
information for each feature annotated.
Example usage:
$python convertTPM.py -c infile.count -g sample.gff -o outfile.tpm.count
'''
import argparse


def getGFFDic(gff):
    length_dic = {}
    with open(gff) as g:
        line = g.readline()
        while line:
            line = line.split('\t')
            contig = line[0]
            length = int(line[4])
            length_dic[contig] = length
            line = g.readline()
    return length_dic


def calcRPK(raw, length):
    raw = int(raw)
    length = int(length)
    kblength = length / 1000
    rpk = raw / kblength
    return rpk


def main(gff, counts, output):
    length_dic = getGFFDic(gff)
    rpk_dic = {}
    with open(output, 'w') as o:
        # Calculate RPK for each feature
        with open(counts) as i:
            line = i.readline().strip()
            while line:
                contig = line.split('\t')[0]
                raw = line.split('\t')[1]
                try:
                    length = length_dic[contig]
                except KeyError:
                    print(f"{contig} not found!")
                rpk = calcRPK(raw, length)
                rpk_dic[contig] = rpk
                line = i.readline().strip()
        # Loop through RPK dictionary and count TPM
        total = sum(rpk_dic.values()) / 1000000
        tpm = {k: v / total for k, v in rpk_dic.items()}
        o.write(f"Feature\tTPM\n")
        for key, value in tpm.items():
            o.write(f"{key}\t{value}\n")
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-g", "--GFF",
                        help="GFF file to get feature length.",
                        required=True)
    parser.add_argument("-c", "--Counts",
                        help="Count file (tab-delimited)",
                        required=True)
    parser.add_argument("-o", "--Output",
                        help="Output file (tab-delimited",
                        required=True)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(arg.GFF, arg.Counts, arg.Output)
