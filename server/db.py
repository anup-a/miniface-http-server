import sqlite3
import os
import json

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
            "create table if not exists accounts('user_id' integer primary key autoincrement, 'Name' varchar(100) not null, 'user_name' varchar(20) UNIQUE, 'password' varchar(20) not null)")
        con.commit()
        con = sqlite3.connect('server/db/accounts.db')
        cur = con.cursor()
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('Anup Aglawe', 'anup_22', 'hianup'))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('A', 'A', 'hianup'))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('B', 'B', 'hianup'))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('C', 'C', 'hianup'))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('D', 'D', 'hianup'))
        
        con.commit()
    return "success"

def db_init3():
    if(os.path.exists("server/db/friendship.db")):
        db = ''
    else:
        con = sqlite3.connect('server/db/friendship.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists friendship('user_id1' integer not null,'user_id2' integer not null, 'status' varchar(100) not null, PRIMARY KEY(user_id1,user_id2))")
        con.commit()
        con = sqlite3.connect('server/db/friendship.db')
        cur = con.cursor()
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (1, 2,"pending"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (3, 4,"friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (4, 3,"friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (2, 3,"friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (3, 2,"friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (5, 3,"friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (3, 5,"friends"))
        con.commit()
    return "success for friends"



# initialize JSON DATABASE
db_f = open('server/db/data.json')
database = json.load(db_f)

# initialize SQLITE DATABASE
db_init()
db_init2()
db_init3()