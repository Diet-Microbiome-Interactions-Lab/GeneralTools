import os
import sys
import csv

filelist = []
for file in os.listdir('MAG_Bin_Comparisons/'):
    if file.startswith('maxbin2') and file.endswith('fasta'):
        filelist.append(file)
filelist = sorted(filelist)
# print(filelist)

qlist = []
for q in os.listdir('MAG_Bin_Comparisons/'):
    if q.startswith('BT2_All'):
        qlist.append(q)
qlist = sorted(qlist)
# print(qlist)
# qlist = ['Index'] + qlist

os.chdir('MAG_Bin_Comparisons')


def create_bin_matrix(filelist, qlist):
    master_dictionary = {}
    for file in filelist:
        with open(file) as f:
            master_dictionary[file] = []
            fvals = []
            line = f.readline()
            nucleotides = ''
            while line:
                if line.startswith('>'):
                    fvals.append(nucleotides)
                    nucleotides = ''
                else:
                    nucleotides = nucleotides + line.strip()
                line = f.readline()
            fvals.append(nucleotides)
            fvals.remove('')
            # Open the query file
            for qfile in qlist:
                count = 0
                nocount = 0
                with open(qfile) as q:
                    qnucleotides = ''
                    line = q.readline()
                    while line:
                        if line.startswith('>'):
                            if qnucleotides != '' and qnucleotides in fvals:
                                count += 1
                            else:
                                nocount += 1
                            qnucleotides = ''
                        else:
                            qnucleotides = qnucleotides + line.strip()
                        line = q.readline()
                    if qnucleotides != '' and qnucleotides in fvals:
                        count += 1
                # After done reading file and creating list, add to dict
                    master_dictionary[file].append(count)
    return master_dictionary


def write_bin_similarity_matrix(filelist, qlist, savename):
    b_dict = create_bin_matrix(filelist, qlist)
    with open(savename, 'w', newline='') as mat:
        qlist = ['Index'] + qlist + ['\n']
        header = '\t'.join(qlist)
        mat.write(header)
        for key, val in b_dict.items():
            items = [key] + val + ['\n']
            newline = '\t'.join(str(item) for item in items)
            mat.write(newline)
    print('Finished!')
    return None

write_bin_similarity_matrix(filelist, qlist, 'testmatrix.txt')
