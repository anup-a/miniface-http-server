from os.path import isfile, getsize
from mimetypes import guess_type
from datetime import datetime


def get_size(resource):
    file_size = 0
    if isfile(resource):
        file_size = getsize(resource)
    return file_size


def get_mime_type(file):

    mime_type = b'text/html'

    if get_size(file) > 0:
        (mime_type, encoding) = guess_type(file)
        mime_type = mime_type.encode('ASCII')
    return mime_type


def gen_status(file_size):

    status = b'HTTP/1.1 '

    if file_size > 0:
        status += b'200 OK\r\n'
    else:
        # no html file found
        status += b'404 Not Found\r\n'

    return status


def read_file(file):

    file_data = b''

    if get_size(file):
        res = open(file, 'r+b')

        for i in range(get_size(file)):
            file_data += res.read()

    return file_data


# create response headers for client response
def get_response_headers(file):

    response_headers = []

    timestamp = datetime.utcnow()
    date = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    response_headers.append(b'Date: ' + date.encode('ASCII') + b'\r\n')

    content_length = get_size(file)
    response_headers.append(b'Content-Length: ' +
                            str(content_length).encode('ASCII') + b'\r\n')

    response_headers.append(b'Content-Type: ' + get_mime_type(file) + b'\r\n')
    response_headers.append(b'Connection: close\r\n')

    return response_headers
