import sqlite3
import os
import json
from persistqueue import sqlqueue
from argon2 import PasswordHasher

ph = PasswordHasher()

# def queue_init():
#     # cdir = os.getcwd()
#     # path = os.path.join(cdir, '/server/db/')
#     onlineQueue = sqlqueue.UniqueQ('server/db', auto_commit="true")
#     return onlineQueue

def posts_db_create():
    if(os.path.exists("server/db/posts.db")):
        db = ''
    else:
        con = sqlite3.connect('server/db/posts.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists posts('post_id' integer primary key autoincrement, 'post_body' varchar(5000) not null, 'user_id' varchar(20) not null)")
        con.commit()
        con = sqlite3.connect('server/db/posts.db')
        cur = con.cursor()
        cur.execute("insert into posts(post_body, user_id) values(?,?)",
                    ('Chilling at Beach with 5 Others. At Louisiana', '1'))
        cur.execute("insert into posts(post_body, user_id) values(?,?)",
                    ('At the restaurant.', '2'))
        cur.execute("insert into posts( post_body, user_id) values(?,?)",
                    ('Hacking NASA with HTML, and 3 others. ', '3'))
        cur.execute("insert into posts( post_body, user_id) values(?,?)",
            ('Be kind to unkind people they need it the post. ', '4'))
        cur.execute("insert into posts( post_body, user_id) values(?,?)",
            ('At the Facebook company, we are constantly iterating, solving problems and working together to connect people all over the world', '5'))
        con.commit()
    return "success"


def accounts_db_create():
    if(os.path.exists("server/db/accounts.db")):
        db = ''
    else:
        con = sqlite3.connect('server/db/accounts.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists accounts('user_id' integer primary key autoincrement, 'Name' varchar(100) not null, 'user_name' varchar(20) UNIQUE, 'password' varchar(100) not null)")
        con.commit()
        con = sqlite3.connect('server/db/accounts.db')
        cur = con.cursor()
        hashedPassword = ph.hash('hianup')
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('Anup Aglawe', 'anup_22', hashedPassword))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('A', 'A', hashedPassword))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('B', 'B', hashedPassword))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('C', 'C', hashedPassword))
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    ('D', 'D', hashedPassword))

        con.commit()
    return "success"


def friends_db_create():
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
                    (1, 2, "pending"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (3, 4, "friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (4, 3, "friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (2, 3, "friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (3, 2, "friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (5, 3, "friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (3, 5, "friends"))
        con.commit()
    return "success for friends"


def online_peers_db_create():

    if(os.path.exists("server/db/online_peers.db")):
        db = ''
    else:
        con = sqlite3.connect('server/db/online_peers.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists online_peers('user_id' integer primary key, 'ip' varchar(100), 'port' varchar(7))")
        
        con.commit()

        # con = sqlite3.connect('server/db/online_peers.db')
        # cur = con.cursor()
        # user_name="default"
        # cur.execute("insert into online_peers(user_name) values(?)",
        #         (user_name,))
        # con.commit()

    return "success"


def initialize_db():

    accounts_db_create()

    posts_db_create()
    
    friends_db_create()

    online_peers_db_create()


# LEGACY::initialize JSON DATABASE
# db_f = open('server/db/data.json')
# database = json.load(db_f)

# initialize SQLITE DATABASE
initialize_db()

# # Queue initialization for online users
# onlineQueue = queue_init()
