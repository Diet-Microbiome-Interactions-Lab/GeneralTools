import argparse

import pandas as pd


def color_boolean(val):
    color = ''
    if val is True:
        color = 'green'
    elif val is False:
        color = 'red'
    else:
        color = None
    return 'background-color: %s' % color


def compare_modules(file, genomes, output):
    raw = pd.read_csv(file, delimiter='\t')
    raw = raw.loc[raw['db_name'].isin(genomes)]
    df = raw.iloc[:, [2, 3, 4, 6, 7, 9, 10]]
    all_mods = raw.iloc[:, [3, 4, 6, 7]].drop_duplicates(
        'kegg_module').set_index('kegg_module')
    for genome in genomes:
        tmp_df = df.loc[df['db_name'] == genome].set_index('kegg_module')
        tmp_df = tmp_df.iloc[:, [1, 2, 3, 4, 5]]
        tmp_df.columns = [
            'module_category', 'module_category',
            'module_subcategory', f'{genome}-Comp', f'{genome}-Bool'
        ]
        all_mods = pd.concat([all_mods, tmp_df], axis=1)

    res = all_mods.loc[:, ~all_mods.columns.duplicated()]
    res.style.\
        applymap(color_boolean).to_excel(output)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Default Parser")
    parser.add_argument("-i", "--input", help="Input Kegg Module file",
                        default='kegg-metabolism_modules.txt')
    parser.add_argument(
        "-o", "--output", help="Output (xlsx) file to write to")
    parser.add_argument("-g", "--genomes",
                        help="List of genomes to subset and analyze",
                        nargs="+")
    args = parser.parse_args()
    compare_modules(args.input, args.genomes, args.output)
