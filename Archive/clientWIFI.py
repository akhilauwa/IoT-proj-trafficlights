import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's host and port
host = "10.135.192.199"  # Use the server's IP address or "localhost" for local testing
port = 9000  # Use the same port number as the server

# Connect to the server
client_socket.connect((host, port))

# Send a message to the server
try:
    while True:
        message = input("Enter a message to send to the server: ")
        client_socket.send(message.encode("utf-8"))
        if message == "exit":
            break
except KeyboardInterrupt:
    print("Closing client socket...")
    client_socket.close()
    print("Client socket closed.")