import socket
import threading
import time
import random


class DisconnectListener:
    def on_disconnect(self, client_connection: object):
        pass


class PlayerCharacter:
    def __init__(self, username, x, y):
        self.username = username
        self.x = x
        self.y = y

class ServerGlobals:
    connections = []
    player_character = list[PlayerCharacter]()


class DataHandler:
    def __init__(self):
        pass

    @staticmethod
    def send_to_all(data: bytes):
        for connection in ServerGlobals.connections:
            connection.socket.sendall(data)

    @staticmethod
    def send_character_add(player_character: PlayerCharacter):
        DataHandler.send_to_all(f'2;{player_character.username};{player_character.x};{player_character.y}'.encode())

    @staticmethod
    def send_character_transfer(player_character_list: list[PlayerCharacter]):
        data = f'{3}'

        for i in range(len(player_character_list)):
            p = player_character_list[i]
            data += ';' + p.username + ';' + str(p.x) + ';' + str(p.y)

        print('Tranfer', data)
        DataHandler.send_to_all(data.encode())


class PacketListener:

    def listen_for_packets(self, socket: socket.socket):
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
                print(f"Login-Versuch mit '{username},{key}'")
                socket.sendall(f'1;{username}'.encode())

                DataHandler.send_character_transfer(ServerGlobals.player_character)

                player_character = PlayerCharacter(username, random.randint(0, 500), random.randint(0, 500))
                ServerGlobals.player_character.append(player_character)

                # Add player
                DataHandler.send_character_add(player_character)

                print(f'[ClientConnection] Der Client {socket.getpeername()} sendete Paket {paket_id}')


class ClientConnection:
    def __init__(self, client_socket: socket.socket, client_ip: str, disconnect_listener: DisconnectListener):
        self.socket = client_socket
        self.client_ip = client_ip
        self.disconnect_listener = disconnect_listener
        self.packet_listener = PacketListener()
        print(type(client_socket))

    def start(self):
        try:
            self.packet_listener.listen_for_packets(self.socket)
        # Catch every exception
        except Exception as e:
            print('[ClientConnection]', 'Fehler bei der Datenübertragung: ' + str(e))
            self.disconnect_listener.on_disconnect(self)
            self.socket.close()
            return


class ConnectionHandler(DisconnectListener):
    def __init__(self, server_socket: socket):
        # self.connections: list[ClientConnection] = []
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

            ServerGlobals.connections.append(client_connection)

            threading.Thread(target=client_connection.start).start()

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
