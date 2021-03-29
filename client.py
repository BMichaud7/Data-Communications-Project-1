#!/usr/bin/env python3

import socket
import sys

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #gets args from user to use in the program
    host = sys.argv[1]
    port = int(sys.argv[2])
    request_type = sys.argv[3]
    File = sys.argv[4]
    # print(sys.argv)
    #gets url request string ready to send info to the server. Consist of request type and host ip and port.
    url_string =  request_type + " /" +File + " HTTP/1.1\r\nHost: "+host+"\r\nAccept: text/html\r\nConnection: close\r\n\r\n"
    #connect to server
    s.connect((host , port))
    #send url_string to server
    s.sendall(url_string.encode())

    # print("REQ",request_type)
    #what request type is it? 
    #if get re wait for the server to respond.
    if request_type == "GET":
        while True:
            data = s.recv(1024)
            if not data:
                break
            # print(data.decode())
        s.close()
    # if put open file and sent it to the server.
    elif request_type == "PUT":
        with open(File, "r") as f:
            # print("READING NOW",f)
            for l in f.readlines():
                print(l)
                s.sendall(str.encode(""+l+""))
                l = f.read(1024)
        f.close()
        #send file to server
        data = s.recv(1024)
        #print responce
        print(data.decode())
        s.close()
        print('connection closed')
    else:
        print("NOT VALID COMMAND")
        sys.exit()
