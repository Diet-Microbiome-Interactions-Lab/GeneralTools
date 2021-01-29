#!/Users/ddeemer/.pyenv/versions/3.9.0/bin/python

print('In the module')


def main():
    print('Script run as __main__')


import sys

print(sys.path)

if __name__ == '__main__':
    main()

import glob
a = [script for script in glob.glob('GT_Bin/*.py')]
print(a)
