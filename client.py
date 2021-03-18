#!/usr/bin/env python3

import socket
import sys

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    host = sys.argv[1]
    port = int(sys.argv[2])
    request_type = sys.argv[3]
    File = sys.argv[4]
    print(sys.argv)
    url_string =  request_type + " /" +File + " HTTP/1.1\r\nHost: "+host+"\r\nAccept: text/html\r\nConnection: close\r\n\r\n"
    s.connect((host , port))
    s.sendall(url_string.encode())
    if request_type == "GET":
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(data.decode())
    elif request_type == "PUT":
        with open(File, "r") as f:
            for l in f.readlines():
                print(l)
                s.sendall(str.encode(""+l+""))
                l = f.read(1024)
        f.close()
        data = s.recv(1024)
        print(data.decode())
        s.close()
        print('connection closed')
    else:
        print("NOT VALID COMMAND")
        sys.exit()
