import socket

HOST = "0.0.0.0"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(1)

print(f"Listening on port {PORT}...")

while True:
    client, address = server.accept()
    print("Connected from:", address)

    while True:
        data = client.recv(1024)

        if not data:
            break

        message = data.decode(errors="ignore")
        print("Received:", message)

        client.sendall(b"ACK")

    print("Client disconnected")
    client.close()
