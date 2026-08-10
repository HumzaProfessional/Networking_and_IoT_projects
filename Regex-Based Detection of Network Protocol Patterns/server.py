import socket

# 0.0.0.0 means:
# listen on all IPv4 network interfaces on this machine
HOST = "0.0.0.0"

# Port number the server will listen on
PORT = 8080

# Create a TCP socket
# AF_INET = IPv4
# SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allows the server to restart more easily without
# getting "Address already in use"
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Attach the socket to this IP address and port
server.bind((HOST, PORT))

# Put the socket into listening mode
# The server is now waiting for clients to connect
server.listen(1)

print(f"Listening on port {PORT}...")

while True:

    # Wait here until a client connects
    # client = new socket used to talk to that client
    # address = client's IP address and port
    client, address = server.accept()

    print("Connected from:", address)

    while True:

        # Receive up to 1024 bytes from the client
        data = client.recv(1024)

        # If recv() returns no data,
        # the client has disconnected
        if not data:
            break

        # Convert received bytes into readable text
        message = data.decode(errors="ignore")

        print("Received:", message)

        # Send a response back to the client
        # Network data is sent as bytes
        client.sendall(b"ACK")

    print("Client disconnected")

    # Close this client's connection
    client.close()
