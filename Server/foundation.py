import threading
import time

from general import MatchmakingHandler
from ingame import ActiveRoundHandler
from shared import *


class PacketListener:

    @staticmethod
    def listen_for_packets(socket: socket.socket):
        while True:
            raw = str(socket.recv(1024).decode())
            data = raw.split(";")
            print('RAW: ' + raw)
            packet_id = int(data[0])

            # Login
            if packet_id == 1:
                time.sleep(1)  # Cooldown
                print(raw)
                username = str(data[1])
                key = str(data[2])

                print(f"Login-Versuch mit '{username},{key}'")
                socket.sendall(f'1;{username}'.encode())
                user = UserConnectionLink(socket, username)

                ServerGlobals.CONNECTION_LINKS.append(user)

            elif packet_id == 2:
                round_username = ServerGlobals.get_client_connection_by_socket(socket).username
                active_round = ServerGlobals.get_round_by_username(round_username)

                left = int(data[1])
                right = int(data[2])
                top = int(data[3])
                bottom = int(data[4])

                movement = (left, right, top, bottom)
                if active_round is not None:
                    active_round.update_movement_for_user(round_username, movement)
            elif packet_id == 3:
                selected_hero_id = int(data[1])

                user = ServerGlobals.get_client_connection_by_socket(socket)
                user.selected_hero_id = selected_hero_id

                MatchmakingHandler.add_player(user)
            elif packet_id == 4:
                user = ServerGlobals.get_client_connection_by_socket(socket)
                MatchmakingHandler.remove_player(user)
            elif packet_id == 5:
                round_username = ServerGlobals.get_client_connection_by_socket(socket).username
                active_round = ServerGlobals.get_round_by_username(round_username)
                if active_round is not None:
                    active_round.request_ability(round_username)


            print(f'[ClientConnection] Der Client {socket.getpeername()} sendete Paket {packet_id}')


class ConnectionHandler(DisconnectListener):
    def __init__(self, server_socket: socket):
        self.server_socket = server_socket

    def on_disconnect(self, client_connection: ClientConnection):
        print('[ConnectionHandler]', f'Verbindung abgebrochen von: {client_connection.client_ip}')

        user = ServerGlobals.get_connection_link_by_cc(client_connection)

        MatchmakingHandler.remove_player(user)

        ServerGlobals.CONNECTION_LINKS.remove(user)
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
