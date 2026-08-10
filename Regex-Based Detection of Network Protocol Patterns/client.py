import socket
import time

# Address of the server
# 127.0.0.1 means this same computer
HOST = "127.0.0.1"

# Must match the port used by server.py
PORT = 8080

# Create a TCP socket
# AF_INET = IPv4
# SOCK_STREAM = TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect((HOST, PORT))

while True:

    # Message we want to send
    message = "HELLO"

    # Convert the string into bytes and send it
    client.sendall(message.encode())

    # Wait for a response from the server
    # Receive up to 1024 bytes
    response = client.recv(1024)

    # Convert the received bytes back into text
    print("Server:", response.decode())

    # Wait one second before sending again
    time.sleep(1)
