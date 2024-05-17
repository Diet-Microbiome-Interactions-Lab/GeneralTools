import os
# import sys
os.chdir('/Users/ddeemer/OneDrive - purdue.edu/AshProject/Spring21-Analyses/Abundance-Bin-Coding')
print(os.listdir())


def read_abund(file):
    '''
    '''
    abundance_dic = {}
    with open(file) as f:
        header = f.readline().strip().split('\t')
        line = f.readline().strip()
        while line:
            values = line.split('\t')
            abundance_dic[values[0]] = values[1:]
            line = f.readline().strip()
    # print(abundance_dic)
    return abundance_dic


def main(ani, file1):
    '''
    Given a merged covered file, i.e. one that contains all coverage
    values for all samples for all bins (supernatant and particle)
    together, 
    '''
    removed = []

    prev_mag = None

    a = read_abund(file1)
    all_bins = list(a.keys())
    print(len(all_bins))

    with open(ani) as file:
        header = file.readline()
        line = file.readline().strip()
        while line:
            values = line.split('\t')
            ref = f"p-{values[1].split('Bin.')[1].strip('.fasta')}"
            quer = f"s-{values[0].split('Bin.')[1].split('.fast')[0]}"
            ani = float(values[2])
            mappings = int(values[3])
            if ani > 98.0:
                if not ref == prev_mag:
                    removed.append(f"{quer}_{ref}")
                    all_bins.remove(quer)
                    print(f"Removing {quer}")
                    all_bins.remove(ref)
                    all_bins.append(f"{ref}-MERGED")
                    # Now re-normalize the read count
                    norm_counts = []
                    for sup, par in zip(a[quer], a[ref]):
                        mu = (float(sup) + float(par)) / 2
                        norm_counts.append(mu)
                    del a[quer]
                    del a[ref]
                    new_key = f"{ref}-MERGED"
                    a[new_key] = norm_counts
                else:
                    pass
            prev_mag = ref
            line = file.readline().strip()

    return all_bins, removed, a


all_bins, removed, a = main(
    'AllAniResults.txt', 'Cov-Both.txt')
print(len(all_bins))
print(all_bins)
# print(len(all_bins))
# print('Total removed:')
# print(len(removed))
# print(len(a))
# cnt = 0
# nocnt = 0
# cnt2 = 0


def write_merged_file(indict, output):
    with open(output, 'w') as out:
        for mag in indict.keys():
            writeline = [mag] + indict[mag] + ['\n']
            print(writeline)
            out.write('\t'.join([str(val) for val in writeline]))


write_merged_file(a, 'Cov-Both-Mean.txt')
# mylist = [1, 2, 3, 4, 5]

# print(sum(mylist))
