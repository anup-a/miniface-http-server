import sqlite3
from os.path import join
from helpers import *
import controller
import jwt


def handle_redirect(res_sock, req_uri='index.html', user_id=None, token=None):
    redir_param = {
        "redirect": True,
        "path": req_uri,
        "user_id": user_id,
        "token": token,
    }
    print(redir_param)
    handle_response(res_sock, req_uri, redir_param)


def handle_response(res_sock, req_uri, redir_param={}): #http
    url=req_uri[:]
    # print(url)
    if url == '':
        url = 'index.html'
    if (not url.endswith('html')) and 'html' in url: #htt
        url=url.split("?")
        url=url[0]
        # print(url)
        
        
    file = join('server/src', url)
    file_size = get_size(file)
    http_res = gen_status(file_size)

    http_body = b'\r\n'

    http_body += read_file(file, req_uri, redir_param)

    res_headers = get_response_headers(file)

    for header in res_headers:
        http_res += header

    http_res += http_body
    res_sock.sendall(http_res)


def read_file(file, req_uri, redir_param={}):
    print("reading file...")
    redirect = False
    path = "/"
    token = None

    if 'redirect' in redir_param.keys():
        redirect = redir_param['redirect']
        path = redir_param['path']

    if 'token' in redir_param.keys():
        token = redir_param['token']
    
    file_data = b''

    if get_size(file):
        if not redirect:
            if file.endswith('.html'):
                template = loader.load_template(file)
                file_data = generateHTML(template, loader, req_uri, token)
            else:
                res = open(file, 'r+b')
                for i in range(get_size(file)):
                    file_data += res.read()

        else:
            strToken = None
            if token and type(token) != str:
                strToken = token.decode('utf-8')
            else:
                strToken = token

            # if token != None:
            #     template = loader.load_template(file)
            #     file_data = generateHTML(template, loader, req_uri, token=strToken)

            # else:
            file = 'server/src/redirect.html'
            template = loader.load_template(file)

            file_data = template.render(
                {'path': path, 'token': strToken}, loader=loader).encode('utf-8')

        """
        For Static files
        """
        # res = open(file, 'r+b')
        # for i in range(get_size(file)):
        #     file_data += res.read()

    return file_data


def generateHTML(template, loader, req_uri, token=None):
    print("generating HTML")
    #defa ult User
    user_id = 3
    if token and len(token) != 0:
        user = jwt.decode(token, 'MINI_SECRET', algorithms=['HS256'])
        username = user['username']
        session = controller.get_user(username)
        user_id = dict(session)['user_id']

    data = str(controller.handleDBFetchAPI(req_uri, user_id)).encode()
    # file_data = template.render(
    #     {'data': data, 'token': token}, loader=loader).encode('utf-8')

    return data
