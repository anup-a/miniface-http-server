def body_parser(body):
    body = body.decode("utf-8")
    if '&' in body:
        all_data = body.split("&")
    else:
        all_data = [body]
    dic = dict()
    for data2 in all_data:
        data = data2.split('=')
        postBody = data[1].replace("+", " ")
        dic[data[0]] = postBody
    return dic
