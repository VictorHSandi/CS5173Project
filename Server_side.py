import socket
import threading

FORMAT = 'utf-8'
PRIVATE_IP = '10.1.0.4'
PORT = 9000
ADDRESS = (PRIVATE_IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server Initiated on " + PRIVATE_IP)
server.bind(ADDRESS)

clients = []
names = []

SERVER_PASSPHRASE = "ALICEBOB123"

def startChat():
    server.listen(5)
    print("Server started. Waiting for connections...")

    while True:
        conn, addr = server.accept()
        conn.send("123NAME123".encode(FORMAT))

        name = conn.recv(1024).decode(FORMAT)

        conn.send("123PASS123".encode(FORMAT))
        passphrase = conn.recv(1024).decode(FORMAT)

        if passphrase != SERVER_PASSPHRASE:
            conn.send("WRONG".encode(FORMAT))
            conn.close()
        else:
            names.append(name)
            clients.append(conn)

            print(f"Name is :{name}")

            broadcastMessage(f"{name} has joined the chat!".encode(FORMAT), conn, True)

            conn.send('Connection successful!'.encode(FORMAT))

            thread = threading.Thread(target=handle_client,
                                      args=(conn, addr), daemon=True)
            thread.start()

            print(f"active connections {threading.active_count() - 1}")


def handle_client(client_socket, addr):
    print(f"new connection {addr}")
    connected = True

    while connected:
        # receive message
        message = client_socket.recv(1024)

        # broadcast message
        broadcastMessage(message, client_socket, False)

    # close the connection
    client_socket.close()


def broadcastMessage(message, client_socket, forAll):
    for client in clients:
        if forAll:
            client.send(message)
        else:
            if client != client_socket:
                client.send(message)


startChat()
