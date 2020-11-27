import sqlite3
from body_parser import body_parser
from os.path import join
from helpers import *
from response import *
from argon2 import PasswordHasher
from db import onlineQueue
import jwt

ph = PasswordHasher()


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


def genAccessToken(user):
    username = user[2]
    token = jwt.encode({'username': username},
                       'MINI_SECRET', algorithm='HS256')
    return token


def login(user_name, password):
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from accounts where user_name=?", (user_name,))

    c = cur.fetchone()
    if c:
        try:
            if ph.verify(c[3], password):
                print("password verified")
                accessToken = genAccessToken(c)
                return((1, c[0], accessToken))
            else:
                return((0, 'The password was wrong.'))
        except:
            return((0, 'The password was wrong.'))
    else:
        return((0, 'The username does not exist.'))


def signup(name, user_name, password):
    hashedPassword = ph.hash(password)
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("insert into accounts(Name, user_name, password) values(?,?,?)",
                    (name, user_name, hashedPassword))
        con.commit()
        cur.execute("select * from accounts where user_name=?", (user_name,))
        c = cur.fetchone()
        return(1, c[0])
    except Exception as e:
        con.commit()
        return(0, e)
def add_friend(user_id,friend_user_id):
    friend_user_id=int(friend_user_id)
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row


    cur = con.cursor()
    print("Reached in add_friends")
    cur.execute('select user_id2 from friendship where user_id1=? and status="friends"',(user_id,))
    c = cur.fetchall()
    friends = []
    for friend in c:
        dic = dict(friend)
        friends.append(dic)
    if friend_user_id in friends:
        print("Already friends")
        return 2


    cur = con.cursor()
    cur.execute('select user_id2 from friendship where user_id1=? and status="pending"',(user_id,))
    c = cur.fetchall()
    pending = []
    for friend in c:
        dic = dict(friend)
        pending.append(dic)
    if friend_user_id in pending:
        print("ALready sent request")
        return 1


    cur = con.cursor()
    cur.execute('select user_id1 from friendship where user_id2=? and status="pending"',(user_id,))
    c = cur.fetchall()
    reverse_pending = []
    for friend in c:
        dic = dict(friend)
        reverse_pending.append(dic)
    if friend_user_id in reverse_pending:
        print("Accept pending request")
        cur = con.cursor()
        cur.execute("delete from friendship where user_id1=? and user_id2=? and status=?",
                        (friend_user_id,user_id,"pending"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                        (user_id,friend_user_id,"friends"))
        cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                        (friend_user_id,user_id,"friends"))
        con.commit()
        return 3

    cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                        (user_id,friend_user_id,"pending"))
    print("Request Sent")
    con.commit()
    return 0
def unfriend(user_id,friend_user_id):
    friend_user_id=int(friend_user_id)
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    print("Reached in add_friends")
    cur.execute("delete from friendship where user_id1=? and user_id2=? and status=?",
                (friend_user_id,user_id,"friends"))
    cur.execute("delete from friendship where user_id1=? and user_id2=? and status=?",
                (user_id,friend_user_id,"friends"))


def handleDBPushAPI(res_sock, req_uri, body):
    if req_uri == '/addpost.html' or req_uri == 'addpost.html':
        print("Adding to SQLite Database.....")
        add_post('2', body["name"], '1')
        print("Done. Added")
        handle_redirect(res_sock)

    if req_uri == '/login_page.html' or req_uri == 'login_page.html':
        res = login(body['username'], body['password'])
        if res[0] == 1:
            print("authenticated.")
            token = res[2]
            handle_redirect(
                res_sock=res_sock, user_id=res[1], token=token, req_uri="index.html")
        else:
            print(res[1])
            handle_redirect(res_sock, req_uri="login_page.html")

    if req_uri == '/signup_page.html' or req_uri == 'signup_page.html':
        res = signup(body['name'], body['username'], body['password'])
        if res[0]:
            print("User inserted")
            handle_redirect(res_sock, user_id=res[1])
        else:
            print(res[1])
            handle_redirect(res_sock)

    if req_uri=='/add_friends.html' or req_uri == 'add_friends.html':
        print(body)
        user_id=3
        res = add_friend(user_id,body['user_id'])
        # if res[0]:
        #     print("authenticated.")
        #     handle_redirect(res_sock, user_id=res[1])
        # else:
        #     print(res[1])
        handle_redirect(res_sock,req_uri="add_friends.html")


def getPostsForUser(user_id):
    friends = get_friends(user_id)

    con = sqlite3.connect('server/db/posts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from posts where user_name in ?", ( friends,))

    c = cur.fetchall()

    posts = []
    for t in c:
        x = dict(t)
        posts.append(x)
    return posts


def addtoDB(res_sock, req_uri, body):
    parsedText = body_parser(body)
    handleDBPushAPI(res_sock, req_uri, parsedText)


# def setOnline(user_id):
#     onlineQueue.put(user_id)


# def resetOnlineUsers():

#     def deleteLastUser():
#         if onlineQueue.size >= 1:
#             onlineQueue.get()

#     # Delete users every 10 sec
#     set_interval(deleteLastUser, 10)


# resetOnlineUsers()

# setOnline('1')
# setOnline('3')

# def get_online_users():
#     con = sqlite3.connect('server/db/data.db')
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select data from unique_queue_default")

#     c = cur.fetchall()
#     print(c)
#     accounts = []
#     for t in c:
#         x = dict(t)
#         accounts.append(x)
#     return accounts

# print("running")


# a = get_online_users()
# print(a)