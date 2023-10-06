import socket

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind(("b8:08:cf:f1:1a:d9", 4))

server.listen(1)
client, address = server.accept()

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print("Received: %s" % data)
        message = input("Enter message: ")
        client.send(message)
except OSError as e:
    print("Error: %s" % e)

client.close()
server.close()