#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        print("test1")
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("test2")
        clientSocket.connect((host,int(port)))
        print("test3")
        return clientSocket

    def get_code(self, data):
        code = data.split(" ")[1]
        return int(code)

    def get_headers(self,data):
        headers = data.split("\r\n\r\n")
        headers = headers[0].split('\n')[1:]
        return str(headers)

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1:][0]

        return str(body)

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        parsing = re.search('(https?):\/\/([^\/?#]+)(.*)', url)
        
        protocol = parsing.groups()[0]
        host = parsing.groups()[1]
        path = parsing.groups()[2]


        s = host.split(':')
        
        host = s[0]
        if (len(s) > 1):
            port = s[1]
        else:
            port = 80
        
        
        request = "GET " + path + " HTTP/1.0\n" + "Host: " + host + "\n\n"
        print('-------\n')
        print(request)
        print('-------\n')
        
        try:
            print(host, port)
            socket = self.connect(host, port)
            print("connected")
            socket.sendall(request)
            print("request sent")
            result = self.recvall(socket)
            
            print(result)

            code = self.get_code(result)
            body = self.get_body(result)

            header = self.get_headers(result)
        
            print(code,body,header)
            
        except:
            code = 404
            body = "<html><body>404 Error</body></html>\r\n"
    
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        
        request  = "POST" + url + "HTTP/1.0\n\n"
        
        try:
            socket = self.connect(url, 80)
            socket.sendall(request)
            result = self.recvall(socket)
        
            code = self.get_code(result)
            body = self.get_body(result)
            header = self.get_headers(result)
        
            print(code,body)

        except:
            print(sys.exc_info())
            code = 404
            body = "<html><body>404 Error</body></html>\r\n"

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command(sys.argv[1] )
