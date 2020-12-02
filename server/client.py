import socket
import time
import requests
import re
import subprocess, sys
import getpass
#login_password
#online_friends
#ip_address_show
#connection
'''
how to run:
for server:
    python3 server/client.py server <ip_Address>
for client
    python3 server/client.py client <ip_Address>
'''
def login(req, payload):
    return(requests.post("http://localhost:8080/{}".format(req), payload))

def GET(req, headers):
    return(requests.get("http://localhost:8080/{}".format(req), headers=headers))

def POST(req, data, headers={}):
    return(requests.post("http://localhost:8080/{}".format(req), data, headers=headers))

def run_server( port):
    script_name = 'server/client_server.py'
    cmd_line = [sys.executable, script_name, 'server', port]
    subprocess.check_call(cmd_line)

def request_to_join( port):
    script_name = 'server/client_server.py'
    cmd_line = [sys.executable, script_name, 'requester', '12345']
    subprocess.check_call(cmd_line)

if __name__ == '__main__':

    if sys.argv[1]=="server":
        run_server('12345')

    elif sys.argv[1]=="client":
        user_name=input("Please enter your user name to login : ")
        password=getpass.getpass(prompt="Enter your password : ")
        payload = {'username':user_name, "password":password}
        r = login('login_page.html', payload)
        print(r.text)
        if 'document.cookie' not in r.text:
            print("The user does not exist.")
            sys.exit()
        cookie = re.findall('document.cookie = ".*"', r.text)[0]
        print(cookie)
        while True:
            # print("Please enter 1 to chat")
            print("Please enter 2 to chat with friends")
            print("Please enter 3 to see your friends")
            print("Please enter 4 to see your online friends")
            print("Please enter 5 to quit")
            print("Please enter 6 to add post")
            print("Please enter 7 to see your post")
            print("Please enter 8 to see all post")
            print("Please enter 9 to add friends")
            print("Please enter 10 to see all pending request")
            print("Please enter 11 to accept pending request")
            print("Please enter 12 to reject pending request")
            print("Please enter 13 to change post status")

            response=int(input("Please enter your response : "))
            # if response==1:
            #     request_to_join('12345')
            if response==2:
                request_to_join('12345')
            elif response==3:
                r = GET('friends.html', {'Cookie': cookie[19:-1]})
                print(r.text)
            elif response==4:
                r = GET('online.html', {'Cookie': cookie[19:-1]})
                print(r.text)
            elif response==5:
                exit(0)
            elif response==6:
                print('Adding post')
                post_to_make=input("Please enter your post here : ")
                r = POST("addpost.html", {'name': post_to_make}, headers={'Cookie': cookie[19:-1]})
                print(r.text)
            elif response==7:
                print('Your Post')
                r = GET('me.html', {'Cookie': cookie[19:-1]})
                # print(r.text)
                temp=r.text.split("{")
                for i in temp:
                    i=i.replace(",",'')
                    i=i.replace("}",'')
                    i=i.replace("'",'')

                    print(i)
            elif response==8:
                print('All post')
                r = GET('index.html', {'Cookie': cookie[19:-1]})
                temp=r.text.split("{")
                for i in temp:
                    i=i.replace(",",'')
                    i=i.replace("}",'')
                    i=i.replace("'",'')
                    print(i)
                # print(r.text)
            elif response==9:
                print('Add friends')
                user_id=int(input("Please enter User_id of person : "))
                r = POST("add_friends.html", {'user_id': user_id}, headers={'Cookie': cookie[19:-1]})
                print(r.text)
            elif response==10:
                print('All pending request')
                r = GET('friend_request.html', {'Cookie': cookie[19:-1]})
                print(r.text)
                
            elif response==11:
                print('Accept friend request')
                user_id=input("Please enter User_id of person to accept : ")
                r = POST("friend_request", {'user_id': user_id}, headers={'Cookie': cookie[19:-1]})
                print(r.text)
            elif response==12:
                print('Reject friend request')
                user_id=input("Please enter User_id of person to accept : ")
                r = POST("reject_friend_request", {'user_id': user_id}, headers={'Cookie': cookie[19:-1]})
                print(r.text)
            elif response==13:
                post_id=int(input("Please enter Post - ID : "))
                print('Change Status of your post')
                print("Pick between 'friends','private' and 'public'")
                user_input=input("Please enter option : ")
                r = POST("changestatus", {'status': user_input,'post_id':post_id}, headers={'Cookie': cookie[19:-1]})
                print(r.text)
                
            else:
                print("Please select a number from the above list :)")
