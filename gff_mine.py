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

import os
import argparse


def list_gff_attributes(gff):
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
    bindict = {}
    with open(binfile) as f:
        line = f.readline()  # Skip header
        line = f.readline()
        while line:
            line = line.split('\t')
            bindict[line[0].strip('>')] = line[1].strip()
            line = f.readline()
    return bindict


def get_gff_attribute(gff, attribute):
    mydict = {}
    with open(gff) as f:
        line = f.readline()  # Skip header
        line = f.readline().strip()
        while line:
            line = line.split('\t')
            contig = line[0]
            if len(line) > 8:
                attribs = line[8].split(';')
                for attrib in attribs:
                    if attrib.split('=')[0] == attribute:
                        att = attrib.split('=')[1]
                        if contig in mydict:
                            mydict[contig].append(att)
                        else:
                            mydict[contig] = [att]
                    else:
                        pass
            else:
                pass
            line = f.readline().strip()
            if line == '':
                line = f.readline().strip()
            else:
                pass
    return mydict


# def write_gff_attribute(gffdict, attribute, bins, outfile, top=None):
#     mydict = get_gff_attribute(gffdict, attribute)
#     bindict = get_bin_dictionary(bins)
#     with open(outfile, 'w') as o:
#         header = f"Contig\t{attribute}\tN\tBin\n"
#         o.write(header)
#         # For each contig in mydict (keys)
#         for key in mydict.keys():
#             # Flag to get only the top result
#             if top is not None:
#                 # Initialize a new dictionary
#                 valuedict = {}
#                 # Go through each unique value for the key
#                 for val in set(mydict[key]):
#                     # Use the attribute info as key, and count as value
#                     valuedict[val] = mydict[key].count(val)
#                 # Find the attribute with the highest count
#                 besthit = max(valuedict, key=lambda key: valuedict[key])
#                 print(besthit)
#                 # Create a variable of the count of the best hit
#                 count = valuedict[besthit]
#                 # If that node is in bin file, append information
#                 if key in bindict:
#                     # Initialize the write line
#                     writeline = f"{key}\t{besthit}\t{count}\t{bindict[key]}\n"
#                     o.write(writeline)
#                 else:
#                     writeline = f"{key}\t{besthit}\t{count}\tNoBin\n"
#                     o.write(writeline)
#             else:
#                 # Loop through all unique values in key
#                 for val in set(mydict[key]):
#                     # Count each one of those unique values occurences
#                     count = mydict[key].count(val)
#                     # If the key (node) matches a bin, append info
#                     if key in bindict:
#                         writeline = f"{key}\t{val}\t{count}\t{bindict[key]}\n"
#                         o.write(writeline)
#                     else:
#                         writeline = f"{key}\t{val}\t{count}\tNoBin\n"
#                         o.write(writeline)


def write_gff_attribute(gffdict, attribute, bins, outfile, top=None):
    mydict = get_gff_attribute(gffdict, attribute)
    bindict = get_bin_dictionary(bins)
    updict = {}
    for key in bindict.keys():
        updict[str(int(key.split('_')[1]))] = bindict[key]
    with open(outfile, 'w') as o:
        header = f"Contig\t{attribute}\tN\tBin\n"
        o.write(header)
        # For each contig in mydict (keys)
        for key in mydict.keys():
            # Flag to get only the top result
            if top is not None:
                # Initialize a new dictionary
                valuedict = {}
                # Go through each unique value for the key
                for val in set(mydict[key]):
                    # Use the attribute info as key, and count as value
                    valuedict[val] = mydict[key].count(val)
                # Find the attribute with the highest count
                besthit = max(valuedict, key=lambda key: valuedict[key])
                # Create a variable of the count of the best hit
                count = valuedict[besthit]
                # If that node is in bin file, append information
                identifier = str(int(key.split('_')[1]))
                if identifier in updict:
                    b = updict[identifier]
                    # Initialize the write line
                    writeline = f"{key}\t{besthit}\t{count}\t{b}\n"
                    o.write(writeline)
                else:
                    writeline = f"{key}\t{besthit}\t{count}\tNoBin\n"
                    o.write(writeline)
            else:
                # Loop through all unique values in key
                for val in set(mydict[key]):
                    # Count each one of those unique values occurences
                    count = mydict[key].count(val)
                    # If the key (node) matches a bin, append info
                    identifier = str(int(key.split('_')[1]))
                    if identifier in updict:
                        b = updict[identifier]
                        writeline = f"{key}\t{val}\t{count}\t{b}\n"
                        o.write(writeline)
                    else:
                        writeline = f"{key}\t{val}\t{count}\tNoBin\n"
                        o.write(writeline)


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
                        required=False, default=None)
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
