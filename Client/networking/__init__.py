import socket


class ServerConnection:
    def __init__(self, ip, port):
        self.client_socket = socket.socket()
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            self.client_socket.connect((self.ip, self.port))
            return True, "Connected"
        except socket.error as msg:
            return False, str(msg)
