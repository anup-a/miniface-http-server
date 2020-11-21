import sqlite3
from os.path import join
from helpers import *
from db import *


def handle_redirect(res_sock, req_uri='index.html', user_id=None, token=None):
    redir_param = {
        "redirect": True,
        "path": req_uri,
        "user_id": user_id,
        "token": token,
    }
    handle_response(res_sock, req_uri, redir_param)


def handle_response(res_sock, req_uri, redir_param={}):
    if req_uri == '':
        req_uri = 'index.html'

    file = join('server/src', req_uri)
    file_size = get_size(file)
    http_res = gen_status(file_size)

    http_body = b'\r\n'

    http_body += read_file(file, req_uri, redir_param)

    res_headers = get_response_headers(file)

    for header in res_headers:
        http_res += header

    http_res += http_body

    res_sock.sendall(http_res)


def read_file(file, req_uri, redir_param):

    redirect = False
    path = "/"
    token = None

    if 'redirect' in redir_param.keys():
        redirect = redir_param['redirect']
        path = redir_param['path']

    if 'token' in redir_param.keys():
        token = redir_param['token']
    file_data = b''

    if get_size(file):
        if not redirect:
            if file.endswith('.html'):
                template = loader.load_template(file)
                file_data = generateHTML(template, loader, req_uri, token)
            else:
                res = open(file, 'r+b')
                for i in range(get_size(file)):
                    file_data += res.read()

        else:
            file = 'server/src/redirect.html'
            template = loader.load_template(file)
            file_data = template.render(
                {'path': path}, loader=loader).encode('utf-8')

        """
        For Static files
        """
        # res = open(file, 'r+b')
        # for i in range(get_size(file)):
        #     file_data += res.read()

    return file_data


def generateHTML(template, loader, req_uri, token=None):
    data = handleDBFetchAPI(req_uri)
    file_data = template.render(
        {'data': data, 'token': token}, loader=loader).encode('utf-8')

    return file_data


def handleDBFetchAPI(req_uri):
    if req_uri in ['/index.html', '', '/', "index.html"]:
        return get_posts()

    if req_uri in ['/users.html', "users.html"]:
        return get_users()
    if req_uri in ['/friends.html', "friends.html"]:
        return get_friends(3)


def get_posts():
    con = sqlite3.connect('server/db/posts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from posts")

    c = cur.fetchall()

    posts = []
    for t in c:
        x = dict(t)
        posts.append(x)
    return posts


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
    return accounts


def get_friends(user_id):
    con = sqlite3.connect('server/db/friendship.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    x = user_id
    cur.execute(
        'select user_id2 from friendship where user_id1=? and status="friends"', (x,))
    print(cur)
    c = cur.fetchall()

    friends = []
    for friend in c:
        dic = dict(friend)
        friends.append(dic)
    print(friends)
    return friends
