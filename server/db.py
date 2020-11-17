import sqlite3
import os
import json
from body_parser import body_parser


db_f = open('server/db/data.json')
database = json.load(db_f)


def db_init():
    if(os.path.exists("server/db/post.db")):
        db = ''
    else:
        con = sqlite3.connect('server/db/post.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists posts('post_id' varchar(20) not null, 'post_body' varchar(5000) not null, 'user_id' varchar(20) not null)")
        con.commit()
        con = sqlite3.connect('server/db/post.db')
        cur = con.cursor()
        cur.execute("insert into posts(post_id, post_body, user_id) values(?,?,?,?)",
                    ('1', 'Chilling at Beach with 5 Others. At Louisiana', '1'))
        con.commit()
    return "success"


def update_to_db(body):
    parsedText = body_parser(body)
    database["feed"].append(parsedText["name"])

    with open('server/db/data.json', 'w') as f:
        json.dump(database, f)
