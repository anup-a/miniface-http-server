from os.path import join
from helpers import *


def handle_GET(res_sock, req_line):

    http_req, req_uri, protocol_version = req_line

    req_uri = req_uri[1:]
    if req_uri == '':
        req_uri = 'index.html'

    file = join('src', req_uri)

    file_size = get_size(file)
    http_res = gen_status(file_size)

    res_headers = get_response_headers(file)

    for header in res_headers:
        http_res += header

    http_res += b'\r\n'
    http_res += read_file(file)

    res_sock.sendall(http_res)


def handle_POST(res_sock, req_line, req_headers):

    http_req, req_uri, protocol_version = req_line

    content_length = int(req_headers['Content-Length'])
    body = b''

    for i in range(content_length):
        msg = res_sock.recv(1)
        body += msg

    # DO SOMETHING
    print(body)
