import time
from socket import socket

import pygame.event

import backend.shared
from backend.entities import Rageo, Digla, Vaaslen, Bob
from backend.supers import Character
from frontend.supers import TextButton


class ScreenHandler:
    def __init__(self):
        self.__current_screen = 0

    def set_screen(self, screen_id):
        self.__current_screen = screen_id

    def get_screen(self):
        return self.__current_screen


class LoginHandler:
    def __init__(self):
        self.username = None


class ButtonHandler:
    def __init__(self):
        self.active_buttons = list[TextButton]()

    def update_hover(self, pos: tuple[int, int]):
        for i in self.active_buttons:
            if i.rect.collidepoint(pos):
                i.hover = True
            else:
                i.hover = False

    def update_press(self):
        for i in self.active_buttons:
            if i.hover:
                i.pressed = True


class IngameEntityHandler:
    def __init__(self):
        self.entities = list[Character]()

    def get_entity_by_id(self, id) -> Character:
        for i in self.entities:
            if i.id == id:
                return i
        return None


class HeroHandler:
    def __init__(self):
        self.heroes = {0: Digla, 1: Vaaslen}
        self.selected_hero = 0

    @staticmethod
    def build_hero(hero_id, id, username):
        hero = None
        if hero_id == 0:
            hero = Digla(id, username)
        elif hero_id == 1:
            hero = Vaaslen(id, username)
        return hero


class MovementHandler:
    def __init__(self):
        self.movement = [0, 0, 0, 0]  # LEFT, RIGHT, TOP, BOTTOM

        self.__player_hero: Character = None

    def set_player(self, player_hero: Character):
        self.__player_hero = player_hero

    def get_player(self) -> Character:
        return self.__player_hero

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

        # Ability
        if key == pygame.K_SPACE:
            if self.__player_hero is not None:
                if self.__player_hero.ability.available:
                    self.__player_hero.ability.last_used = time.time_ns()
                    self.send_ability()

        self.send_update()

    # TODO: Game crash after disconnect
    def send_update(self):
        if backend.shared.HandlerGlobals.SERVER_CONNECTION.connected:
            print(f'{self.movement[0]}')
            backend.shared.HandlerGlobals.SERVER_CONNECTION.client_socket.sendall(
                f'2;{self.movement[0]};{self.movement[1]};{self.movement[2]};{self.movement[3]}'.encode())

    @staticmethod
    def send_ability():
        if backend.shared.HandlerGlobals.SERVER_CONNECTION.connected:
            backend.shared.HandlerGlobals.SERVER_CONNECTION.client_socket.sendall('5'.encode())
