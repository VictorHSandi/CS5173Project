import socket
import threading

FORMAT = 'ISO-8859-1'
PRIVATE_IP = '10.1.0.4'
PORT = 9000
ADDRESS = (PRIVATE_IP, PORT)
PRIME = 903913
ROOT = 126

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server Initiated on " + PRIVATE_IP)
server.bind(ADDRESS)

rooms = []


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
        thread = threading.Thread(target=self.negotiate_key, daemon=True)
        thread.start()

    def add_client(self, conn, addr, name):
        self.clients.append(conn)
        print(f"Name is: {name}")

        conn.send('Connection successful.'.encode(FORMAT))
        self.broadcastMessage(f"{name} has joined the chat!\n".encode(FORMAT), conn, True)

        if len(self.names) != 0:
            for other in self.names:
                conn.send(f"{other} is already in the chat.\n".encode(FORMAT))
        else:
            conn.send(f"Waiting on second user...\n".encode(FORMAT))
        self.names.append(name)

        print(f"active connections {threading.active_count() - 1 - len(rooms)}")

    def handle_client(self, client_socket, name):
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

    def negotiate_key(self):
        while True:
            if len(self.names) == 2:
                self.broadcastMessage("123KEY123".encode(FORMAT), None, True)
                break
        self.broadcastMessage(str(PRIME).encode(FORMAT), None, True)
        self.broadcastMessage(str(ROOT).encode(FORMAT), None, True)
        ta = self.clients[0].recv(1024)
        tb = self.clients[1].recv(1024)
        self.clients[0].send(str(tb).encode(FORMAT))
        self.clients[1].send(str(ta).encode(FORMAT))

        for conn, name in zip(self.clients, self.names):
            thread = threading.Thread(target=self.handle_client,
                                      args=(conn, name), daemon=True)
            thread.start()


startChat()
