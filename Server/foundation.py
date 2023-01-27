import socket


class ConnectionHandler:
    def __init__(self, server_socket: socket):
        self.connections: list[socket] = []
        self.server_socket = server_socket

    def wait_for_incomming_connections(self):
        self.server_socket.listen()

        while True:
            (client_socket, clientIP) = self.server_socket.accept()
            self.connections.append(client_socket)
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
