import json
spisok = []
res = open('lubbocks.json', mode='w')
with open('guests.csv', mode='r') as f:
    a = f.readlines()
    count = 1
    for i in a:
        if count == 1:
            count += 1
            continue
        b = i.split(';')
        if 'lilac' in b[3]:
            dict = {f'name': b[1],
                    'title': b[2],
                    'eye_color': b[3]
            }
            spisok.append(dict)
json.dump(spisok, res)