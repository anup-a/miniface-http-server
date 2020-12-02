import sqlite3
from body_parser import body_parser
from os.path import join
from helpers import *
from argon2 import PasswordHasher
from response import handle_redirect
import jwt
import re
# from chat import run_chat_server
from random import randint

ph = PasswordHasher()

# ////////////////
# Database Handlers
# ////////////////

def addtoDB(res_sock, req_uri, body, token=None):
    try:
        parsedText = body_parser(body)
        handleDBPushAPI(res_sock, req_uri, parsedText, token)
    except:
        handleDBPushAPI(res_sock, req_uri, '', token)


def handleDBFetchAPI(req_uri, user_id):
    if req_uri in ['/index.html', '', '/', "index.html"]:
        return getPostsForUser(user_id)+get_posts_by_user(user_id)
    if req_uri in ['/users.html', "users.html"]:
        return get_users()
    if req_uri in ['/friends.html', "friends.html"]:
        return get_friends(user_id)
    if req_uri in ['/online.html', 'online.html']:
        return getOnlineFriends(user_id)
    if req_uri in ['/add_friends.html', "add_friends.html"]:
        return show_potential_friends(user_id)
    if req_uri in ['/friend_request.html', "friend_request.html"]:
        return show_request(user_id)
    if req_uri in ['me.html', '/me.html']:
        return get_posts_by_user(user_id)
    if req_uri[0:13] in ['messages.html'] or req_uri[0:14] in ['/messages.html']:
        if req_uri[0:13] in ['messages.html']:
            friend_user_id=req_uri[21:]
        if req_uri[0:14] in ['/messages.html']:
            friend_user_id=req_uri[22:]
        friend_user_id=int(friend_user_id)
        return get_messages(user_id,friend_user_id)  
    if re.match(r"\/?feed\.html\?user=(\d+)", req_uri):
        m = re.match(r"\/?feed\.html\?user=(\d+)", req_uri)
        user = m.group(1)
        return get_posts_by_user(user_id, user)  
    # if req_uri in ['/chat/start']:
    #     port = get_port_from_user(user_id)
    #     print(port)
    #     run_chat_server("server", port)
    
    # if req_uri in ['chat/send']:
        
    # if req_uri in ['chat/client']:
    #     port = get_port_from_user(user_id)
    #     print(port)
    #     run_chat_server("requester", port)



def handleDBPushAPI(res_sock, req_uri, body, token):

    user_id = 3 #Default
    print(token)

    if token and len(token) != 0:
        user = jwt.decode(token, 'MINI_SECRET', algorithms=['HS256'])
        username = user['username']
        session = get_user(username)
        print(session)
        user_id = dict(session)['user_id']

    if req_uri == '/addpost.html' or req_uri == 'addpost.html':
        print("Adding to SQLite Database.....")
        add_post(body["name"], token)
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
            handle_redirect(res_sock, user_id=res[1], req_uri="login_page.html")
        else:
            print(res[1])
            handle_redirect(res_sock, req_uri="signup_page.html")

    if req_uri=='/add_friends.html' or req_uri == 'add_friends.html':

        res = add_friend(user_id,body['user_id'])
        handle_redirect(res_sock,req_uri="add_friends.html")


    if req_uri=='/logout' or req_uri=="logout":

        print(req_uri)
        if token and len(token) != 0:
            user = jwt.decode(token, 'MINI_SECRET', algorithms=['HS256'])
            username = user['username']
            setOffline(username)

        handle_redirect(res_sock,req_uri="login_page.html")

    if req_uri=='/friends.html' or req_uri == 'friends.html':
        res = unfriend(user_id,body['user_id'])
        handle_redirect(res_sock,req_uri="friends.html")

    if req_uri=='/friend_request' or req_uri == 'friend_request':
        res = accept_friend_request(user_id,body['user_id'])
        handle_redirect(res_sock,req_uri="friend_request.html")

    if req_uri=='/reject_friend_request' or req_uri == 'reject_friend_request':
        res = reject_friend_request(user_id,body['user_id'])
        handle_redirect(res_sock,req_uri="friend_request.html")

    if req_uri == '/changestatus' or req_uri == 'changestatus':
        print(body)
        status = body['status']
        post_id = body['post_id']

        updatePostStatus(post_id, status, token)
        handle_redirect(res_sock, req_uri="me.html")
        
    if req_uri=='/insert_message' or req_uri == 'insert_message':
        res = insert_messages(user_id,body['friend_user_id'],body['msg'])
        new_url="messages.html?friend="+body['friend_user_id']
        handle_redirect(res_sock,req_uri=new_url)

