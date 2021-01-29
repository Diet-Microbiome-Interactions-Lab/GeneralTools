'''
Super simple script that takes the stdout from CheckM
and writes it to a tab-delimited file, adding 1 additional
column that traces the file it came from!

Example usage:
$ python grabCheckMOutput.py checkMOut.out output.txt
'''
import sys


def grab_checkm_out(checkm_file, output):
    writelist = []
    with open(checkm_file) as checkm:
        line = checkm.readline()
        while line:
            line = line.strip()
            if (line.startswith("Bin") or line.startswith("bin")):
                line = line.split('\t')
                writeline = '\t'.join(line + [str(checkm_file)])
                writeline = writeline + '\n'
                writelist.append(writeline)
            else:
                pass
            line = checkm.readline()
    with open(output, 'w') as o:
        for line in writelist:
            o.write(line)


grab_checkm_out(sys.argv[1], sys.argv[2])
