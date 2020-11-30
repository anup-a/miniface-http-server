import socket
import os
import re
from threading import Thread
import time
import sys
import time
HOST = 'localhost' 
stopthreads = set()

def send(req_sock):
    i = None
    while i!='Quit' and req_sock not in stopthreads:
        i = input()
        req_sock.sendall(i.encode() + b'\r\n\r\n')
    stopthreads.add(req_sock)

def parse_message(req_sock):
    req = b''
    while b'\r\n\r\n' not in req and req_sock not in stopthreads:
        req+=req_sock.recv(1024)
    return req

def receive(req_sock):
    req = parse_message(req_sock)
    while req!=b'Quit\r\n\r\n' and req_sock not in stopthreads:
        print(req)
        req = parse_message(req_sock)
    stopthreads.add(req_sock)

def client(req_sock, req_addr):
    req = parse_message(req_sock)
    if b'join' in req and (req_sock, req_addr):
        print("confirmation sent")
        req_sock.sendall(b"Join request accepted.\r\n\r\n")
    else:
        req_sock.sendall(b'Not Connected.')
        req_sock.close()
        return
    
    ts = Thread(target=send, args=(req_sock,))
    ts.daemon = True
    ts.start()

    tr = Thread(target=receive, args=(req_sock,))
    tr.daemon = True
    tr.start()

    while ts.is_alive() and tr.is_alive():
        pass
    print("closed")
    req_sock.close()
    sys.exit()
            
def server(port):

    # create socket
    listen_addr = '', port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(listen_addr)
    sock.listen(20)

    print("Server listening ....")

    while True:
        req_sock, req_addr = sock.accept()
        thread = Thread(target=client, args=(req_sock, req_addr))
        thread.start()

def send_join_request(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    s.sendall(b'join \r\n\r\n')
    print("Request sent")

    ts = Thread(target=send, args=(s,))
    ts.daemon = True
    ts.start()

    tr = Thread(target=receive, args=(s,))
    tr.daemon = True
    tr.start()

    while ts.is_alive() and tr.is_alive():
        pass
    print('closed')
    s.close()
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv)==3:
        if sys.argv[1]=='server':
            server(int(sys.argv[2]))
        elif sys.argv[1]=='requester':
            send_join_request(int(sys.argv[2]))