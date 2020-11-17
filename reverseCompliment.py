'''
Finding the reverse compliment and printing to stdout
'''
import time
import sys


def compliments(nucleotide):
    dic = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return dic.get(nucleotide, 'N')


def rev(string):
    if len(string) == 0:
        return ''
    else:
        letter = string[-1].upper()   # Grab the last letter
        compliment = compliments(letter)  # Find the compliment
        string = string[:-1]               # Remove last letter
        return (compliment + rev(string))


if __name__ == '__main__':
    # start_time = time.time()
    print(rev(sys.argv[1]))
    # print(f"--- {time.time() - start_time} seconds ---")
