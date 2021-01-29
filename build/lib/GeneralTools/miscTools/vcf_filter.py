"""
Program that takes as input a .vcf files and a list of
reference IDs to write to a new .vcf file
"""
import sys
import os

def get_reference_list(file, bin_num):
    lst = []
    with open(file) as f:
        line = f.readline()
        while line:
            nodenum = line.split('\t')[0].split('_')[1]
            nodenum = str(int(nodenum))
            bins = line.split('\t')[1].strip()
            if bins == bin_num:
                lst.append(nodenum)
            else:
                pass
            line = f.readline()
    return lst


def filter_vcf_file(vcf_file, filt, bin_num, output):
    with open(output, 'w') as o:
        files = get_reference_list(filt, bin_num)
        with open(vcf_file) as vcf:
            # Step 1: Write the top metadata
            for i in range(4):
                line = vcf.readline()
                o.write(line)
            # Proceed to next level of metadata
            line = vcf.readline()
            while line:
                if line.startswith('##contig'):
                    node = str(line.split('_')[1])
                    if node in files:
                        o.write(line)
                    else:
                        pass
                elif line.startswith('##'):
                    o.write(line)
                elif line.startswith('#CHROM'):
                    o.write(line)
                else:
                    lne = line.split('\t')
                    node = str(lne[0].split('_')[1])
                    if node in files:
                        o.write(line)
                    else:
                        pass
                line = vcf.readline()


if __name__ == '__main__':
    vcf = sys.argv[1]
    binfile = sys.argv[2]
    binnum = sys.argv[3]
    output = sys.argv[4]
    filter_vcf_file(vcf, binfile, binnum, output)
