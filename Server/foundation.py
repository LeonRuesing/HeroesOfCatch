import threading
import time

from ingame import ActiveRound
from shared import *


class PacketListener:

    @staticmethod
    def listen_for_packets(socket: socket.socket):
        while True:
            raw = str(socket.recv(1024).decode())
            data = raw.split(";")
            print('RAW: ' + raw)
            paket_id = int(data[0])

            # Login
            if paket_id == 1:
                time.sleep(1)  # Cooldown
                print(raw)
                username = str(data[1])
                key = str(data[2])

                ServerGlobals.CONNECTION_LINKS.append(UserConnectionLink(socket, username))

                #temp create new round
                if len(ServerGlobals.CONNECTION_LINKS) == 2:
                    round = Round()
                    round.users = ServerGlobals.CONNECTION_LINKS

                    ingame_handler = ActiveRound(round)
                    ingame_handler.start_game()

                print(f"Login-Versuch mit '{username},{key}'")
                socket.sendall(f'1;{username}'.encode())

            print(f'[ClientConnection] Der Client {socket.getpeername()} sendete Paket {paket_id}')


class ConnectionHandler(DisconnectListener):
    def __init__(self, server_socket: socket):
        self.server_socket = server_socket

    def on_disconnect(self, client_connection: ClientConnection):
        print('[ConnectionHandler]', f'Verbindung abgebrochen von: {client_connection.client_ip}')
        ServerGlobals.CONNECTIONS.remove(client_connection)

    def wait_for_incomming_connections(self):
        self.server_socket.listen()

        while True:
            (client_socket, client_ip) = self.server_socket.accept()
            print('[ConnectionHandler]', f'Eingehende Verbindung von: {client_ip}')

            client_connection = ClientConnection(client_socket, client_ip, self)

            ServerGlobals.CONNECTIONS.append(client_connection)

            threading.Thread(target=self.start_packet_listener, args=(client_connection,)).start()

            # Send welcome
            client_socket.sendall("0".encode())

    @staticmethod
    def start_packet_listener(client_connection: ClientConnection):
        try:
            packet_listener = PacketListener()
            packet_listener.listen_for_packets(client_connection.socket)
        # Catch every exception
        except Exception as e:
            print('[ClientConnection]', 'Fehler bei der Datenübertragung: ' + str(e))
            client_connection.disconnect_listener.on_disconnect(client_connection)
            client_connection.socket.close()


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
    server_foundation = ServerFoundation(ServerGlobals.PORT)
    server_foundation.start()

    connection_handler = ConnectionHandler(server_foundation.server_socket)
    connection_handler.wait_for_incomming_connections()
