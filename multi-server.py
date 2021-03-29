import socket
import sys
import threading

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)



print('Listening on port %s ...' % SERVER_PORT)
def Socket_Thread(sock, addr):
    # Get the client request
    try:
        print("IN TRY")
        request = client_connection.recv(1024).decode()
        file_request = request.split()[1]
        file_request = "index.html" if file_request == "/" else file_request[1:]
        if request.split()[0] == "GET":
            with open(file_request, "r") as f:
                outputdata = f.read()

            response = ("HTTP/1.1 200 OK\n"
                    "Server: Python 3.8\n"
                    "Content-Type: text/html; charset=utf-8\r\n\n")
            print("SENDING RESPONSE")
            client_connection.send(response.encode())
            print("response sent")

        
            for i in range(0, len(outputdata)):
                client_connection.send(outputdata[i].encode())

            client_connection.send("\r\n".encode())
            client_connection.close()

        elif request.split()[0] == "PUT":
            filename = request.split()[1].replace("/", "")
            print("SAVING: ",filename)
            with open(filename, 'wb') as f:
                client_connection.sendall(str.encode("200 OK File Created"))
                while True:
                    print('receiving data...')
                    data = client_connection.recv(1024)
                    if not data:
                        break
                    # write data to a file
                    f.write(data) 
                f.close()
            
             
            

        # else: 

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


while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
    threading.Thread(target=Socket_Thread, args=(client_connection, client_address)).start()

