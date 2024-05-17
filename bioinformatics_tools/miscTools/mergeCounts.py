'''
Program designed to merge multiple TPM files into 1 matrix
Example usage:
$python mergeCounts.py -i infile.count -o outfile.tpm.count
'''


def mergeCounts(files, outfile):
    output = {}
    header = ["Feature"]
    for file in files:
        header.append(file.split('/')[-1])
        print(file)
        with open(file) as i:
            line = i.readline()  # Skip header
            line = i.readline()
            while line:
                line = line.strip().split('\t')
                if line[0] not in output:
                    output[line[0]] = [line[1]]
                else:
                    output[line[0]].append(line[1])
                line = i.readline()
    # Write the output to a master sheet
    with open(outfile, 'w') as o:
        writehead = '\t'.join(header) + '\n'
        o.write(writehead)
        for contig, tpms in output.items():
            writeline = contig + '\t' + '\t'.join(tpms) + '\n'
            o.write(writeline)
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-i", "--Infiles",
                        help="TPM files to merge",
                        required=True, nargs="*")
    parser.add_argument("-o", "--Output",
                        help="Output file to write to",
                        required=True)
    arg = parser.parse_args()
    mergeCounts(arg.Infiles, arg.Output)
