def body_parser(body):
    body = body.decode("utf-8")
    data = body.split("=")
    postBody = data[1].replace("+", " ")
    return {data[0]: postBody}
