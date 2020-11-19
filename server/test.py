import sqlite3
con = sqlite3.connect('server/db/accounts.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("select * from accounts")
c = cur.fetchall()

posts = []
for t in c:
    x = dict(t)
    posts.append(x)
print(posts)