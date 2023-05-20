import pygame

from backend.shared import ProjectGlobals, HandlerGlobals, ControllerGlobals
from frontend.supers import TextButton


def send_matchmaking_request():
    if HandlerGlobals.SERVER_CONNECTION.connected:
        HandlerGlobals.SERVER_CONNECTION.client_socket.sendall('3'.encode())


class RoundResultScreen:

    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background")

        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.sub_font = pygame.font.Font(pygame.font.get_default_font(), 22)

        texture = ProjectGlobals.load_image("button_red")
        self.close_button_rect = texture.get_rect()
        self.close_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.close_button_rect.bottom = ProjectGlobals.SCREEN_RECT.bottom - 50
        self.close_button = TextButton(texture, self.close_button_rect, "Zurück")

        texture = ProjectGlobals.load_image("button_green")
        self.play_button_rect = texture.get_rect()
        self.play_button_rect.bottom = self.close_button_rect.top - 10
        self.play_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.play_button = TextButton(texture, self.play_button_rect, "Nochmal spielen")

    def draw(self, screen, dt):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

        if ControllerGlobals.ROUND_RESULT_SCREEN_CONTROLLER.heroes_win:
            text = "Die Helden haben gewonnen!"
            subtext = "Mindestens ein Held wurde nicht gefangen"
        else:
            text = "Der Hunter hat gewonnen!"
            subtext = "Alle Helden wurden gefangen"

        text_surface = self.font.render(text, True, (255, 255, 255))

        text_surface_rect = text_surface.get_rect()
        text_surface_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        text_surface_rect.top = ProjectGlobals.SCREEN_RECT.top + 50

        screen.blit(text_surface, text_surface_rect)

        sub_text_surface = self.sub_font.render(subtext, True, (255, 255, 255))

        sub_text_surface_rect = sub_text_surface.get_rect()
        sub_text_surface_rect.top = text_surface_rect.bottom + 5
        sub_text_surface_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx

        screen.blit(sub_text_surface, sub_text_surface_rect)

        self.play_button.render(screen)
        self.close_button.render(screen)

    def update(self, dt):
        if self.play_button.pressed:
            send_matchmaking_request()
            self.play_button.pressed = False

        if self.close_button.pressed:
            HandlerGlobals.SCREEN_HANDLER.set_screen(1)
            self.close_button.pressed = False

    def show(self):
        HandlerGlobals.BUTTON_HANDLER.active_buttons.clear()
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.play_button)
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.close_button)
