# from Bio import SeqIO
# import sys
from BCBio import GFF

in_file = 'iFpraus_GCF_000162015.1_ASM16201v1_genomic.gff'


in_handle = open(in_file)
for rec in GFF.parse(in_handle):
    print(rec)
in_handle.close()


# def main(file, out):
#     with open(file) as f:
#         with open(out, 'w') as outfile:
#             for record in SeqIO.parse(f, 'genbank'):
#                 outfile.write(
#                     f'>{record.id} {record.description}\n{record.seq}\n')
#     return 0


# if __name__ == '__main__':
#     main(sys.argv[1], sys.argv[2])
