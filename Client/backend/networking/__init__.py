import socket

import backend.handler
from backend.shared import PacketListener


class ServerConnection:
    def __init__(self, ip, port):
        self.client_socket = socket.socket()
        self.ip = ip
        self.port = port
        self.connected = False
        self.error = False
        self.state = ""
        self.packet_listeners: list[PacketListener] = []

    def connect(self):
        try:
            self.state = "Stelle Verbindung mit Server her"
            self.error = False
            self.connected = False
            self.client_socket = socket.socket()
            self.client_socket.connect((self.ip, self.port))
            self.state = "Verbunden, warte auf Austausch"
            self.connected = True
            self.client_socket.sendall("1".encode())
            return True, "Connected"
        except socket.error as msg:
            self.state = "Der Verbindungsaufbau ist fehlgeschlagen"
            self.error = True
            self.stop()
            return False, str(msg)

    def trigger_packet_listener(self, packet_id: int):
        for i in self.packet_listeners:
            i.on_paket_reveived(packet_id=packet_id)

    def listen(self):
        while True:
            try:
                paket_id = self.client_socket.recv(1024).decode()
                self.trigger_packet_listener(int(paket_id))
                print("[Networking] Packet erhalten mit ID", paket_id)

            except Exception:
                # Set to loading screen
                backend.shared.HandlerGlobals.SCREEN_HANDLER.current_screen = 0
                self.state = "Problem bei der Datenübertragung!"
                self.error = True
                self.stop()
                break

    def stop(self):
        self.connected = False
        self.client_socket.close()
