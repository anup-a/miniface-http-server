import sqlite3
from body_parser import body_parser
from os.path import join
from helpers import *
from response import *


def add_post(post_id, post_body, user_id):
    con = sqlite3.connect('server/db/posts.db')
    cur = con.cursor()
    cur.execute("insert into posts(post_id, post_body, user_id) values(?,?,?)",
                (post_id, post_body, user_id))
    con.commit()
    return "success"

    # parsedText = body_parser(body)
    # database["feed"].append(parsedText["name"])

    # with open('server/db/data.json', 'w') as f:
    #     json.dump(database, f)

# legacy method


# def populate_data(template):
#     file_data = template.render(
#         {'feed': database["feed"]}, loader=loader).encode('utf-8')

#     return file_data


def login(user_name, password):
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from accounts where user_name=?", (user_name,))

    c = cur.fetchone()
    if c:
        if c[3] == password:
            return((1, c[0]))
        else:
            return((0, 'The password was wrong.'))
    else:
        return((0, 'The username does not exist.'))

def signup(name, user_name, password):
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                        (name, user_name, password))
        con.commit()
        cur.execute("select * from accounts where user_name=?", (user_name,))
        c = cur.fetchone()
        return(1, c[0])
    except Exception as e:
        con.commit()
        return(0, e)

def handleDBPushAPI(res_sock, req_uri, body):
    if req_uri == '/addpost.html' or req_uri == 'addpost.html':
        print("Adding to SQLite Database.....")
        add_post('2', body["name"], '1')
        print("Done. Added")
        handle_redirect(res_sock)
        
    if req_uri=='/login_page.html' or req_uri == 'login_page.html':
        print(body)
        res = login(body['username'], body['password'])
        if res[0]:
            print("authenticated.")
            handle_redirect(res_sock, user_id=res[1])
        else:
            print(res[1])
            handle_redirect(res_sock)
    
    if req_uri=='/signup_page.html' or req_uri == 'signup_page.html':
        res = signup(body['name'], body['username'], body['password'])
        if res[0]:
            print("User inserted")
            handle_redirect(res_sock, user_id=res[1])
        else:
            print(res[1])
            handle_redirect(res_sock)


def addtoDB(res_sock, req_uri, body):
    parsedText = body_parser(body)
    handleDBPushAPI(res_sock, req_uri, parsedText)
