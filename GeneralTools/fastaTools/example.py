import argparse

from GeneralTools.FileClasses import Fasta

def main(args):
    files = args.Input
    output = args.Output
    print(f'Dealing with {files} and {output}')
    return 0

def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-i", "--Input",
                        help="Fasta files to parse (can be multiple)",
                        required=True)
    # parser.add_argument("-i", "--Input",
    #                     help="Fasta files to parse (can be multiple)",
    #                     required=True, nargs='*')
    parser.add_argument("-o", "--Output",
                        help="Output file to write to",
                        required=False)
    return parser




if __name__ == "__main__":
    print('Running in main!!!')
    parser = parse_args()
    args = parser.parse_args()
    print(args)
    main(args)