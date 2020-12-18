''' Program to parse a .SAM file and filter it for a user-defined
percent identity '''

import sys


def blocks(file, size=65536):
    while True:
        b = file.read(size)
        if not b:
            break
        yield b


with open(sys.argv[1], "r", encoding="utf-8", errors='ignore') as f:
    print(sum(bl.count(">") for bl in blocks(f)))