# ////////////////
# Post CONTROLLERS
# ////////////////

def add_post(post_body, token):
    con = sqlite3.connect('server/db/posts.db')
    cur = con.cursor()
    user  = get_user(jwt.decode(token, 'MINI_SECRET', algorithm='HS256')['username'])
    user_id = dict(user)['user_id']
    cur.execute("insert into posts(post_body, user_id, status) values(?,?,?)",
                (post_body, user_id, "public"))
    con.commit()
    return "success"



def getPostsForUser(user_id):
    all_friends = get_friends(user_id)
    friends = [i['user_id2'] for i in all_friends]
    con = sqlite3.connect('server/db/posts.db')
    print(user_id, friends)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    sql="select * from posts where not status='private' and user_id in ({seq}) ".format(seq=','.join(['?']*len(friends)))
    cur.execute(sql, friends)
    c = cur.fetchall()

    posts = []
    for t in c:
        x = dict(t)
        user_id = x['user_id']
        author_name = get_user_by_id(user_id)
        x['author'] = author_name
        posts.append(x)
        
    return posts

def get_posts_by_user(user_id):
    con = sqlite3.connect('server/db/posts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from posts where user_id=?", (user_id,))

    c = cur.fetchall()

    print(user_id)
    posts = []
    author_name = get_user_by_id(user_id)
    for t in c:
        x = dict(t)
        x['author'] = author_name
        posts.append(x)
    return posts

def updatePostStatus(post_id, status, token):
    user  = get_user(jwt.decode(token, 'MINI_SECRET', algorithm='HS256')['username'])
    user_id = dict(user)['user_id']
    post = get_post_by_id(post_id)

    if (int(user_id) != int(dict(post)['user_id'])):
        return 0
    
    con = sqlite3.connect('server/db/posts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("update posts set status=? where post_id=?", (status, post_id,))
    con.commit()

def get_post_by_id(post_id):
    con = sqlite3.connect('server/db/posts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    post_id = int(post_id)
    cur.execute("select * from posts where post_id=?", (post_id,))

    c = cur.fetchone()
    if c:
        return c


    

# ////////////////
# User CONTROLLERS
# ////////////////

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
                setOnline(c[0])
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


def get_users():
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select Name, user_name from accounts")

    c = cur.fetchall()

    accounts = []
    for t in c:
        x = dict(t)
        accounts.append(x)
    # print(accounts)
    return accounts

def get_user(user_name):
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        "select user_id, Name, user_name from accounts where user_name=?", (user_name,))

    c = cur.fetchone()

    if c:
        return c

def get_user_by_id(user_id):
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute(
        "select Name, user_name from accounts where user_id=?", (user_id,))
    c = cur.fetchone()

    if c:
        return c['Name']

# //////////////////
# Friends CONTROLLERS
# //////////////////


def get_friends(user_id):
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    x = user_id
    cur.execute(
        'select user_id2 from friendship where user_id1=? and status="friends"', (x,))
    c = cur.fetchall()


    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    friends = []
    for friend in c:
        dic = dict(friend)
        user_id2= dic["user_id2"]  #{'user_id2': 5}
        cur.execute("select Name from accounts where user_id=?",(user_id2,))
        cnew = dict(cur.fetchone())
        dic["Name"]=cnew["Name"]
        friends.append(dic)
    return friends


def show_potential_friends(user_id):
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select user_id,Name, user_name from accounts")

    c = cur.fetchall()

    a = []
    for t in c:
        x = dict(t)
        a.append(x)
    return a


def add_friend(user_id, friend_user_id):
    friend_user_id=int(friend_user_id)
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("insert into friendship(user_id1, user_id2, status) values(?,?,?)",
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
    con.commit()


def accept_friend_request(user_id,friend_user_id):
    friend_user_id=int(friend_user_id)
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    print("Accept pending request")
    cur.execute("delete from friendship where user_id1=? and user_id2=? and status=?",
                    (friend_user_id,user_id,"pending"))
    cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (user_id,friend_user_id,"friends"))
    cur.execute("insert into friendship(user_id1, user_id2,status) values(?,?,?)",
                    (friend_user_id,user_id,"friends"))
    con.commit()

def reject_friend_request(user_id,friend_user_id):
    friend_user_id=int(friend_user_id)
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    print("Accept pending request")
    cur.execute("delete from friendship where user_id1=? and user_id2=? and status=?",
                    (friend_user_id,user_id,"pending"))
    con.commit()


def show_request(user_id):
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    x = user_id
    cur.execute(
        'select user_id1 from friendship where user_id2=? and status="pending"', (x,))
    c = cur.fetchall()


    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    friends = []
    for friend in c:
        dic = dict(friend)

        user_id1= dic["user_id1"]  #{'user_id2': 5}
        cur.execute("select Name from accounts where user_id=?",(user_id1,))
        cnew = dict(cur.fetchone())
        dic["Name"]=cnew["Name"]
        friends.append(dic)
    print(friends)
    return friends

# ////////////////
# Chat/Online CONTROLLERS
# ////////////////


def setOnline(user_id):
    try:
        con = sqlite3.connect('server/db/online_peers.db')
        con.row_factory = sqlite3.Row
        # con.set_trace_callback(print)
        cur = con.cursor()
        ip, port = "127.0.0.1", randint(1024, 9999)
        cur.execute("insert into online_peers(user_id, ip, port) values(?, ?, ?)",
                    (user_id, ip, port))
        con.commit()

    except:
        print("User already online.")

def setOffline(user_id):
    con = sqlite3.connect('server/db/online_peers.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("delete from online_peers where user_id=?",
                (user_id,))

    con.commit()

def get_port_from_user(user_id):

    con = sqlite3.connect('server/db/online_peers.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select port from online_peers where user_id=?",
                (user_id,))

    c = cur.fetchOne()
    return c


def getOnlineFriends(user_id):
    all_friends = get_friends(user_id)
    friends_ids = [i['user_id2'] for i in all_friends]
    con = sqlite3.connect('server/db/online_peers.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    sql="select * from online_peers where user_id in ({seq})".format(seq=','.join(['?']*len(friends_ids)))
    cur.execute(sql, friends_ids)
    c = cur.fetchall()
    print(c)
    con.commit()

    online_friends = []
    for friend in c:
        dic = dict(friend)
        online_friends.append(dic)

    return online_friends



def insert_messages(user_id,friend_user_id,message_content):
    friend_user_id=int(friend_user_id)
    con = sqlite3.connect('server/db/messages.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    print("inserting messages")
    cur.execute("insert into messages(user_id1, user_id2,message) values(?,?,?)",
                    (user_id,friend_user_id,message_content))
    # cur.execute("insert into messages(user_id1, user_id2,message) values(?,?,?)",
    #                 (user_id,friend_user_id,message_content))
    con.commit()

def get_messages(user_id,friend_user_id):
    friend_user_id=int(friend_user_id)
    con = sqlite3.connect('server/db/messages.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        'select user_id1,user_id2,message,timestamp,message_status from messages  where (user_id1=? and user_id2=?) or (user_id2=? and user_id1=?)', (user_id,friend_user_id,user_id,friend_user_id))
    c = cur.fetchall()

    message1_2 = []
    for x in c:
        dic = dict(x)
        message1_2.append(dic)
    cur = con.cursor()
    cur.execute(
        'update messages set message_status=? where (user_id2=? and user_id1=?)', ("read",user_id,friend_user_id))
    con.commit()
    
    return message1_2