import socket
import time
import requests
import re
import subprocess, sys

def login(req, payload):
    return(requests.post("http://localhost:8080/{}".format(req), payload))

def GET(req, headers):
    return(requests.get("http://localhost:8080/{}".format(req), headers=headers))

def POST(req, data, headers={}):
    return(requests.post("http://localhost:8080/{}".format(req), data, headers=headers))

def run_server(HOST, port):
    script_name = 'server/client_server.py'
    cmd_line = [sys.executable, script_name, 'server', port, 'IP', HOST]
    subprocess.check_call(cmd_line)

def request_to_join(HOST, port):
    script_name = 'server/client_server.py'
    cmd_line = [sys.executable, script_name, 'requester', '12345', 'IP', HOST]
    subprocess.check_call(cmd_line)

if __name__ == '__main__':

    
    payload = {'username':'B', "password":'hianup'}
    r = login('login_page.html', payload)
    print(r.text)
    if 'document.cookie' not in r.text:
        print("The user does not exist.")
        sys.exit()
    cookie = re.findall('document.cookie = ".*"', r.text)[0]
    print(cookie)
    print('Add post')
    r = POST("addpost.html", {'name': "Hi, How do you do?"}, headers={'Cookie': cookie[19:-1]})
    print(r.text)
    print('Index')
    r = GET('index.html', {'Cookie': cookie[19:-1]})
    print(r.text)
    print("Friends")
    r = GET('friends.html', {'Cookie': cookie[19:-1]})
    print(r.text)
    r = GET('online.html', {'Cookie': cookie[19:-1]})
    print(r.text)
    request_to_join('', '12345')
    run_server('', '12345')
