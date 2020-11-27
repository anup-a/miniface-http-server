import socket
import time
import requests
import re

def login(req, payload):
    return(requests.post("http://localhost:8081/{}".format(req), payload))

def GET(req, headers):
    return(requests.get("http://localhost:8081/{}".format(req), headers=headers))

def POST(req, data, headers={}):
    return(requests.post("http://localhost:8081/{}".format(req), data, headers=headers))

if __name__ == '__main__':

    payload = {'username':'anup_22', "password":'hianup'}
    r = login('login_page.html', payload)
    cookie = re.findall('document.cookie = ".*"', r.text)[0]
    r = POST("addpost.html", {'name': "Hi, How do you do?"}, headers={'Cookie': cookie[19:-1]})
    print(r.text)
    r = GET('index.html', {'Cookie': cookie[19:-1]})
    print(r.text)