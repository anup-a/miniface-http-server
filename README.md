# MiniFace HTTP Server

MiniFace HTTP Server is the minimal replica of facebook with custom socket server implementation, custom framework. It servers html pages using quik templating engine, and data is handled with sqlite.

Note : This project is just to demonstrate minimal http server, and none of the techniques are scaled to their standard and efficient level. 

![image](https://user-images.githubusercontent.com/29516633/100913633-0ed05480-34f8-11eb-8614-5fe0af21fdb8.png)



## Features

- 🌍 Serves HTML pages over TCP non-persistent connection.
- 🌛 Serves images, text files.
- 💻 Supports file uploading ( implemented as social media post image upload )
- 🏹 User can signup and login ( hashed credentials are stored in DB).
- ⭐ User can add post, view feed and view others profile.
- 🚴‍♀️ User can change status of their posts.
- 🤼 User can accept/add new/ friends and also friend requests.

## Code Structure

- server.py - Custom socket server to recieve HTTP Requests

- http_requests.py - Handle GET & POST Requests separately

- response.py - create response based on user's request.

- db.py - initialize db and defines schema

- controller.py - handles all data related operations

- src/* - all the static servings

- src/uploads/* - all the uploaded images are stored in this dir

- helpers.py - all the methods to parse HTTP headers.

- body_parser.py - formats the form body for signup/login/post-form data.

## Snapshots


| Section      | Snapshot |
| ----------- | ----------- |
| Main Section      | ![image](https://user-images.githubusercontent.com/29516633/100913883-58b93a80-34f8-11eb-975e-819ed859936e.png)|
| Chat Section   | <center> <img src="https://user-images.githubusercontent.com/29516633/100913917-65d62980-34f8-11eb-8f1d-d9f64c5b34c4.png" width="60%"></center>|
| User's Timeline   | ![image](https://user-images.githubusercontent.com/29516633/100914069-94540480-34f8-11eb-9e41-d8477e0ea8cc.png)|
| Friend's Section   | ![image](https://user-images.githubusercontent.com/29516633/100914416-088ea800-34f9-11eb-82d9-7e4c2f79faa5.png)|



----


## Running Instructions

**Github Repository - **
	
- *Branch Master* - 
This branch contains code to run server and client on browser.

- *Branch Client* - 
This Branch contains code to run server and `cli` client on terminal.
	
In the root directory of the project
`python server\server.py` will start the server instance.

Client - We have implemented a server to handle HTTP Requests, hence browser can be used as a client or run client.py file by following commands

> Default - run `http://localhost:8080` on browser


**Client Branch - How to run Client-server: **

> Server: `python3 server/server.py`

> Client: `python3 server/client.py client `

> Client-Server: `python3 server/client.py server`


To chat with a friend, first look at what all friends are online first press 4 to check his/her/their IP and then press 2 to go to the chat option. Input the IP of that friend and a chat will start. To exit from the chat enter ‘Quit’. Note, you can only chat if the other party’s client-server is on.


```
cd mini-facebook
python server\server.py

```


Examples of HTTP Headers & mimetypes from `https://www.tutorialspoint.com/http/http_requests.htm`


### GET Request

```
GET /hello.htm HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.tutorialspoint.com
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive
```


### POST Request

```
POST /cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.tutorialspoint.com
Content-Type: text/xml; charset=utf-8
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

<?xml version="1.0" encoding="utf-8"?>
<string xmlns="http://clearforest.com/">string</string>
```

#### Contributors

- Abhisht Tiwari - IIT Gn CSE
- Aditya Grag - IIT Gn CSE
- Anup Aglawe - IIT Gn CSE

#### UI Designs

> Inspired By https://dribbble.com/shots/9650156-Facebook-Ui-Redesign/attachments/1678611?mode=media
