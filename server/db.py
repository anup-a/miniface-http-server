import sqlite3
import os
import json
from body_parser import body_parser


def db_init():
    if(os.path.exists("server/db/posts.db")):
        db = ''
    else:
        con = sqlite3.connect('server/db/posts.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists posts('post_id' varchar(20) not null, 'post_body' varchar(5000) not null, 'user_id' varchar(20) not null)")
        con.commit()
        con = sqlite3.connect('server/db/posts.db')
        cur = con.cursor()
        cur.execute("insert into posts(post_id, post_body, user_id) values(?,?,?)",
                    ('1', 'Chilling at Beach with 5 Others. At Louisiana', '1'))
        con.commit()
    return "success"

def db_init2():
    if(os.path.exists("server/db/accounts.db")):
        db = ''
    else:
        con = sqlite3.connect('server/db/accounts.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists accounts('user_id' varchar(20) not null, 'user_name' varchar(20) not null, 'password' varchar(20) not null)")
        con.commit()
        con = sqlite3.connect('server/db/accounts.db')
        cur = con.cursor()
        cur.execute("insert into accounts(user_id, user_name, password) values(?,?,?)",
                    ('1', 'anup_22', 'hianup'))
        con.commit()
    return "success"

# initialize JSON DATABASE
db_f = open('server/db/data.json')
database = json.load(db_f)

# initialize SQLITE DATABASE
db_init()
db_init2()