import socket


class DisconnectListener:
    def on_disconnect(self, client_connection: object):
        pass


class ClientConnection:
    def __init__(self, client_socket: socket.socket, client_ip: str, disconnect_listener: DisconnectListener):
        self.socket = client_socket
        self.client_ip = client_ip
        self.disconnect_listener = disconnect_listener


class UserConnectionLink:
    def __init__(self, socket: socket.socket, username: str):
        self.socket = socket
        self.username = username


class PlayerCharacter:
    def __init__(self, username, x, y):
        self.username = username
        self.x = x
        self.y = y

class Round:
    def __init__(self):
        self.users: list[UserConnectionLink] = []
