import socket
from datetime import datetime as dt

client_connected = False
dt_str = '%Y-%m-%d %H:%M:%S'

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port to listen on
host = "10.135.192.199"
port = 9000  

# Bind the socket to the address
server_socket.bind((host, port))

# Listen for incoming connections (max 5 connections in the queue)
server_socket.listen(5)

# Set a timeout for the accept() method (1 second)
server_socket.settimeout(1)


print(f"{dt.now().strftime(dt_str)}   Listening for incoming connections on {host}:{port}")
try:
    while True:
        try:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print(f"{dt.now().strftime(dt_str)}   Accepted connection from {client_address}")
            client_connected = True
            break
        except socket.timeout:
            print(f"{dt.now().strftime(dt_str)}   Waiting for connections...")
            continue

    # Set a timeout for the client socket (1 second)
    client_socket.settimeout(1)

    while client_connected:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)  # Receive up to 1024 bytes

            if not data: # Break the loop if the client disconnects
                print(f"{dt.now().strftime(dt_str)}   Client disconnected.")
                break  

            # Decode and print the received message
            message = data.decode("utf-8")
            print(f"{dt.now().strftime(dt_str)}   Received message from {client_address}: {message}")
        except socket.timeout:
            print(f"{dt.now().strftime(dt_str)}   Waiting for messages...")
            continue
except KeyboardInterrupt:
    print(f"{dt.now().strftime(dt_str)}   Keyboard Interrupt registered")
    if client_connected:
        print(f"{dt.now().strftime(dt_str)}   Closing client socket...")
        client_socket.close()
        print(f"{dt.now().strftime(dt_str)}   Client socket closed.")
    
print(f"{dt.now().strftime(dt_str)}   Closing server socket...")
server_socket.close()
print(f"{dt.now().strftime(dt_str)}   Server socket closed.")