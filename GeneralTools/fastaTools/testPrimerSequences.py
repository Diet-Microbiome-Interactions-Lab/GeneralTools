from FastaLib import gcContent

import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
import re


def findClosestStrings(forward_results, reverse_results, sequence, save):
    all_results = []
    for forward in forward_results:
        start = forward[0]
        distance_threshold = 10000
        for reverse in reverse_results:
            end = reverse[1]
            distance = end - start
            if distance < distance_threshold and distance > 0:
                seq = sequence[start:end]
                gc_content = gcContent(seq)
                if save:
                    all_results.append((start, end, distance, gc_content, seq))
                else:
                    print('Pair detected...')
                    print(f'End: {end} - Start {start}')
                    print(f'Distance: {distance}')
                    print(f'Seq({seq})')
                    print(f'GC Content: {gc_content}\n')
    if len(all_results) > 0:
        return all_results
    return None


def writeResults(results, savefile):
    header = f'File\tDefline\tStart\tEnd\tSize\tGC\tSeq\n'
    with open(savefile, 'w') as out:
        out.write(header)
        for file in results:
            for defline in results[file]:
                for result in results[file][defline]:
                    stats = '\t'.join([str(res) for res in result])
                    writeline = f'{file}\t{defline}\t{stats}\n'
                    out.write(writeline)
    return 0


def main(args):
    output = {}
    save = args.Save
    files, reverse, forward = args.Fasta, args.Reverse, args.Forward

    for file in files:
        print(f'Analyzing {file}...')
        with open(file) as f:
            for values in SimpleFastaParser(f):
                defline, sequence = values[0:2]
                reverse_results = [(v.start(), v.end())
                                   for v in re.finditer(reverse, sequence)]
                forward_results = [(v.start(), v.end())
                                   for v in re.finditer(forward, sequence)]
                print(f'Searching in {defline}...\n')
                if len(reverse_results) > 0 and len(forward_results) > 0:
                    results = findClosestStrings(
                        forward_results, reverse_results, sequence, save)
                    if results:
                        output.setdefault(file, {})
                        output[file][defline] = results
    if save:
        writeResults(output, save)
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-f", "--Fasta",
                        help="Fasta files to parse (can be multiple)",
                        required=True, nargs='*')
    parser.add_argument("--Reverse",
                        help="Reverse primer",
                        required=True)
    parser.add_argument("--Forward",
                        help="Forward primer",
                        required=True)
    parser.add_argument("-s", "--Save",
                        help="Option to save the output to a file",
                        required=False, default=False)
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
