import sqlite3
from os.path import join
from helpers import *
import controller

END_OF_REQ = b'\r\n\r\n'

def handle_redirect(res_sock, req_uri='index.html', user_id=None, token=None):
    redir_param = {
        "redirect": True,
        "path": req_uri,
        "user_id": user_id,
        "token": token,
    }
    print(redir_param)
    handle_response(res_sock, req_uri, redir_param)
    print('response done')


def handle_response(res_sock, req_uri, redir_param={}):
    if req_uri == '':
        req_uri = 'index.html'
    print('reached')
    file = join('server/src', req_uri)
    file_size = get_size(file)
    http_res = gen_status(file_size)

    http_body = b'\r\n'

    http_body += read_file(file, req_uri, redir_param)

    res_headers = get_response_headers(file)

    for header in res_headers:
        http_res += header

    http_res += http_body + END_OF_REQ
    print(http_res)
    res_sock.sendall(http_res)

def read_file(file, req_uri, redir_param={}):

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
    data = controller.handleDBFetchAPI(req_uri)
    file_data = template.render(
        {'data': data, 'token': token}, loader=loader).encode('utf-8')

    return file_data

    # if req_uri in ['/add_friends.html', "add_friends.html"]:
    #     return add_friends()
