import socket
import time

HOST = "127.0.0.1"
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    message = "HELLO"

    client.sendall(message.encode())

    response = client.recv(1024)
    print("Server:", response.decode())

    time.sleep(1)
