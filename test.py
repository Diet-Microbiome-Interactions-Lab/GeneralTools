import sys


def parse_reports(full_path, output):
    flag = False
    writeline = ''
    with open(output, 'w') as o:
        with open(full_path) as i:
            header = i.readline().split()
            reference = f"Supernatant_{os.path.basename(header[0])}"
            query = f"Particle_{os.path.basename(header[1])}"
            line = i.readline()
            while line:
                if line.startswith('TotalSeqs'):
                    values = line.split()
                    refSeqs = values[1]
                    querSeqs = values[2]
                if line.startswith('AlignedSeqs'):
                    values = line.split()
                    refSeqsAln = values[1]
                    querSeqsAln = values[2]
                    refPercent = float(refSeqsAln.split('(')[1].split('%')[0])
                    querPercent = float(
                        querSeqsAln.split('(')[1].split('%')[0])
                    if (refPercent >= 50 or querPercent >= 50):
                        flag = True
                        writeline = f"{reference}\t{query}\t{refSeqs}\t{querSeqs}\t"
                        writeline = writeline + \
                            f"{refSeqsAln}\t{querSeqsAln}\t"
                        writeline = writeline + \
                            f"{refPercent}\t{querPercent}\t"
                    else:
                        flag = False
                        break
                line = i.readline()
                if flag:
                    while not line.startswith('[Alignments]'):
                        if line.startswith('UnalignedSeqs'):
                            values = line.split()
                            refSeqsUnAln = values[1]
                            querSeqsUnAln = values[2]
                            writeline = writeline + \
                                f"{refSeqsUnAln}\t{querSeqsUnAln}\t"
                        if line.startswith('TotalBases'):
                            values = line.split()
                            refBases = values[1]
                            querBases = values[2]
                            writeline = writeline + \
                                f"{refBases}\t{querBases}\t"
                        if line.startswith('AlignedBases'):
                            values = line.split()
                            refBasesAln = values[1]
                            querBasesAln = values[2]
                            writeline = writeline + \
                                f"{refBasesAln}\t{querBasesAln}\t"
                        if line.startswith('UnalignedBases'):
                            values = line.split()
                            refBasesUnAln = values[1]
                            querBasesUnAln = values[2]
                            writeline = writeline + \
                                f"{refBasesUnAln}\t{querBasesUnAln}\n"
                        line = i.readline()
                    o.write(writeline)
                    break
    return writeline


if __name__ == '__main__':
    parse_reports(sys.argv[1], sys.argv[2])
