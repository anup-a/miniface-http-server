from body_parser import body_parser
from controller import *
from response import *


def handle_GET(res_sock, req_line):
    print("Fetching Response ...")
    
    http_req, req_uri, protocol_version = req_line
    print(req_uri,req_line)
    req_uri = req_uri[1:]
    handle_response(res_sock, req_uri)


def handle_POST(res_sock, req_line, req_headers):
    http_req, req_uri, protocol_version = req_line
    content_length = int(req_headers['Content-Length'])
    body = b''
    for i in range(content_length):
        msg = res_sock.recv(1)
        body += msg

    # Update data to database

    # json
    # update_to_db(body)

    addtoDB(res_sock, req_uri, body)

    # Redirect to / or /index.html
    # handle_redirect(res_sock, '')
