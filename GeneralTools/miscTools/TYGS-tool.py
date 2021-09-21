'''
'''
import os
import mailparser
import pandas as pd


os.chdir('/Users/ddeemer/OneDrive - purdue.edu/Projects/AshProject/Summer21Analyses/TypeStrains-01Jun21/EmailParsing/')


def parse_email(body):
    '''
    '''
    link = ''.join([val for val in body if val.startswith('<a href')])
    mylink = link.split('href="')[1].split('</a>')[0]
    mylink = mylink.split('">https:')[0]

    return mylink


def parse_emails(directory):
    '''
    '''
    cnt = 0
    no_cnt = 0
    links = []
    for root, dirs, files in os.walk(directory):
        mail_list = [os.path.join(root, val) for val in files]

    for mail in mail_list:
        m = mailparser.parse_from_file(mail)
        body = m.body.split('\n')
        myflag = ''.join(
            [val for val in body if val.startswith('new results')])
        if myflag:
            cnt += 1
            links.append(parse_email(body))
        else:
            no_cnt += 1
    return links


def get_tygs_information(directory):
    '''
    '''
    hit = 0

    column_names = ['Query_strain', 'Subject_strain', 'dDDH_d0',
                    'CI_d0', 'dDDH_d4', 'CI_d4', 'dDDH_d6',
                    'CI_d6', 'GC_content_difference']
    table3_out = pd.DataFrame(columns=column_names)
    columns_names2 = [
        'TYGS ID', 'Kind', 'Species cluster', 'Subspecies cluster',
        'Preferred name', 'Deposit', 'Authority', 'Other deposits',
        'Synonymous taxon names', 'Base pairs', 'Percent G+C', 'No. proteins',
        'Goldstamp', 'Bioproject accession', 'Biosample accession',
        'Assembly accession', 'IMG OID', 'BacDive'
    ]
    table4_out = pd.DataFrame(columns=columns_names2)

    for link in parse_emails(directory):
        print(link)
        mytables = pd.read_html(link)

        for table in mytables:
            if table.columns[0] == 'Query strain':
                hit += 1
                table3 = table
            if table.columns[0] == 'TYGS ID':
                table4 = table

        # Process table 3
        table3.columns = column_names
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

    table3_out.to_excel('Table3-23Jun21-DGD.xlsx')
    table4_out.to_excel('Table4-23Jun21-DGD.xlsx')

    return None


# get_tygs_information('Emails/')


# Next part, go through the list of Assembly accessions and download the
# assemblies
