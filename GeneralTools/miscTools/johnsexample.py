"""
Created on Fri Nov  5 13:47:20 2021

@author: hunte
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import datetime as dt


def scrape_fly(date=''):
    payload = {'username': 'jbodzick', 'password': 'purple55'}
    login_url = 'https://thefly.com'
    data_url = 'https://thefly.com/syndicate.php' + '?fecha=' + date

    with requests.Session() as s:
        log = s.post(login_url, data=payload, headers={
                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        # time.sleep(3)
        page = s.get(data_url, headers={
                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'})

    soup = BeautifulSoup(page.text, 'html.parser')
    dates = soup.find_all('header', {'class': 'calendar_time_syn'})
    date_entries = [dates[x].find_next_siblings(
        'ul', {'class': 'synItems'}) for x in range(len(dates))]
    unique_dates = [d.text for d in dates]

    # prettify each element of date entries to get the html for that date
    pretty_by_date = [date_entries[x][0].prettify() for x in range(
        len(date_entries)) if len(date_entries[x]) > 0]

    # parse the HTML and match it with the dates, then fill the df
    html_by_date = [BeautifulSoup(x, 'html.parser') for x in pretty_by_date]
    date_and_html = dict(zip(unique_dates, html_by_date))

    # fill dfs
    dfs = []
    elements = {'synSymbolItem': 'div', 'issuerItemDesc': 'div', 'synTypeItem': 'span',
                'price': 'span', 'synShares': 'span', 'list': 'span', 'periodTimeDesc': 'div'}

    for day in date_and_html:
        df = {}

        for col in elements:
            rows = [x.text for x in date_and_html[day].find_all(
                elements[col], {'class': col})]
            df[col] = rows

        df = pd.DataFrame(df).rename(columns={'synSymbolItem': 'Symbol', 'issuerItemDesc': 'Issuer', 'synTypeItem': 'Type',
                                              'synShares': 'Syndicate Shares', 'list': 'Managers old', 'periodTimeDesc': 'Time', 'tablaDetalles': 'Managers'})
        df['Date'] = [day] * len(df)
        dfs.append(df)

    df = pd.DataFrame().append(dfs)
    if len(df) == 0:
        return None
    # drop duplicated tickers
    if 'Date' in df.columns:
        df['duped'] = ['-' not in x for x in df['Date']]
        df = df[df['duped'] == False].drop(columns=['duped'])
    # clear extra whitespace
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df


s_date = dt.date(2018, 6, 1)  # first day to pass,
e_date = dt.date(2022, 7, 21)  # last day to pass


def scrape_period(s_date, e_date):
    # get all dates to pass to fly
    days = [s_date.strftime('%Y-%m-%d')]
    while s_date < e_date:  # dt.date.today()-dt.timedelta(days=7):
        s_date += dt.timedelta(days=7)
        days.append(s_date.strftime('%Y-%m-%d'))

    df = pd.DataFrame()
    for day in days:
        print(day)
        t_df = scrape_fly(date=day)
        if t_df is not None:
            t_df['Year'] = '/' + \
                str(dt.datetime.strptime(day, '%Y-%m-%d').year)
            df = df.append(t_df)
    # final date cleaning
    df['Deal Date'] = [x.split(' - ')[0] for x in df['Date']]
    df['Deal Date'] = pd.to_datetime(df['Deal Date'] + df['Year'])
    df = df.reset_index().drop(columns=['Date', 'Year', 'index'])
    return df
