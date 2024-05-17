'''
Script to parse an outlook email and grab all of them
sent by a specific name
'''
import os

import mailparser
import pandas as pd

os.chdir('/Users/ddeemer/OneDrive - purdue.edu/Projects/AshProject/Summer21Analyses/TypeStrains-01Jun21/EmailParsing/')
d = '/Users/ddeemer/OneDrive - purdue.edu/Projects/AshProject/Summer21Analyses/TypeStrains-01Jun21/EmailParsing/Emails'


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
    out_table = pd.DataFrame(columns=column_names)

    for link in parse_emails(directory):
        print(link)
        mytables = pd.read_html(link)

        for table in mytables:
            if table.columns[0] == 'Query strain':
                hit += 1
                mytable = table
        mytable.columns = column_names
        tmp = mytable.sort_values('dDDH_d4').drop_duplicates(
            ["Query_strain"], keep="last")
        out_table = out_table.append(tmp)
    out_table.to_excel('test1.xlsx')


get_tygs_information(d)
