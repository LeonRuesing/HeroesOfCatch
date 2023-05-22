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
        except:
            print('connection error')

    # Override
    def on_packet_received(self, packet_id: int, data: str):
        # Login request
        if packet_id == 0:
            HandlerGlobals.SERVER_CONNECTION.state = "Kommunikation mit Server erfolgreich, Anmelden..."

            username = f'username{random.randint(0, 1_000_000)}'
            HandlerGlobals.SERVER_CONNECTION.client_socket.sendall(f'1;{username};abc'.encode())
        # Server approve login
        elif packet_id == 1:
            HandlerGlobals.SCREEN_HANDLER.set_screen(1)
            backend.shared.HandlerGlobals.LOGIN_HANDLER.username = data[1]


class MatchmakingController(PacketListener):
    def __init__(self):
        HandlerGlobals.SERVER_CONNECTION.packet_listeners.append(self)

        self.present_players = 0
        self.needed_players = 0

    def on_packet_received(self, packet_id: int, data: list[str]):
        # Enter matchmaking
        if packet_id == 4:
            self.needed_players = int(data[1])
            HandlerGlobals.SCREEN_HANDLER.set_screen(3)
        # Leave matchmaking
        elif packet_id == 5:
            HandlerGlobals.SCREEN_HANDLER.set_screen(1)
        # Update matchmaking
        elif packet_id == 6:
            self.present_players = int(data[1])

    @staticmethod
    def send_matchmaking_request():
        if HandlerGlobals.SERVER_CONNECTION.connected:
            HandlerGlobals.SERVER_CONNECTION.client_socket.sendall(
                f'3;{HandlerGlobals.HERO_HANDLER.selected_hero}'.encode())

    @staticmethod
    def send_queue_cancel():
        if HandlerGlobals.SERVER_CONNECTION.connected:
            HandlerGlobals.SERVER_CONNECTION.client_socket.sendall('4'.encode())


class RoundResultScreenController(PacketListener):
    def __init__(self):
        HandlerGlobals.SERVER_CONNECTION.packet_listeners.append(self)

        self.heroes_win = 0

    def on_packet_received(self, packet_id: int, data: list[str]):
        # Round result
        if packet_id == 11:
            HandlerGlobals.SCREEN_HANDLER.set_screen(4)
            self.heroes_win = int(data[1])


class IngameScreenController(PacketListener):
    def __init__(self):
        HandlerGlobals.SERVER_CONNECTION.packet_listeners.append(self)

        self.seconds_left = 0

    def on_packet_received(self, packet_id: int, data: str):
        # Round transfer
        if packet_id == 2:
            HandlerGlobals.IN_GAME_ENTITY_HANDLER.entities.clear()
            HandlerGlobals.SCREEN_HANDLER.set_screen(2)

            self.seconds_left = 60

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

                    hero = HeroHandler.build_hero(hero_id, id, username)
                    hero.x = x
                    hero.y = y
                    hero.sync_pos_with_server()

                    HandlerGlobals.IN_GAME_ENTITY_HANDLER.entities.append(hero)

                    if hero.username == backend.shared.HandlerGlobals.LOGIN_HANDLER.username:
                        backend.shared.HandlerGlobals.MOVEMENT_HANDLER.set_player(hero)
                else:
                    hunter = Bob(id, username)
                    hunter.x = x
                    hunter.y = y
                    hunter.sync_pos_with_server()

                    HandlerGlobals.IN_GAME_ENTITY_HANDLER.entities.append(hunter)

                    if hunter.username == backend.shared.HandlerGlobals.LOGIN_HANDLER.username:
                        backend.shared.HandlerGlobals.MOVEMENT_HANDLER.set_player(hunter)

        # Pos update
        elif packet_id == 3:
            index = 1

            while index + 3 <= len(data):
                id = int(data[index])
                index += 1
                x = float(data[index])
                index += 1
                y = float(data[index])
                index += 1

                hero = HandlerGlobals.IN_GAME_ENTITY_HANDLER.get_entity_by_id(id)

                if hero is not None:
                    hero.x = x
                    hero.y = y
        # Effect triggered
        elif packet_id == 7:
            id = int(data[1])
            effect_name = data[2]
            effective_speed = float(data[3])

            for i in HandlerGlobals.IN_GAME_ENTITY_HANDLER.entities:
                if effect_name == 'Freeze':
                    if i.id == id and type(i) == Bob:
                        i.freeze = True
                        i.interpolation_speed = effective_speed
                elif effect_name == 'Shield':
                    if i.id == id:
                        i.shield = True
        # Effect cleared
        elif packet_id == 8:
            id = int(data[1])
            effect = data[2]
            entity = HandlerGlobals.IN_GAME_ENTITY_HANDLER.get_entity_by_id(id)
            if entity is not None:
                entity.interpolation_speed = entity.orig_interpolation_speed

                if effect == 'Freeze':
                    if entity.id == id:
                        entity.freeze = False
                elif effect == 'Shield':
                    entity.shield = False
        # Hero hunted
        elif packet_id == 9:
            id = int(data[1])
            entity = HandlerGlobals.IN_GAME_ENTITY_HANDLER.get_entity_by_id(id)
            if entity is not None:
                entity.hunted = True
        # Timer update
        elif packet_id == 10:
            self.seconds_left = int(data[1])
