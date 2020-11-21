from body_parser import body_parser
from controller import *
from response import *
import jwt


def handle_GET(res_sock, req_line, token=None):
    print("Fetching Response ...")

    http_req, req_uri, protocol_version = req_line
    req_uri = req_uri[1:]

    if (req_uri in ['/index.html', '', '/', "index.html"]):
        # try:
        if token and len(token) != 0:
            user = jwt.decode(token, 'MINI_SECRET', algorithms=['HS256'])
            username = user['username']
            session = get_user(username)
            if session != None:
                handle_redirect(res_sock, req_uri="index.html", token=token)
            else:
                handle_redirect(res_sock, req_uri='login_page.html')
        else:
            handle_redirect(res_sock, req_uri='login_page.html')
        # except:
        #     handle_redirect(res_sock, req_uri='login_page.html')
    else:
        handle_response(res_sock, req_uri, {'token': token})


def handle_POST(res_sock, req_line, req_headers, token=None):
    http_req, req_uri, protocol_version = req_line
    content_length = int(req_headers['Content-Length'])
    body = b''
    for i in range(content_length):
        msg = res_sock.recv(1)
        body += msg

    # Update data to database

    # json
    # update_to_db(body)
    # print(req_uri)
    if (req_uri in ["login_page.html", "/login_page.html", "signup_page.html", "/signup_page.html"]) or (token and len(token) != 0):
        addtoDB(res_sock, req_uri, body)
    else:
        handle_redirect(res_sock, "login_page.html")

    # Redirect to / or /index.html
    # handle_redirect(res_sock, '')
