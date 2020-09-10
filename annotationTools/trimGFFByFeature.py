'''
Author: Dane Deemer
Script used to filter a .GFF file to contain either:
i) Only entries that contain a specific feature, OR
ii) Only entries that contain a specific feauture and are
indicated in a bin identification file.

Example usage:
$ python trimGFFByFeature.py 
'''

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
                                o.write(f"{line}\n
                        else:
                            pass
                except IndexError:
                    pass
                line = i.readline().strip()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        trim_gff_by_feature(sys.argv[1], sys.argv[2], binfile=sys.argv[3])
    elif len(sys.argv) == 3:
        trim_gff_by_feature(sys.argv[1], sys.argv[2])
    else:
        print('Invalid number of arguments. Requires (1) GFF file, (2) Feature name and optionally (3) Binfile')
