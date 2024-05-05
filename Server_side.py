import socket
import threading

FORMAT = 'utf-8'
PRIVATE_IP = '10.1.0.4'
PORT = 9000
ADDRESS = (PRIVATE_IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server Initiated on " + PRIVATE_IP)
server.bind(ADDRESS)

rooms = []

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

        found_room = None
        for room in rooms:
            if room.hash == passphrase:
                found_room = room
                break
        if found_room is not None:
            if len(found_room.clients) == 2:
                conn.send(f"The chatroom you tried to join is full!".encode(FORMAT))
            else:
                found_room.add_client(conn, addr, name)
        else:
            newroom = Chatroom(passphrase)
            rooms.append(newroom)
            newroom.add_client(conn, addr, name)


class Chatroom:
    def __init__(self, hash):
        self.clients = []
        self.names = []
        self.hash = hash

    def add_client(self, conn, addr, name):
        self.clients.append(conn)
        print(f"Name is: {name}")

        conn.send('Connection successful.'.encode(FORMAT))

        if len(self.names) != 0:
            for other in self.names:
                conn.send(f"{other} is already in the chat.\n".encode(FORMAT))
        self.names.append(name)
        self.broadcastMessage(f"{name} has joined the chat!".encode(FORMAT), conn, True)

        thread = threading.Thread(target=self.handle_client,
                                  args=(conn, addr, name), daemon=True)
        thread.start()

        print(f"active connections {threading.active_count() - 1}")

    def handle_client(self, client_socket, addr, name):
        print(f"new connection {addr}")

        while True:
            # receive message
            try:
                message = client_socket.recv(1024)

                # broadcast message
                self.broadcastMessage(message, client_socket, False)

            except:
                print(f"{name} disconnected")
                client_socket.close()
                self.clients.remove(client_socket)
                self.names.remove(name)
                self.broadcastMessage(f"{name} has disconnected.".encode(FORMAT), client_socket, False)
                if len(self.clients) == 0:
                    rooms.remove(self)
                    del self
                break

    def broadcastMessage(self, message, client_socket, forAll):
        for client in self.clients:
            if forAll:
                client.send(message)
            else:
                if client != client_socket:
                    client.send(message)


startChat()
