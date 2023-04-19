import threading
import random

import backend.supers
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
            #HandlerGlobals.SERVER_CONNECTION.listen()
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


class IngameScreenController(PacketListener):
    def __init__(self):
        HandlerGlobals.SERVER_CONNECTION.packet_listeners.append(self)

    def on_packet_reveived(self, packet_id: int, data: str):
        #print('packet_id', packet_id)
        if packet_id == 2:
            print("Transfer= " + str(data))
            HandlerGlobals.SCREEN_HANDLER.current_screen = 2
            index = 1

            while index + 4 <= len(data):
                id = int(data[index])
                index += 1
                username = data[index]
                index += 1
                x = int(data[index])
                index += 1
                y = int(data[index])
                index += 1

                print(f'{id} {username}, {x}, {y}')

                hero = backend.supers.Hero(id, username)
                hero.x = x
                hero.y = y
                hero.hero_id = random.randint(0, 2)

                HandlerGlobals.INGAME_ENTITY_HANDLER.entities.append(hero)

                if hero.username == backend.shared.HandlerGlobals.LOGIN_HANDLER.username:
                    backend.shared.HandlerGlobals.MOVEMENT_HANDLER.set_player(hero)

        elif packet_id == 3:
            index = 1

            while index + 3 <= len(data):
                id = int(data[index])
                index += 1
                x = float(data[index])
                index += 1
                y = float(data[index])
                index += 1

                hero = HandlerGlobals.INGAME_ENTITY_HANDLER.get_entity_by_id(id)

                if hero is not None:
                    hero.x = x
                    hero.y = y
