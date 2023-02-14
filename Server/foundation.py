import socket
import threading


class DisconnectListener:
    def on_disconnect(self, client_connection: object):
        pass


class ClientConnection:
    def __init__(self, client_socket: socket.socket, disconnect_listener: DisconnectListener):
        self.socket = client_socket
        self.disconnect_listener = disconnect_listener

    def listen_for_pakets(self):
        try:
            while True:
                paket_id = self.socket.recv(1024).decode()
                print(f'[ClientConnection] Der Client {socket.gethostname()} sendete Paket {paket_id}')
        # Catch every exception
        except Exception:
            self.disconnect_listener.on_disconnect(self)
            self.socket.close()
            return


class ConnectionHandler(DisconnectListener):
    def __init__(self, server_socket: socket):
        self.connections: list[ClientConnection] = []
        self.server_socket = server_socket

    def on_disconnect(self, client_connection: object):
        print('[ConnectionHandler]', f'Verbindung abgebrochen von: {client_connection}')
        self.connections.remove(client_connection)

    def wait_for_incomming_connections(self):
        self.server_socket.listen()

        while True:
            (client_socket, clientIP) = self.server_socket.accept()

            client_connection = ClientConnection(client_socket, self)
            threading.Thread(target=client_connection.listen_for_pakets).start()

            self.connections.append(client_connection)

            # Send welcome
            client_socket.sendall("0".encode())

            print('[ConnectionHandler]', f'Eingehende Verbindung von: {clientIP}')
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
            print('[ERROR]', f'{msg[0]}: {msg[1]}')


if __name__ == '__main__':
    server_foundation = ServerFoundation(56021)
    server_foundation.start()

    connection_handler = ConnectionHandler(server_foundation.server_socket)
    connection_handler.wait_for_incomming_connections()
