import threading

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
    def on_paket_reveived(self, packet_id: int):
        if packet_id == 0:
            HandlerGlobals.SERVER_CONNECTION.state = "Kommunikation mit Server erfolgreich, Anmelden..."
            print(packet_id)
            pass
