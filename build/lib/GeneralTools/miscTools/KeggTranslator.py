'''
Author: Dane
Purpose: Given a hierarchical text (htext) file downloaded from the KEGG
database, create a list of all KO (pathways) identifiers associated with
each individual Kegg identifier. See download at:
https://www.genome.jp/kegg-bin/get_htext?ko00001.keg

This program takes in a file containing a list of Kegg identifiers as a specified
field (by default, first field in tab-delimited file). If given Kegg identifiers,
all pathways that the Kegg identifier is in will be output.

Output is formated as: KeggIdentifier\tKO#1\tKO#2...\tKO#N i

Example usage:
$python KeggTranslator.py -Database <kegghtext.keg> -Input <myKeggFile.txt>
-Output <output.txt>
Note: Specify "--Field" only if KEGG identifiers are not in the first field.
Note: Specify "--Header False" if there is no header (default = True).
Note: Specify "--Log <logfilename.log" if a unique log file is desired.
'''


def read_htext_dictionary(file):
    '''
    Function that reads the lines of the htext Kegg database file into
    a dictionary in the form: dict[KIdent] = [KOPath]
    '''
    return_dictionary = {}
    with open(file) as i:
        line = i.readline()
        while line:
            if line.startswith('C'):
                # Grab the pathway name
                ko_number = line.split()[1]
                line = i.readline()
                while line.startswith('D'):
                    kegg_identifier = line.split()[1]
                    assert kegg_identifier.startswith(
                        'K'), "Invalid identifier!"
                    # Add to dictionary
                    if kegg_identifier in return_dictionary:
                        return_dictionary[kegg_identifier].append(ko_number)
                    else:
                        return_dictionary[kegg_identifier] = [ko_number]
                    line = i.readline()
            else:
                line = i.readline()
    print(len(return_dictionary))
    return return_dictionary


def read_kegg_file(database, file, output, log, field, header=True):
    '''
    Function that reads in a file where Kegg identifiers are located in the
    (default) first column, but if 'field' is specified, it could be a
    different column
    '''
    match = 0
    mismatch = 0
    mismatch_name = []
    total = 0
    kegg_dictionary = read_htext_dictionary(database)
    with open(output, 'w') as o:
        with open(file) as i:
            line = i.readline()
            if header:  # Skip the first line
                line = i.readline()
            while line:
                total += 1
                kegg_identifier = line.split()[int(field)]
                assert kegg_identifier.startswith('K'), "Invalid K identifier!"
                if kegg_identifier in kegg_dictionary:
                    pathways = '\t'.join(kegg_dictionary[kegg_identifier])
                    writeline = f"{kegg_identifier}\t{pathways}\n"
                    o.write(writeline)
                    match += 1
                else:
                    mismatch += 1
                    mismatch_name.append(kegg_identifier)
                line = i.readline()
    with open(log, 'w') as lg:
        lg.write(f"Total Kegg Identifiers to match: {total}\n")
        lg.write(f"Found {match} matches and {mismatch} had no pathway.\n")
        lg.write('\n'.join(mismatch_name))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-d", "--Database",
                        help="Kegg HTEXT database file",
                        required=True)
    parser.add_argument("-i", "--Input",
                        help="Input file with Kegg identifiers",
                        required=True)
    parser.add_argument("-o", "--Output",
                        help="Output file (tab-delimited)",
                        required=True)
    parser.add_argument("-l", "--Log",
                        help="Log file to write metadata to",
                        required=False, default="logfile.log")
    parser.add_argument("-f", "--Field",
                        help="Field (whitespace delimited) where Kegg Identifier is",
                        required=False, default=0)
    parser.add_argument("--Header",
                        help="If specified, there is a header in input file",
                        required=False, default=True)
    arg = parser.parse_args()
    read_kegg_file(arg.Database, arg.Input, arg.Output,
                   arg.Log, arg.Field, arg.Header)
