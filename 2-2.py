import json
import requests
with open('daemon.json', mode='r') as f:
    res = json.load(f)
    host = res['host']
    port = res['port']
    deals = res['deals']

import json
import requests
with open('daemon.json', mode='r') as f:
    res = json.load(f)
    host = res['host']
    port = res['port']
    deals = res['deals']


a = requests.get('http://' + str(host) + ':' + str(port))
spisok = []
if a:
    data = a.json()
    for i in data:
        slova = i['job'].split()
        for j in deals:
            if j.split()[0] in slova[0]:
                b = i['being'] + ': ' + j
                spisok.append(b)
spisok.sort()
for i in spisok:
    print(i)
