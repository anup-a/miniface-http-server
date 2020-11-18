import sqlite3
from body_parser import body_parser
from os.path import join
from helpers import *


def add_post(post_id, post_body, user_id):
    con = sqlite3.connect('server/db/posts.db')
    cur = con.cursor()
    cur.execute("insert into posts(post_id, post_body, user_id) values(?,?,?)",
                (post_id, post_body, user_id))
    con.commit()
    return "success"


def get_posts():
    con = sqlite3.connect('server/db/posts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from posts")

    c = cur.fetchall()
    print(c)

    posts = []
    for t in c:
        x = dict(t)
        posts.append(x)

    return posts

# legacy method


def update_to_db(body):
    parsedText = body_parser(body)
    database["feed"].append(parsedText["name"])

    with open('server/db/data.json', 'w') as f:
        json.dump(database, f)

# legacy method


def populate_data(template):
    file_data = template.render(
        {'feed': database["feed"]}, loader=loader).encode('utf-8')

    return file_data


def handleDBFetchAPI(req_uri):
    if req_uri in ['/index.html', '', '/', "index.html"]:
        return get_posts()


def login(user_name, password):
    con = sqlite3.connect('server/db/accounts.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from accounts where user_name=?", (user_name,))

    c = cur.fetchone()
    # posts = []
    if c:
        if c[2]==password:
            return((1, c[0]))
        else:
            return((0, 'The password was wrong.'))
    else:
        return((0, 'The username does not exist.'))
    # return posts


def handleDBPushAPI(res_sock, req_uri, body):
    if req_uri == '/addpost.html' or req_uri == 'addpost.html':
        print("Adding to SQLite Database.....")
        add_post('2', body["name"], '1')
        print("Done. Added")
        return req_uri
        
    if req_uri=='/login_page.html' or req_uri == 'login_page.html':
        print(body)
        res = login(body['username'], body['password'])
        if res[0]:
            print("authenticated.")
            handle_redirect(res_sock, user_id=res[1])
        else:
            print(res[1])
            handle_redirect(res_sock)


def addtoDB(res_sock, req_uri, body):
    print(req_uri, body)
    parsedText = body_parser(body)
    handleDBPushAPI(res_sock, req_uri, parsedText)


def generateHTML(template, loader, req_uri):
    data = handleDBFetchAPI(req_uri)
    file_data = template.render({'data': data}, loader=loader).encode('utf-8')

    return file_data

def handle_redirect(res_sock, req_uri='/index.html', user_id=None):
    redir_param = {
        "redirect": True,
        "path": req_uri,
        "user_id": user_id,
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

    if 'redirect' in redir_param.keys():
        redirect = redir_param['redirect']
        path = redir_param['path']

    file_data = b''

    if get_size(file):

        if not redirect:
            template = loader.load_template(file)
            file_data = generateHTML(template, loader, req_uri)

        else:
            res = open('server/src/redirect.html', 'r+b')
            for i in range(get_size(file)):
                file_data += res.read()

        """
        For Static files
        """
        # res = open(file, 'r+b')
        # for i in range(get_size(file)):
        #     file_data += res.read()

    return file_data