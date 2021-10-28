import os
import sys


def main(file):
    # Set indices for strings to mine
    indexForGff = [1, 7, 2, 3]
    # Set static vars
    feature, score, frame = ['gene', '.', '0']

    output = os.path.basename(os.path.splitext(file)[0]) + '.gff'
    with open(output, 'w') as out:
        with open(file) as infile:
            line = infile.readline()
            line = infile.readline().strip()
            while line:
                line = line.split('\t')
                seqname, source, start, end = [
                    line[val] for val in indexForGff
                ]
                attribute = f"gene_callers_id:{line[0]};"
                if line[4] == 'f':
                    strand = '+'
                elif line[4] == 'r':
                    strand = '-'
                else:
                    print(line[4])
                    raise IndexError('What is this?!?')
                writeline = '\t'.join(
                    [seqname, source, feature, start, end, score,
                     strand, frame, attribute, '\n']
                )
                out.write(writeline)
                line = infile.readline().strip()


main(sys.argv[1])
