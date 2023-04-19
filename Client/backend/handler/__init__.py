from socket import socket

import pygame.event

import backend.shared
from backend.supers import Hero


class ScreenHandler:
    def __init__(self):
        self.current_screen = 0


class LoginHandler:
    def __init__(self):
        self.username = None


class IngameEntityHandler:
    def __init__(self):
        self.entities = list[Hero]()

    def get_entity_by_id(self, id) -> Hero:
        for i in self.entities:
            if i.id == id:
                return i
        return None


class MovementHandler:
    def __init__(self):
        self.movement = [0, 0, 0, 0]  # LEFT, RIGHT, TOP, BOTTOM

        self.__player_hero = None

    def set_player(self, player_hero: Hero):
        self.__player_hero = player_hero

    def check_keyboard_input(self, event: pygame.event.Event, active):
        key = event.key

        if key == pygame.K_LEFT or key == pygame.K_a:
            self.movement[0] = active

        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.movement[1] = active

        if key == pygame.K_UP or key == pygame.K_w:
            self.movement[2] = active

        if key == pygame.K_DOWN or key == pygame.K_s:
            self.movement[3] = active

        self.send_update()

    #TODO: Game crash after disconnect
    def send_update(self):
        if backend.shared.HandlerGlobals.SERVER_CONNECTION.connected:
            print(f'{self.movement[0]}')
            backend.shared.HandlerGlobals.SERVER_CONNECTION.client_socket.sendall(
                f'2;{self.movement[0]};{self.movement[1]};{self.movement[2]};{self.movement[3]}'.encode())
