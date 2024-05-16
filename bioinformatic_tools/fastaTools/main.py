import argparse

from bioinformatic_tools.FileClasses.Fasta import Fasta

def main(args):
    input = args.Input
    output = args.Output
    print(f'Dealing with {input} and {output}')
    print(f'Adding to the class')
    mydata = Fasta(input)
    print(f'Class init successful')
    print(mydata.all_headers)
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
