from body_parser import body_parser
from controller import *
from response import *
import jwt


def handle_GET(res_sock, req_line, token=None):
    print("Fetching Response ...")
    http_req, req_uri, protocol_version = req_line
    req_uri = req_uri[1:]

    if (req_uri in ['/index.html', '', '/', "index.html"]):
        # try:
        if token and len(token) != 0:
            user = jwt.decode(token, 'MINI_SECRET', algorithms=['HS256'])
            username = user['username']
            session = get_user(username)
            if session != None:
                handle_response(res_sock, req_uri="index.html", redir_param={'token': token})
            else:
                handle_redirect(res_sock, req_uri='login_page.html')
        else:
            handle_redirect(res_sock, req_uri='login_page.html')
        # except:
        #     handle_redirect(res_sock, req_uri='login_page.html')
    else:
        handle_response(res_sock, req_uri, {'token': token})


def handle_POST(res_sock, req_line, req_headers, token=None):
    http_req, req_uri, protocol_version = req_line
    content_length = int(req_headers['Content-Length'])
    body = b''

    if req_uri != '/addpost.html':
        for i in range(content_length):
            msg = res_sock.recv(1)
            body += msg
    else:
        boundary = b''
        while b'\r\n\r\n' not in boundary:
            msg = res_sock.recv(1)
            boundary += msg

        boundary_sep = boundary.split(b'\r\n')[0]

        form_body = b''

        while b'\r\n\r\n' not in form_body:
            msg = res_sock.recv(1)
            form_body += msg
        
        form_body = form_body.decode("utf-8")
        print(form_body)
        name = form_body.split('\r\n')[0]
        
        fn = re.findall(r'Content-Disposition.*name="fileToUpload"; filename="(.*)"', form_body)
        
        if not fn or len(fn)==0 or len(fn[0])==0:
            body = ("name=" + name).encode("utf-8")
            file_length = content_length - len(boundary) - len(form_body)
            print(file_length)
            for i in range(file_length):
                msg = res_sock.recv(1)

        else:
            file_path = 'server/src/uploads/'+ fn[0]

            try:
                out = open(file_path, 'wb')
            except IOError:
                return False, "Can't create file to write, do you have permission to write?"

            image_data = b''
            file_length = content_length - len(boundary) - len(form_body)
            escape = len('\r\n--\r\n') + len(boundary_sep)
            image_body_length = file_length - escape
            
            for i in range(file_length):
                msg = res_sock.recv(1)
                if i < image_body_length:
                    image_data += msg
                    out.write(msg)
            
            body = ("name=" + name + '&' + "img_path=" + fn[0]).encode()
            out.close()


    # print(body)
    # Update data to database

    # json
    # update_to_db(body)
    # print(req_uri)
    if (req_uri in ["login_page.html", "/login_page.html", "signup_page.html", "/signup_page.html"]) or (token and len(token) != 0):
        addtoDB(res_sock, req_uri, body, token)
    else:
        handle_redirect(res_sock, "login_page.html")

    # Redirect to / or /index.html
    # handle_redirect(res_sock, '')
