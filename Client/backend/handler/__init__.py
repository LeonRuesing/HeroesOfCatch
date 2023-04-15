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
        print(str(key) + " " + str(active))
        print(f'{key} {pygame.K_LEFT}')
        if key == pygame.K_LEFT:
            self.movement[0] = active

        if key == pygame.K_RIGHT:
            self.movement[1] = active

        if key == pygame.K_UP:
            self.movement[2] = active

        if key == pygame.K_DOWN:
            self.movement[3] = active

        print(str(key) + " " + str(active))

        self.send_update()

    def update(self):
        if self.__player_hero is None:
            return

        if self.movement[0]:
            self.__player_hero.x -= 1
        elif self.movement[1]:
            self.__player_hero.x += 1

        if self.movement[2]:
            self.__player_hero.y -= 1
        elif self.movement[3]:
            self.__player_hero.y += 1

    def send_update(self):
        print(f'{self.movement[0]}')
        backend.shared.HandlerGlobals.SERVER_CONNECTION.client_socket.sendall(
            f'2;{self.movement[0]};{self.movement[1]};{self.movement[2]};{self.movement[3]}'.encode())
