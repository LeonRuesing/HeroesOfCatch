import threading
import random

import backend.shared
from backend.shared import PacketListener, HandlerGlobals


class LoadingScreenController(PacketListener):

    def __init__(self):
        HandlerGlobals.SERVER_CONNECTION.packet_listeners.append(self)

    def connect(self):
        try:
            connected, error = HandlerGlobals.SERVER_CONNECTION.connect()

            if not connected:
                return

            threading.Thread(target=HandlerGlobals.SERVER_CONNECTION.listen).start()
        except:
            print('connection error')

    # Override
    def on_packet_reveived(self, packet_id: int, data: str):
        if packet_id == 0:
            HandlerGlobals.SERVER_CONNECTION.state = "Kommunikation mit Server erfolgreich, Anmelden..."

            username = f'username{random.randint(0, 1_000_000)}'
            HandlerGlobals.SERVER_CONNECTION.client_socket.sendall(f'1;{username};abc'.encode())
            print(f"Anmelden mit {username}")
            print(packet_id)
        elif packet_id == 1:
            HandlerGlobals.SCREEN_HANDLER.current_screen = 1
            backend.shared.HandlerGlobals.LOGIN_HANDLER.username = data[1]
            print("Angemeldet mit: " + data[1])
