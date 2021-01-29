#!/Users/ddeemer/.pyenv/versions/3.9.0/bin/python

import GeneralTools
import GeneralTools.fastaTools.tetranucleotideFreq as tnf

print('In the import!')
seq = 'AGATCGCTGAC'
tetra = tnf.tetranucleotide_freq(seq)
print(tetra)


if __name__ == '__main__':
    print('In the main')
    print(tetra)
