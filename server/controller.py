import sqlite3
from body_parser import body_parser


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


def handleDBPushAPI(req_uri, body):
    if req_uri == '/addpost.html' or req_uri == 'addpost.html':
        print("Adding to SQLite Database.....")
        add_post('2', body["name"], '1')
        print("Done. Added")


def addtoDB(req_uri, body):
    print(req_uri, body)
    parsedText = body_parser(body)
    handleDBPushAPI(req_uri, parsedText)


def generateHTML(template, loader, req_uri):
    data = handleDBFetchAPI(req_uri)
    file_data = template.render({'data': data}, loader=loader).encode('utf-8')

    return file_data
