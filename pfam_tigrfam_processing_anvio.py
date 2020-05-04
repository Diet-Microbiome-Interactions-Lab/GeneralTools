import os
import sys

tigrfile = sys.argv[1]
pfamfile = sys.argv[2]
direct = sys.argv[3]
output = sys.argv[4]

match = '.INFO'


def merge_tigr_pfam(tigrfile, pfile, direct, output):
    with open(output, 'w') as testfile:
        header = 'gene_callers_id\tsource\taccession\tfunction\te_value\n'
        testfile.write(header)
        with open(tigrfile) as f:
            # Skip comments
            line = f.readline()
            while line:
                if line.startswith('#'):
                    line = f.readline()
                else:
                    line = line.split()
                    gene_id = line[0]
                    access = line[3]
                    e_val = line[4]
                    for tfile in os.listdir(direct):
                        if tfile.startswith(access):
                            with open(os.path.join(direct, tfile)) as tf:
                                for i in range(3):
                                    de = tf.readline().strip().strip('DE ')
                                for i in range(9):
                                    cc = tf.readline().strip().strip('CC ')
                                function = de + ': ' + cc
                    newline = '\t'.join([gene_id, 'TIGRFAM',
                                         access, function, e_val])
                    testfile.write(newline + '\n')
                    line = f.readline()
        # Now append information for Pfam to the end
        with open(pfamfile) as pf:
            # Skip comments
            line = pf.readline()
            while line:
                if line.startswith('#'):
                    line = pf.readline()
                else:
                    line = line.split()
                    gene_id = line[0]
                    access = line[3]
                    e_val = line[4]
                    function = line[2]
                    newline = '\t'.join([gene_id, 'Pfam', access, function, e_val])
                    testfile.write(newline + '\n')
                    line = pf.readline()


if __name__ == "__main__":
    merge_tigr_pfam(tigrfile, pfamfile, direct, output)
