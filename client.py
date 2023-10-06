import socket

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("b8:27:eb:8c:3a:6e", 4))

try:
    while True:
        message = input("Enter message: ")
        client.send(message)
        data = client.recv(1024)
        if not data:
            break
        print("Received: %s" % data)
except OSError as e:
    print("Error: %s" % e)

client.close()