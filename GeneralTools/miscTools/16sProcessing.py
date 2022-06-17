import argparse
import pandas as pd
import re


def readMetadata(metadata):
    meta = {}
    df = pd.read_excel(metadata, dtype={'sample_id': str}).to_dict(
        orient='records')
    for dic in df:
        meta[dic['sample_id']] = [
            dic['Name'], dic['Batch'], dic['Gender'], dic['Substrate']
        ]
    return meta


def cleanTaxonomyString(value):
    levels_dic = {}
    levels = ['Kingdom', 'Phylum', 'Class',
              'Order', 'Family', 'Genus', 'Species']
    tax_string = re.sub("([\(\[]).*?([\)\]])", "", value)
    values = tax_string.split(';')
    levels_dic = dict(zip(levels, values))

    return levels_dic


def readTaxonomy(taxonomy):
    tax_dic = {}

    with open(taxonomy) as file:
        next(file)
        line = file.readline().strip()
        while line:
            values = line.split('\t')
            otu = values[0]
            tax_levels = cleanTaxonomyString(values[2])
            tax_dic[otu] = tax_levels
            line = file.readline().strip()
    return tax_dic


def readCount(countfile):
    count = {}
    with open(countfile) as file:
        line = file.readline().strip()
        values = line.split('\t')
        otus = [values[v] for v in list(range(3, len(values), 1))]

        line = file.readline().strip()
        while line:
            values = line.split('\t')
            group = values[1]
            counts = [values[v] for v in list(range(3, len(values), 1))]
            # cur_len_counts = len(counts)
            # assert len(counts) == 3875, 'Invalid count range.'
            count[group] = dict(zip(otus, counts))

            line = file.readline().strip()
    return count


def combineAllData(**kwargs):

    meta = readMetadata(kwargs['Metadata'])
    tax = readTaxonomy(kwargs['Taxonomy'])
    counts = readCount(kwargs['Subsample'])

    header = '\t'.join(['Group', 'OTU', 'Kingdom', 'Phylum', 'Class', 'Order',
                        'Family', 'Genus', 'Species', 'Sample', 'Substrate', 'ID', 'Count']) + '\n'
    with open(kwargs['Output'], 'w') as out:
        out.write(header)
        for group in counts:
            g_counts = counts[group]
            for otu in g_counts:
                t = tax[otu]
                cur_line = [group, otu, t['Kingdom'], t['Phylum'], t['Class'],
                            t['Order'], t['Family'], t['Genus'], t['Species']]
                cur_line.extend(meta[group])
                cur_line.append(g_counts[otu])
                writeline = '\t'.join(cur_line) + '\n'
                out.write(writeline)
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-m", "--Metadata",
                        help="Metadata file", required=True)
    parser.add_argument("-t", "--Taxonomy",
                        help="Taxonomy file", required=True)
    parser.add_argument("-s", "--Subsample",
                        help="Subsample file", required=True)
    parser.add_argument("-o", "--Output",
                        help="Output file", required=True)
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = vars(parser.parse_args())
    combineAllData(**args)
