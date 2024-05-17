'''
Note - this can be combined with the gff_mine.py program in the future!!!!!
Script designed to take in a file created from the gff_mine.py and produce
the top feature for each bin. The top feature is specified as the mode and ties
will be arbitrarily assigned on of the tying features.
Example usage:
$ python writeTopGFFFeature.py <inputfeature.txt> <output.txt>
'''
import sys


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
            assert len(line) == 4, "Error in number of delimiters."
            attrib = line[1]
            n = line[2]
            bins = line[3].strip()
            attrib = [attrib] * n
            try:
                output_dic[bins].extend(attrib)
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
                final_dic[bins] = [val, besthit]
    return final_dic


def write_new_bin_file(attfile, output):
    '''
    Function that takes in a dictionary in the form of:
    dict[bin] = [Assembly, N]
    '''
    # Dict[node] = bin
    # bin_dic = get_bin_dictionary(binfile)
    # Dict[bin] = Attribute
    att_dict = read_attribute_output(attfile)
    with open(output, 'w') as o:
        header = f"Bin\tAssembly\tN"
        for key in att_dict.keys():
            vals = '\t'.join([str(val) for val in att_dict[key]])
            writeline = key + '\t' + vals + '\n'
            o.write(writeline)
    return 0
    
write_new_bin_file(sys.argv[1], sys.argv[2])
