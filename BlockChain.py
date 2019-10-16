import os
import shutil
import urllib.request, json, io
import http


def blockchainJsonExtractor(addresses,wallet_Index):
    try:
        for address in addresses:
            with urllib.request.urlopen("https://blockchain.info/rawaddr/" + address) as url:
                try:
                    data = json.loads(url.read().decode())
                    print(type(data))
                    data.update({"walletId": str(wallet_Index)})
                    jsr = json.dumps(data)
                    # jsr.add(data1)
                    print(jsr)
                    name = 'walletId_' + str(wallet_Index) + '_AD_' + address
                    with io.open(f'{name}.json', 'w', encoding='utf8') as data_file:
                        data_file.write(jsr)
                    os.rename(f'{name}.json', "BlockchainData/"f'{name}.json')
                except(http.client.IncompleteRead) as e:
                    url = e.partial
    except:
        pass
