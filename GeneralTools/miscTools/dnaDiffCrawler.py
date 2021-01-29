'''
Author: Dane
Creation: 19Nov20
Purpose: To parse a directory containing DNADiff results and filtering
for only files that contain a match (reference vs. query) above a defined
threshold.

Example usage:
$ python dnaDiffCrawler.py -d <directory> -s <percent_aligned_seqs>
-b <percent_aligned_bases>
'''
import os


def remove_non_reports(directory):
    for file in os.listdir(directory):
        if not file.endswith('.report'):
            full_path = os.path.join(directory, file)
            os.remove(full_path)
    return 0


def parse_reports(directory, output, threshold):
    count = 0
    with open(output, 'w') as o:
        for file in os.listdir(directory):
            flag = False
            full_path = os.path.join(directory, file)
            with open(full_path) as i:
                line = i.readline().split()
                reference = f"Supernatant_{os.path.basename(line[0])}"
                query = f"Particle_{os.path.basename(line[1])}"
                writeline = f"{reference}\t{query}\t"
                line = i.readline()
                while line:
                    if line.startswith('TotalSeqs'):
                        values = line.split()
                        refSeqs = values[1]
                        querSeqs = values[2]
                        writeline = writeline + f"{refSeqs}\t{querSeqs}\t"
                    if line.startswith('AlignedSeqs'):
                        values = line.split()
                        refSeqsAln = values[1]
                        querSeqsAln = values[2]
                        writeline = writeline + \
                            f"{refSeqsAln}\t{querSeqsAln}\t"
                        refPercent = float(
                            refSeqsAln.split('(')[1].split('%')[0])
                        querPercent = float(
                            querSeqsAln.split('(')[1].split('%')[0])
                        writeline = writeline + \
                            f"{refPercent}\t{querPercent}\t"
                        if (refPercent >= int(threshold) or querPercent >= int(threshold)):
                            count += 1
                            flag = True
                        else:
                            flag = False
                            writeline = ''
                    if flag:
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
                            refBPercent = float(
                                refBasesAln.split('(')[1].split('%')[0])
                            querBPercent = float(
                                querBasesAln.split('(')[1].split('%')[0])
                            writeline = writeline + \
                                f"{refBasesAln}\t{querBasesAln}\t{refBPercent}\t{querBPercent}\t"
                        if line.startswith('UnalignedBases'):
                            values = line.split()
                            refBasesUnAln = values[1]
                            querBasesUnAln = values[2]
                            writeline = writeline + \
                                f"{refBasesUnAln}\t{querBasesUnAln}\n"
                            print(writeline)
                            o.write(f"{writeline}")
                            writeline = ''
                    line = i.readline()
    with open('count.txt', 'w') as c:
        c.write(count)
    return writeline


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-d", "--Directory",
                        help="Directory containing dnadiff output.",
                        required=True)
    parser.add_argument("-o", "--Output",
                        required=True)
    parser.add_argument("-s", "--Seqs",
                        help="Percent of sequences aligned. Ex. 50",
                        required=False, default=50)
    parser.add_argument("-b", "--Bases",
                        help="Percent of bases aligned. Ex. 50",
                        required=False, default=50)
    argument = parser.parse_args()
    parse_reports(argument.Directory, argument.Output, argument.Seqs)
