'''
Author: Dane
Program designed to take metaphlan output that contains 4 columns -
such as where additional species are listed - and cut down to only
the top species hit and abundance score.

Example usage:
$ python processMetaphlanOutput.py <initialMetaphlanFile.txt> <outputMetaphlan.txt>
'''

import sys


def process_metaphlan_output(file, output):
    '''
    Function to morph a MetaPhlAn output file with multiple
    species per clade into a format friendly for ConStrains.
    This form consists only of 2 columns:
    clade_name and relative_abundance.
    '''
    print(f"File:\t{file}\nOutput:\t{output}")
    with open(output, 'w') as o:
        o.write(f"#clade_name\trelative_abundance\n")
        with open(file) as i:
            line = i.readline()
            print(f"This is my line:\n{line}\n")
            while line:
                if line.startswith('#'):
                    pass
                else:
                    cladeName = line.split()[0]
                    relAbund = line.split()[2]
                    o.write(f"{cladeName}\t{relAbund}\n")
                line = i.readline()
    return 0


if __name__ == "__main__":
    process_metaphlan_output(sys.argv[1], sys.argv[2])
