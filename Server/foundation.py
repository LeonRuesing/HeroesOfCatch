import socket
import threading
import time
import random

class DisconnectListener:
    def on_disconnect(self, client_connection: object):
        pass

class ServerGlobals:
    connections = []

class ClientConnection:
    def __init__(self, client_socket: socket.socket, client_ip: str, disconnect_listener: DisconnectListener):
        self.socket = client_socket
        self.client_ip = client_ip
        self.disconnect_listener = disconnect_listener

    def listen_for_pakets(self):
        try:
            while True:
                raw = str(self.socket.recv(1024).decode())
                data = raw.split(";")
                paket_id = int(data[0])

                # Login
                if paket_id == 1:
                    time.sleep(1)  # Cooldown
                    print(raw)
                    username = str(data[1])
                    key = str(data[2])
                    print(f"Login-Versuch mit '{username},{key}'")
                    self.socket.sendall(f'1;{username}'.encode())

                    add_data = f'2;{username};{random.randint(0, 500)};{random.randint(0, 500)}'.encode()
                    for i in ServerGlobals.connections:
                        i.socket.sendall(add_data)

                print(f'[ClientConnection] Der Client {socket.gethostname()} sendete Paket {paket_id}')
        # Catch every exception
        except Exception as e:
            print('[ClientConnection]', 'Fehler bei der Datenübertragung: ' + str(e))
            self.disconnect_listener.on_disconnect(self)
            self.socket.close()
            return


class ConnectionHandler(DisconnectListener):
    def __init__(self, server_socket: socket):
        #self.connections: list[ClientConnection] = []
        self.server_socket = server_socket

    def on_disconnect(self, client_connection: ClientConnection):
        print('[ConnectionHandler]', f'Verbindung abgebrochen von: {client_connection.client_ip}')
        ServerGlobals.connections.remove(client_connection)

    def wait_for_incomming_connections(self):
        self.server_socket.listen()

        while True:
            (client_socket, client_ip) = self.server_socket.accept()
            print('[ConnectionHandler]', f'Eingehende Verbindung von: {client_ip}')

            client_connection = ClientConnection(client_socket, client_ip, self)
            threading.Thread(target=client_connection.listen_for_pakets).start()

            ServerGlobals.connections.append(client_connection)

            # Send welcome
            client_socket.sendall("0".encode())
            pass


class ServerFoundation:
    def __init__(self, port: int):
        self.host = 'localhost'
        self.port = port

        self.server_socket = socket.socket()
        print('[Start]', 'Socket erstellt!')

    def start(self):
        try:
            print('[Start]', 'Starten...')
            self.server_socket.bind((self.host, self.port))
            print('[Start]', f'Server erfolgreich gestartet bei {self.host}:{self.port}')
        except socket.error as msg:
            print('[ERROR]', str(msg))


if __name__ == '__main__':
    server_foundation = ServerFoundation(56021)
    server_foundation.start()

    connection_handler = ConnectionHandler(server_foundation.server_socket)
    connection_handler.wait_for_incomming_connections()
