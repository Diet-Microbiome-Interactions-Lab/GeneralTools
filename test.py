# import argparse
# import sys


# def parse_args():
#     parser = argparse.ArgumentParser(description="ArgParser")
#     parser.add_argument("-i", "--input", help="My input file",
#                         required=True)
#     parser.add_argument("-o", "--output", help="My output file",
#                         required=False)
#     return parser


# def main(myin, myout):
#     print('Running main...')
#     print(f"{myin}\t{myout}")


# if __name__ == "__main__":
#     parser = parse_args()
#     print(f"Parser: {parser}")
#     args = parser.parse_args()
#     print(f"Args: {args}")


import memory_profiler
for val in dir(memory_profiler):
    if not val.startswith('__'):
        print(val)
