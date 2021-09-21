def stringToSplitFasta(string, start, end, delim):
    commonHeaderString = '_'.join(
        (string.split(f"{delim}")[int(start):int(end)]))
    return commonHeaderString + '.fasta'


def main(file, start, end, delim):
    seen_header = []
    with open(file) as fopen:
        line = fopen.readline()
        while line:
            if line.startswith('>'):
                commonHeaderString = stringToSplitFasta(
                    line, start, end, delim)
                if commonHeaderString in seen_header:
                    with open(commonHeaderString, 'a') as currentfile:
                        currentfile.write(line)
                        line = fopen.readline()
                        while line and not line.startswith('>'):
                            currentfile.write(line)
                            line = fopen.readline()
                else:
                    seen_header.append(commonHeaderString)
                    with open(commonHeaderString, 'w') as currentfile:
                        currentfile.write(line)
                        while line and not line.startswith('>'):
                            currentfile.write(line)
                            line = fopen.readline()
            else:
                print('Something is being missed...')
                line = fopen.readline()


myfile = 'HL_UCC_isolates_current.fasta'

main(myfile, 1, 4, " ")
