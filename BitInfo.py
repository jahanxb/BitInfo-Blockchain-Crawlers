'''

'''
import io
import os

import requests
from bs4 import BeautifulSoup
from BlockChain import blockchainJsonExtractor
# import json
import simplejson
import re
from lxml import html
from lxml import etree

class MyCrawler:
    try:
        def __init__(self, walletId):
            r = requests.get('https://bitinfocharts.com/bitcoin/wallet/' + str(walletId)).text
            self.soup = BeautifulSoup(r, 'html.parser')

        def getBlocks(self):
            try:
                rows = self.soup.select('.trb.s_coins')
                blocksList = []
                for row in rows:
                    blocks_dict = {}
                    blocks_dict['time'] = row.contents[1].text
                    blocks_dict['amount'] = row.contents[2].text
                    blocks_dict['balance'] = row.contents[3].text
                    blocks_dict['balanceUSD'] = row.contents[4].text
                    try:
                        blocks_dict['block'] = row.contents[0].next.text
                    except Exception as e:
                        continue
                    blocksList.append(blocks_dict)
                return blocksList

            except:
                pass

        def getAddresses(self):
            try:
                span = self.soup.find('div', {'id': 'ShowAddresesContainer'})
                addresses = []
                tags = span.findAll('a', href=True)
                for i in tags:
                    addresses.append(i.getText())
                return addresses

            except Exception as e:
                pass

        def getBalances(self):
            try:
                table_1 = self.soup.find('table', {'class': 'table table-striped table-condensed'})
                # tr_table1 = table_1.findAll('tr')
                rows = table_1.select('tr')

                recievedDict = {}
                sendDict = {}
                unspentDict = {}
                balanceDict = {}
                balance = rows[0].text
                balance = balance.strip('Balance: ')
                balanceDict['BTC'] = balance.split("BTC")[0]
                balanceDict['USD'] = (balance.split("BTC")[1]).split('USD')[0]
                balanceDict['description'] = (balance.split("BTC")[1]).split('USD')[1]

                recievedDict['count'] = rows[1].select('td')[1].text.strip('count: ')
                recievedDict['first'] = rows[1].select('td')[2].text.strip('first: ')
                recievedDict['last'] = rows[1].select('td')[3].text.strip('last: ')

                sendDict['count'] = rows[2].select('td')[1].text.strip('count: ')
                sendDict['first'] = rows[2].select('td')[2].text.strip('first: ')
                sendDict['last'] = rows[2].select('td')[3].text.strip('last: ')

                unspentDict['count'] = rows[3].select('td')[1].text.strip('count: ')
            except:
                pass
            try:
                return {
                    "balance": balanceDict, "recieved": recievedDict, "send": sendDict, "unspent": unspentDict
                }
            except:
                pass

    except:
        pass



walletList = []
index=1
target=11
for i in range(index, target):
    try:
        print(i)
        tempDict = {"walletId": i}
        crawler = MyCrawler(i)
        tempDict["blocks"] = crawler.getBlocks()
        tempDict["addresses"] = crawler.getAddresses()
        blockchainJsonExtractor(tempDict["addresses"], i)
        balanceDict = crawler.getBalances()
        tempDict.update(balanceDict)
        walletList.append(tempDict)
        print(tempDict)
        print(walletList)
    except:
        pass

    #count += 1

try:
    jsr = simplejson.dumps(walletList, iterable_as_array=True)
    name = 'walletId_' + str(index) + "_" + str(target - 1)
    with io.open(f'{name}.json', 'a+', encoding='utf8') as data_file:
        data_file.write(jsr)
    os.rename(f'{name}.json', "BitInfoData/"f'{name}.json')
except:
    pass

#



i=1
#54799999
