from os.path import join
from helpers import *
from body_parser import body_parser
import controller


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

    # Update data to database

    # json
    # update_to_db(body)

    controller.addtoDB(req_uri, body)

    # Redirect to / or /index.html
    handle_redirect(res_sock, '')


def handle_redirect(res_sock, req_uri):
    redir_param = {
        "redirect": True,
        "path": '/index.html',
    }
    handle_response(res_sock, req_uri, redir_param)


def handle_response(res_sock, req_uri, redir_param={}):

    if req_uri == '':
        req_uri = 'index.html'

    file = join('server/src', req_uri)

    file_size = get_size(file)
    http_res = gen_status(file_size)

    print(req_uri, file_size)
    http_body = b'\r\n'

    http_body += read_file(file, req_uri, redir_param)

    res_headers = get_response_headers(file)

    for header in res_headers:
        http_res += header

    http_res += http_body

    res_sock.sendall(http_res)
    print("sent !!!!!")
    # res_sock.send("recieved".encode("utf-8"))
