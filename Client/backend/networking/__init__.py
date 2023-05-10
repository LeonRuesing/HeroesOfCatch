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
            self.client_socket.close()
            self.state = "Stelle Verbindung mit Server her"
            self.error = False
            self.connected = False
            self.client_socket = socket.socket()
            self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.client_socket.connect((self.ip, self.port))
            self.connected = True
            self.state = "Verbunden, warte auf Kommunikation"
            return True, "Connected"
        except socket.error as msg:
            self.state = "Der Verbindungsaufbau ist fehlgeschlagen"
            self.error = True
            self.stop()
            return False, str(msg)

    def trigger_packet_listener(self, packet_id: int, data: list[str]):
        for i in self.packet_listeners:
            i.on_packet_reveived(packet_id=packet_id, data=data)

    def listen(self):
        while True:
            try:
                raw = str(self.client_socket.recv(1024).decode())
                data = raw.split(";")
                packet_id = int(data[0])

                self.trigger_packet_listener(packet_id, data)
                #print("[Networking] Packet erhalten mit ID", packet_id)

            except Exception as msg:
                # Set to loading screen
                backend.shared.HandlerGlobals.SCREEN_HANDLER.current_screen = 0
                self.state = "Problem bei der Datenübertragung!"
                print(msg)
                self.error = True
                self.stop()
                break
        print('End of method')
        backend.shared.HandlerGlobals.SCREEN_HANDLER.current_screen = 0
        self.state = "Problem bei der Datenübertragung!"
        self.error = True

    def stop(self):
        self.connected = False
        self.client_socket.close()
