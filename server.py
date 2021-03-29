import socket
import sys

#multi_server.py ony difference is everyting here is in a function and everytime someone connects we make a new thread.
# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = int(sys.argv[1])

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
    # Get the client request
    try:
        # print("IN TRY")
        #get request which is url_request string
        request = client_connection.recv(1024).decode()
        #get the file name that is being requested or going to be written.
        file_request = request.split()[1]
        #if no file name default to index.html
        file_request = "index.html" if file_request == "/" else file_request[1:]
        # if get request send file to client and send responce
        if request.split()[0] == "GET":
            with open(file_request, "r") as f:
                outputdata = f.read()

            response = ("HTTP/1.1 200 OK\n"
                    "Server: Python 3.8\n"
                    "Content-Type: text/html; charset=utf-8\r\n\n")
            print("SENDING RESPONSE")
            client_connection.send(response.encode())
            print("response sent")

            #swend data and file to client
            for i in range(0, len(outputdata)):
                client_connection.send(outputdata[i].encode())

            client_connection.send("\r\n".encode())
            client_connection.close()
        #if put  open file snet by client and send responce if file was created.
        elif request.split()[0] == "PUT":
            filename = request.split()[1].replace("/", "")
            print("SAVING: ",filename)
            with open(filename, 'wb') as f:
                client_connection.sendall(str.encode("200 OK File Created"))
                #saving file.
                while True:
                    print('receiving data...')
                    data = client_connection.recv(1024)
                    if not data:
                        break
                    # write data to a file
                    f.write(data) 
                f.close()
            
    except IOError:
        # Send response message for file not found
        response = ("HTTP/1.1 404 Not Found\n"
                    "Server: Python 3.8\n"
                    "Content-Type: text/html; charset=utf-8\r\n\n")
        client_connection.send(response.encode())
        client_connection.send("\r\n".encode())
        client_connection.close()

# Close socket
server_socket.close()