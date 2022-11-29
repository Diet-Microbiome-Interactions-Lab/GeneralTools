''' Program that takes in a gff (version 3) file and parses out information
of interest

Three main uses:

1. List all attribute information that a gff (3) file contains:
- Requires the --List and --GFF flags only
- Start with this useage first to obtain --Attribute name
$ python gff_mine.py --GFF <example.gff> --List

2. Grab all information pertaining to an attribute:
- This outputs a tab-delimited file containing the contig name,
attribute called, number of times the attribute was called per contig,
and the bin the file is associated with
$ python gff_mine.py --GFF <example.gff> --Attribute <something-from-list>
--Bins <tab-delim-contigname-binname> --Output <outputfile.txt>

3. Grab all the top hit of an attribute per contig:
- For example, when many genomedb_acc have hits to an assembly, this
will filter only the mode genomedb_acc and report
$ python gff_mine.py --GFF <example.gff> --Attribute <something-from-list>
--Bins <tab-delim-contigname-binname> --Output <outputfile.txt> --Top True


'''
import argparse


def list_gff_attributes(gff):
    '''
    Function that takes in a gff file and lists all
    annotation attributes inside the file to the stdout
    '''
    identifiers = []
    with open(gff, errors='replace') as f:
        line = f.readline()  # Skip header
        line = f.readline().strip()
        while line:
            line = line.split('\t')
            if len(line) > 8:
                attribs = line[8].split(';')
                for count, attrib in enumerate(attribs):
                    if attrib.split('=')[0] not in identifiers:
                        identifiers.append(attrib.split('=')[0])
                    else:
                        pass
            else:
                pass
            line = f.readline().strip()
            if line == '':
                line = f.readline().strip()
            else:
                pass
    return identifiers


def get_bin_dictionary(binfile):
    '''
    Read in a bin identification file in the form of:
    dict[Node] = BinX
    Note: Some finagling may be needed to format properly
    '''
    bindict = {}
    with open(binfile) as f:
        line = f.readline().strip()
        while line:
            line = line.split('\t')
            binid = line[0]
            contig = line[1].strip('>')
            bindict[contig] = binid
            line = f.readline().strip()
    return bindict


def get_gff_attribute(gff, attribute):
    '''
    Given a GFF file and a specified attribute (see list_gff_attributes
    for a list of all possible attributes for a given GFF file), return
    a dictionary in the form:
    dict[Node] = [Attribute1, Attribute2, ... AttributeN]
    For example:
    dict[Node_1] = [pfam002, pfam098, pfam121]
    '''
    attrib_dict = {}
    with open(gff) as f:
        line = f.readline()  # Skip header
        line = f.readline().strip()
        while line:
            line = line.split('\t')
            contig = line[0]
            try:
                if line[8].startswith('Locus'):
                    attribs = line[8].split(';')
                for attrib in attribs:
                    if attrib.split('=')[0] == attribute:
                        att = attrib.split('=')[1]
                        if contig in attrib_dict:
                            attrib_dict[contig].append(att)
                        else:
                            attrib_dict[contig] = [att]
                    else:
                        pass
            except IndexError:
                pass
            line = f.readline().strip()
            if line == '':
                line = f.readline().strip()
            else:
                pass
    return attrib_dict


def write_gff_attribute(gffdict, attribute, bins, outfile, top=False):
    '''
    Function that reports GFF results of a specified attribute and
    appends bin information
    '''
    attrib_dict = get_gff_attribute(gffdict, attribute)
    bin_dict = get_bin_dictionary(bins)
    with open(outfile, 'w') as o:
        header = f"Contig\t{attribute}\tN\tBin\n"
        o.write(header)
        for node in attrib_dict.keys():
            # Flag to get only the top result
            if top is True:
                # Initialize a new dictionary
                valuedict = {}
                # Go through each unique value for the node
                for val in set(attrib_dict[node]):
                    # Count each occurence of attrib
                    valuedict[val] = attrib_dict[node].count(val)
                # Find the attribute with the highest count
                besthit = max(valuedict, key=lambda key: valuedict[val])
                # Create a variable of the count of the best hit
                count = valuedict[besthit]
                # If that node is in bin file, append information
                if node in bin_dict:
                    # Grab the bin information
                    b = bin_dict[node]
                    # Initialize the write line
                    writeline = f"{node}\t{besthit}\t{count}\t{b}\n"
                    o.write(writeline)
                else:
                    writeline = f"{node}\t{besthit}\t{count}\tNoBin\n"
                    o.write(writeline)
            else:
                # Loop through all unique values in node
                for val in set(attrib_dict[node]):
                    # Count each one of those unique values occurences
                    count = attrib_dict[node].count(val)
                    # If the node (node) matches a bin, append info
                    if node in bin_dict:
                        b = bin_dict[node]
                        writeline = f"{node}\t{val}\t{count}\t{b}\n"
                        o.write(writeline)
                    # Otherwise write all information and label bin as NoBin
                    else:
                        writeline = f"{node}\t{val}\t{count}\tNoBin\n"
                        o.write(writeline)
    return 0


if __name__ == "__main__":
    """ Arguments """
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-l", "--List", help="List all attributes",
                        required=False, action='store_true')
    parser.add_argument("-g", "--GFF", help="GFF file (Version 3)",
                        required=True)
    parser.add_argument("-a", "--Attribute", help="Attribute to extract",
                        required=False)
    parser.add_argument("-b", "--Bins", help="Bin identifier file",
                        required=False)
    parser.add_argument("-o", "--Output", help="Output file to write",
                        required=False)
    parser.add_argument("-t", "--Top", help="Get the hit with mode per contig",
                        required=False, default=None, action='store_true')
    argument = parser.parse_args()
    """ Arguments """
    if argument.List:
        a = list_gff_attributes(argument.GFF)
        for count, val in enumerate(a):
            print(f"{count}:\t{val}")
    else:
        write_gff_attribute(argument.GFF, argument.Attribute,
                            argument.Bins, argument.Output,
                            argument.Top)
