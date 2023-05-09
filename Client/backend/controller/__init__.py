import threading
import random

import backend.supers
import backend.shared
from backend.handler import HeroHandler
from backend.entities import Rageo, Digla, Vaaslen, Bob
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
            # HandlerGlobals.SERVER_CONNECTION.listen()
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
            HandlerGlobals.SCREEN_HANDLER.set_screen(1)
            backend.shared.HandlerGlobals.LOGIN_HANDLER.username = data[1]
            print("Angemeldet mit: " + data[1])


class MatchmakingController(PacketListener):
    def __init__(self):
        HandlerGlobals.SERVER_CONNECTION.packet_listeners.append(self)

        self.present_players = 0
        self.needed_players = 0

    def on_packet_reveived(self, packet_id: int, data: list[str]):
        # Enter matchmaking
        if packet_id == 4:
            self.needed_players = int(data[1])
            HandlerGlobals.SCREEN_HANDLER.set_screen(3)
        elif packet_id == 5:
            HandlerGlobals.SCREEN_HANDLER.set_screen(1)
        elif packet_id == 6:
            self.present_players = int(data[1])

    @staticmethod
    def send_matchmaking_request():
        if HandlerGlobals.SERVER_CONNECTION.connected:
            HandlerGlobals.SERVER_CONNECTION.client_socket.sendall('3'.encode())

    @staticmethod
    def send_queue_cancel():
        if HandlerGlobals.SERVER_CONNECTION.connected:
            HandlerGlobals.SERVER_CONNECTION.client_socket.sendall('4'.encode())


class IngameScreenController(PacketListener):
    def __init__(self):
        HandlerGlobals.SERVER_CONNECTION.packet_listeners.append(self)

    def on_packet_reveived(self, packet_id: int, data: str):
        # print('packet_id', packet_id)
        if packet_id == 2:
            print("Transfer= " + str(data))
            HandlerGlobals.INGAME_ENTITY_HANDLER.entities.clear()
            HandlerGlobals.SCREEN_HANDLER.set_screen(2)
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
                character_type = int(data[index])
                index += 1
                # Hero = 0
                # Hunter = 1
                if character_type == 0:
                    hero_id = int(data[index])
                    index += 1

                    hero = backend.supers.Hero(id, username)
                    hero.x = x
                    hero.y = y
                    hero.sync_pos_with_server()
                    # hero.__class__ = type(HandlerGlobals.HERO_HANDLER.entities[hero_id])
                    if hero_id == 0:
                        hero = Rageo(id, username)
                    elif hero_id == 1:
                        hero = Digla(id, username)
                    elif hero_id == 2:
                        hero = Vaaslen(id, username)

                    HandlerGlobals.INGAME_ENTITY_HANDLER.entities.append(hero)

                    if hero.username == backend.shared.HandlerGlobals.LOGIN_HANDLER.username:
                        backend.shared.HandlerGlobals.MOVEMENT_HANDLER.set_player(hero)
                else:
                    hunter = Bob(id, username)
                    hunter.x = x
                    hunter.y = y
                    hunter.sync_pos_with_server()

                    HandlerGlobals.INGAME_ENTITY_HANDLER.entities.append(hunter)

                    if hunter.username == backend.shared.HandlerGlobals.LOGIN_HANDLER.username:
                        backend.shared.HandlerGlobals.MOVEMENT_HANDLER.set_player(hunter)

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
