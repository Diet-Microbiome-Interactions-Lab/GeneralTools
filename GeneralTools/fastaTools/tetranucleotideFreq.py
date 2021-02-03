"""
Obtain tetranucleotide frequency for a
given string within a nucleotide sequnce

Example usage:
$ python tetranucleotideFreq.py 'MYSTRING'
"""
import sys


def main(sequence, sequenc2, kw=None):
    nuc = ["A", "T", "G", "C"]
    mer_list = []
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    mer = nuc[i] + nuc[j] + nuc[k] + nuc[l]
                    mer_list.append(mer)
    sequence = sequence.upper()
    length = len(sequence)
    freq_hash = {}
    for i in range(0, length - 3):
        mer = sequence[i:i + 4]
        if mer not in freq_hash:
            freq_hash[mer] = 0
        freq_hash[mer] = freq_hash[mer] + 1
    return freq_hash


if __name__ == "__main__":
    main(sys.argv[1])
