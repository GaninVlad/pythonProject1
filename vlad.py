import sqlite3
con = sqlite3.connect('native.db')
cur = con.cursor()
spisok_chisel = []
spisok = []
str = input()
for i in str:
    b = f"SELECT how_far, place FROM Places WHERE location LIKE '{i}'"
    res = cur.execute(b).fetchall()
    for i in res:
        spisok.append(i)
a = sorted(spisok, key=lambda x: (x[0], x), reverse=True)
for i in a:
    print(i[1])
con.close()

