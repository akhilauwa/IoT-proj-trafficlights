'''
This file is the server for the YOLO traffic counter. It listens for incoming connections from the client and sends the traffic count to the client.
Runs on YOLO Server
Written by: Akhila Liyanage
'''

import socket
from datetime import datetime
from TrafficCounter import TrafficCounter

traffic_counter = TrafficCounter()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port to listen on (change accordingly)
host = "192.168.35.111"
port = 9000

# Bind the socket to the address
server_socket.bind((host, port))

# Listen for incoming connections (max 5 connections in the queue)
server_socket.listen(5)

# Set a timeout for the accept() method (1 second)
server_socket.settimeout(1)

def log_message(message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{current_time}   {message}")
    # print(message)

try:
    log_message(f"Listening for incoming connections on {host}:{port}")
    while True:
        try:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            log_message(f"Accepted connection from {client_address}")

            # Set a timeout for the client socket (1 second)
            client_socket.settimeout(1)

            while True:
                try:
                    # Receive data from the client
                    data = client_socket.recv(1024)  # Receive up to 1024 bytes

                    if not data:  # Break the loop if the client disconnects
                        log_message("Client disconnected.")
                        break

                    # Decode and print the received message
                    message = data.decode("utf-8")
                    log_message(f"Received message from {client_address}: {message}")
                    log_message("Getting traffic count...")
                    total_count = traffic_counter.count_cars_for_time(int(message))
                    log_message(f"Total Count: {total_count}")
                    
                    # Send traffic to Client
                    log_message("Sending traffic count to client...")
                    client_socket.send(str(total_count).encode("utf-8"))
                    log_message("Traffic data sent to client.")
                except socket.timeout:
                    log_message("Waiting for messages...")
                    continue

        except socket.timeout:
            log_message("Waiting for connections...")
            continue

except KeyboardInterrupt:
    log_message("Keyboard Interrupt registered")
    if 'client_socket' in locals():
        log_message("Closing client socket...")
        client_socket.close()
        log_message("Client socket closed.")

# Close the server socket
log_message("Closing server socket...")
server_socket.close()
log_message("Server socket closed.")
