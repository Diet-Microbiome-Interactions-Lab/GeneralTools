'''
'''
import argparse
import os

import mailparser
import pandas as pd


def parse_email(body):
    '''
    '''
    link = ''.join([val for val in body if val.startswith('<a href')])
    try:
        mylink = link.split('href="')[1].split('</a>')[0]
        mylink = mylink.split('">https:')[0]
    except IndexError:
        return None

    return mylink


def parse_emails(directory):
    '''
    '''
    cnt = 0
    no_cnt = 0
    links = []
    for root, dirs, files in os.walk(directory):
        mail_list = [os.path.join(root, val)
                     for val in files if val.endswith('.eml')]

    total = len(mail_list)
    for cnt, mail in enumerate(mail_list):
        print(f'Reading in file ({cnt + 1} / {total}): {mail}')
        m = mailparser.parse_from_file(mail)
        body = m.body.split('\n')
        myflag = ''.join(
            [val for val in body if val.startswith('new results')])
        if myflag:
            cnt += 1
            current_link = parse_email(body)
            if current_link:
                links.append(parse_email(body))
            else:
                print(f'The file: {mail} did not have a link in it.')
        else:
            no_cnt += 1
    return links


def main(args):
    directory = args.Directory
    out_prefix = args.Output
    hit = 0

    column_names_t3 = ['Query_strain', 'Subject_strain', 'dDDH_d0',
                       'CI_d0', 'dDDH_d4', 'CI_d4', 'dDDH_d6',
                       'CI_d6', 'GC_content_difference']
    columns_names_t4 = [
        'TYGS ID', 'Kind', 'Species cluster', 'Subspecies cluster',
        'Preferred name', 'Deposit', 'Authority', 'Other deposits',
        'Synonymous taxon names', 'Base pairs', 'Percent G+C', 'No. proteins',
        'Goldstamp', 'Bioproject accession', 'Biosample accession',
        'Assembly accession', 'IMG OID', 'BacDive'
    ]

    table3_out = pd.DataFrame(columns=column_names_t3)
    table4_out = pd.DataFrame(columns=columns_names_t4)

    links = parse_emails(directory)
    print(f'\nAmalgamating all emails into 2 excel sheets.\n')
    total = len(links)
    for cnt, link in enumerate(links):
        print(f'Analzing in file ({cnt + 1} / {total}): {link}')
        mytables = pd.read_html(link)

        for table in mytables:
            if table.columns[0] == 'Query strain':
                hit += 1
                table3 = table
            if table.columns[0] == 'TYGS ID':
                table4 = table

        # Process table 3
        table3.columns = column_names_t3
        tmp = table3.sort_values('dDDH_d4').drop_duplicates(
            ["Query_strain"], keep="last")
        # Grab subject strains from table 3
        tmp_strains = tmp['Subject_strain'].tolist()
        table3_out = table3_out.append(tmp)

        # Process table 4
        tmp_names = table4['Preferred name'].tolist()
        matches = [name for name in tmp_names if any(
            name in val for val in tmp_strains)]
        tmp2 = table4[table4['Preferred name'].isin(matches)]
        table4_out = table4_out.append(tmp2)

    table3_out.to_excel(f'{out_prefix}_Table3.xlsx')
    table4_out.to_excel(f'{out_prefix}_Table4.xlsx')

    return None


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-d", "--Directory",
                        help="Directory where .eml files live", required=True)
    parser.add_argument("-o", "--Output",
                        help="Prefix for the output files (2 total)", required=True)
    # TODO: Add an output location?
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    main(args)
