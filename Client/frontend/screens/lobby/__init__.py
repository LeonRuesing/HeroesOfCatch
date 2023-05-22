import sys
from math import sqrt

from pygame.color import lerp

import backend.shared
from backend.supers import Character
from frontend.supers import TextButton
from foundation import pygame
from backend.shared import ProjectGlobals
from backend.shared import HandlerGlobals


def send_matchmaking_request():
    if HandlerGlobals.SERVER_CONNECTION.connected:
        HandlerGlobals.SERVER_CONNECTION.client_socket.sendall('3'.encode())


class LobbyScreen:

    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background")

        self.font = pygame.font.Font(pygame.font.get_default_font(), 22)

        texture = ProjectGlobals.load_image("button_green")
        self.play_button_rect = texture.get_rect()
        self.play_button_rect.top = 170
        self.play_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.play_button = TextButton(texture, self.play_button_rect, "Spielen")

        texture = ProjectGlobals.load_image("button_orange")
        self.change_hero_button_rect = texture.get_rect()
        self.change_hero_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.change_hero_button_rect.top = self.play_button_rect.bottom + 10
        self.change_hero_button = TextButton(texture, self.change_hero_button_rect, "Held wechseln")

        texture = ProjectGlobals.load_image("button_red")
        self.close_button_rect = texture.get_rect()
        self.close_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.close_button_rect.top = self.change_hero_button_rect.bottom + 10
        self.close_button = TextButton(texture, self.close_button_rect, "Spiel beenden")

    def draw(self, screen, dt):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)
        self.play_button.render(screen)
        self.change_hero_button.render(screen)
        self.close_button.render(screen)

    def update(self, dt):
        if self.play_button.pressed:
            send_matchmaking_request()
            self.play_button.pressed = False

        if self.change_hero_button.pressed:
            HandlerGlobals.SCREEN_HANDLER.set_screen(5)
            self.change_hero_button.pressed = False

        if self.close_button.pressed:
            ProjectGlobals.RUNNING = False
            self.close_button.pressed = False

    def show(self):
        HandlerGlobals.BUTTON_HANDLER.active_buttons.clear()
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.play_button)
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.change_hero_button)
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.close_button)


