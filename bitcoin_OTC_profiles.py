
import lxml
import requests
from bs4 import BeautifulSoup
import pandas as pd

# import json
# from lxml import html
import urllib


def check_string_bool(value):

        temp = False
        if str(value) == '<img src="/Resources/red_cross.png" style="width:16px;height:16px"/>':
            temp = False
        elif str(value) == '<img src="/Resources/green_tick.png" style="width:16px;height:16px"/>':
            temp = True
        return temp


def get_addr_tags(offset,end_of_table_pagination):

        try:
            url = 'https://www.blockchain.com/btc/tags?filter=4'
            #r = requests.get(url + '&offset=' + str(offset))
            #soup = BeautifulSoup(r.text, 'lxml')
            try:
                #table = soup.find('table', {'class': 'table table-striped'})

                # page = urllib3.urlopen(url)
                page = urllib.request.urlopen(url + '&offset=' + str(offset))
                soup_1 = BeautifulSoup(page, 'lxml')
                icon_link = soup_1.find("table", {'class': 'table table-striped'})
                icon = icon_link.findAll('img')
                verified =[]
                for i in icon:
                    if str(i) == '<img src="/Resources/red_cross.png" style="width:16px;height:16px"/>':
                        temp = False
                        verified.append(temp)
                    elif str(i) == '<img src="/Resources/green_tick.png" style="width:16px;height:16px"/>':
                        temp = True
                        verified.append(temp)

                addr_verified = []

                df = pd.read_html(str(icon_link))[0]

                df['Verified'] = verified

                # print(df)

            except EnvironmentError as e:
                print(e)
        except ConnectionError as e:
            print(e)
        return df


end_of_table_pagination = 4650   #3650
offset = 0
results = {}
for offset in range(offset, end_of_table_pagination, 50):
        df =get_addr_tags(offset,end_of_table_pagination)
        with open('bitcoin_OTC_profiles/'+str(offset) + 'to' + str(end_of_table_pagination) + '.csv', 'a') as f:
            if offset == 0:
                df.to_csv(f, line_terminator='\n', index=False, header=True)
            else:
                df.to_csv(f, line_terminator='\n', index=False, header=False)

