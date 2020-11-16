from os.path import join
from helpers import *


def handle_GET(res_sock, req_line):

    print("Fetching Response ...")

    http_req, req_uri, protocol_version = req_line

    req_uri = req_uri[1:]
    handle_response(res_sock, req_uri)


def handle_POST(res_sock, req_line, req_headers):

    http_req, req_uri, protocol_version = req_line

    content_length = int(req_headers['Content-Length'])
    body = b''

    for i in range(content_length):
        msg = res_sock.recv(1)
        body += msg

    update_to_db(body)

    # Redirect to / or /index.html
    handle_redirect(res_sock, '')


def body_parser(body):
    body = body.decode("utf-8")
    data = body.split("=")
    return {data[0]: data[1]}


def update_to_db(body):
    parsedText = body_parser(body)
    database["feed"].append(parsedText["name"])

    with open('server/db/data.json', 'w') as f:
        json.dump(database, f)


def handle_redirect(res_sock, req_uri):
    handle_response(res_sock, req_uri)


def handle_response(res_sock, req_uri):
    if req_uri == '':
        req_uri = 'index.html'

    print(req_uri)
    file = join('server/src', req_uri)

    file_size = get_size(file)
    http_res = gen_status(file_size)

    http_body = b'\r\n'
    http_body += read_file(file)

    res_headers = get_response_headers(file)

    for header in res_headers:
        http_res += header

    http_res += http_body

    res_sock.sendall(http_res)
