'''
Script designed to take in a GFF attribute file with the top flag
specified and output a new bin identifier file.
This will be a part of 'gff_mine.py' eventually - maybe

Example usage:
$ python writeFlaggedContigsNewBinID.py -a genomedbAnnotations.txt \
-o supernatant-new-bins.txt
'''
import argparse


def read_attribute_output(attfile):
    '''
    Read in GFF attribute output and return a dictionary
    in the form of dict[bin] = attribute, where attribute is
    the attribute occuring the most for the bin
    '''
    output_dic = {}
    final_dic = {}
    '''
    Output dictionary is in the form of:
    dict[bins] = [attr1, attr2, etc.]...
    final_dic just subsets for highest occuring attribute
    '''
    with open(attfile) as f:
        line = f.readline()  # Skip header
        line = f.readline()
        while line:
            line = line.split('\t')
            bins = line[3].strip()
            attrib = line[1]
            try:
                output_dic[bins].append(attrib)
            except KeyError:
                output_dic[bins] = [attrib]
            line = f.readline()
    # Now loop through dictionary we created
    for bins in output_dic.keys():
        besthit = 0
        for val in set(output_dic[bins]):
            # Count each occurence of attrib
            count = output_dic[bins].count(val)
            if count > besthit:
                besthit = count
                final_dic[bins] = val
    return final_dic


def write_new_bin_file(attfile, output):
    # Dict[node] = bin
    # bin_dic = get_bin_dictionary(binfile)
    # Dict[bin] = Attribute
    '''
    Takes in an attribute file and writes a new bin identification
    file depending on if the contig contains the consensus attribute
    for the bin it is in (or remains NoBin if un-binned)
    '''
    att_dict = read_attribute_output(attfile)
    with open(attfile) as f:
        line = f.readline()  # Skip header
        line = f.readline()
        while line:
            line = line.split('\t')
            node = line[0]
            attrib = line[1]
            b = line[3].strip()
            # Test is attribute is the consensus for the bin
            if attrib == att_dict[b]:
                writeline = f"{node}\t{b}\n"
            else:
                if b == 'NoBin':
                    writeline = f"{node}\t{b}\n"
                else:
                    writeline = f"{node}\tRemoved\n"
            with open(output, 'a') as o:
                o.write(writeline)
            line = f.readline()
    return 0


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-a", "--Annotation",
                        help="Annotation file (output from gff_mine.py --Top)",
                        required=True)
    parser.add_argument("-o", "--OutBins",
                        help="Output bin identification file",
                        required=True)
    argument = parser.parse_args()
    write_new_bin_file(argument.Annotation, argument.OutBins)
