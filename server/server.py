import socket
from os.path import isfile, join, getsize
from datetime import datetime
from threading import Thread, enumerate
from helpers import *
from http_request import *


END_OF_REQ = '\r\n\r\n'
END_OF_HEADERS = '\r\n'


def main():
    # initialize server
    init_server(port=8080)


def init_server(port):

    # create socket
    listen_addr = '', port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(listen_addr)
    sock.listen(5)

    print("Server listening ....")

    while True:
        req_sock, req_addr = sock.accept()
        thread = Thread(target=handle_req, args=(req_sock,)).start()
        print('Running Threads: ', enumerate())


def handle_req(req_sock):
    req_line, req_headers = read_http_request(req_sock)
    http_req, resource, protocol_version = req_line

    if http_req == 'GET':
        handle_GET(req_sock, req_line)

    elif http_req == 'POST':
        handle_POST(req_sock, req_line, req_headers)

    else:
        print(f'{http_req} Not Implemented Yet')
        req_sock.sendall(
            b'HTTP/1.1 405 Method Not Allowed\r\nAllow: GET\r\n\r\n')


def read_http_request(req_sock):

    # \r\n\r\n (CR LF CR LF) - End of Request
    http_req = b''

    while b'\r\n\r\n' not in http_req:
        msg = req_sock.recv(1)
        http_req += msg

    req_line, req_headers = http_req.decode('ASCII').split(END_OF_HEADERS, 1)

    # Ex - req-line = GET /hello.htm HTTP/1.1
    req_line = req_line.split(' ', 3)

    header_dict = {}
    req_headers = req_headers.split(END_OF_HEADERS)

    for header in req_headers:
        if header == "":
            continue

        [header_key, header_val] = header.split(': ', 1)
        header_dict[header_key] = header_val

    return req_line, header_dict


if __name__ == '__main__':
    main()
