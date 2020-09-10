'''
Author: Dane Deemer
Script used to filter a .GFF file to contain either:
i) Only entries that contain a specific feature, OR
ii) Only entries that contain a specific feauture and are
indicated in a bin identification file.

Example usage:
$ python trimGFFByFeature.py 
'''
import os
import sys


def bin_dict(binfile):
    '''
    Function that reads a binID file and returns
    a dictionary
    '''
    bin_dic = {}
    with open(binfile) as i:
        line = i.readline()  # Skip header
        line = i.readline().strip()
        while line:
            line = line.split('\t')
            b = line[0]
            node = line[1]
            bin_dic[node] = b
            line = i.readline().strip()
    return bin_dic


def trim_gff_by_feature(gff, feat_name, binfile=False):
    '''
    Function that removes all feature entries in
    a .GFF(v3) file that do not contain the feature
    indicated. If binfile is provided, it also filters
    to only contain entries in the binfile.
    '''
    new_output = f"{str(gff).rsplit('.', 1)[0]}.{feat_name}.gff"
    with open(new_output, 'w') as o:
        with open(gff) as i:
            line = i.readline()  # Skip header
            o.write(line)
            line = i.readline().strip()
            while line:
                try:
                    cur_line = line.split('\t')
                    node = cur_line[0]
                    features = cur_line[8].split(';')
                    for feature in features:
                        attrib = feature.split('=')[0]
                        if attrib == str(feat_name):
                            if binfile:
                                bin_dic = bin_dict(binfile)
                                if node in bin_dic.keys():
                                    o.write(f"{line}\n")
                                    break
                            else:
                                o.write(f"{line}\n")
                        else:
                            pass
                except IndexError:
                    pass
                line = i.readline().strip()


def write_vanilla_gff(gff):
    '''
    Function that takes in a GFF file and outputs a vanilla GFF file,
    which creates an entry for every sequence ID and for the feature it
    writes "gene_id <sequenceID>". Example usage would be to create a simple
    GFF file to count how many reads from a BAM file overlap each contig in
    an assembly.
    '''
    # Keep track of contigs so they only get read once
    read_list = []
    output = os.path.basename(gff).rsplit('.', 1)[0]
    output = output + ".vanilla.gff"
    with open(output, 'w') as o:
        with open(gff) as i:
            line = i.readline()  # Skip header
            line = i.readline()
            while line:
                line = line.split('\t')
                if (line[0].startswith('NODE') and line[0] not in read_list):
                    length = line[0].split('_')[3]
                    writeline=[line[0], 'bowtie2', 'contig', '1', str(length), '40', '.', '.', f'gene_id "{line[0]}"']
                    writeline = '\t'.join(writeline) + '\n'
                    o.write(writeline)   
                    read_list.append(line[0])
                else:
                    pass
                line = i.readline()
                                        
if __name__ == "__main__":
    import argparse
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-g", "--GFF", help="GFF file (Version 3)",
                        required=True)
    parser.add_argument("-f", "--Feature", help="Feature to count (Default=gene_id)",
                        required=False, default='gene_id')
    parser.add_argument("-b", "--Bins", help="Bin identification file",
                        required=False, default=False)
    parser.add_argument("-v", "--Vanilla", help="If specified, creates a GFF file where each \
    sequence ID is turned into the feature of choice, with contig length extracted from node name",
                        required=False, action='store_true')
    argument = parser.parse_args()
    if argument.Vanilla:
        write_vanilla_gff(argument.GFF)
    else:
        trim_gff_by_feature(argument.GFF, argument.Feature, binfile=argument.Bins)
