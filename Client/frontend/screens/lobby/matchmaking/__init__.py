import pygame

from backend.shared import ProjectGlobals, ControllerGlobals, HandlerGlobals
from frontend.supers import TextButton


class LoadingCircle:
    def __init__(self):
        self.loading_circle = ProjectGlobals.load_image("loading_circle")
        self.loading_circle = pygame.transform.scale(self.loading_circle, (100, 100))
        self.image = self.loading_circle
        self.rect = self.loading_circle.get_rect()
        self.angle = 0

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.loading_circle, self.angle)

        rect = self.image.get_rect()
        rect.center = self.rect.center
        self.rect = rect

    def draw(self, screen, dt):
        self.angle += 4
        self.rotate_image()

        screen.blit(self.image, self.rect)


class MatchmakingScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background")

        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)

        self.loading_circle = LoadingCircle()
        self.loading_circle.rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.loading_circle.rect.centery = ProjectGlobals.SCREEN_RECT.centery

        texture = ProjectGlobals.load_image("button_red")
        self.cancel_button_rect = texture.get_rect()
        self.cancel_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.cancel_button_rect.centery = ProjectGlobals.SCREEN_RECT.centery + 120

        self.cancel_button = TextButton(texture, self.cancel_button_rect, "Abbrechen")

        self.current_players = 0
        self.needed_players = 0

    def draw(self, screen, dt):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

        text = f"Suche nach Spielern"
        basic_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        text_rect.centery = ProjectGlobals.SCREEN_RECT.centery - 150

        screen.blit(basic_surface, text_rect)

        text = f"({ControllerGlobals.MATCHMAKING_CONTROLLER.present_players} / {ControllerGlobals.MATCHMAKING_CONTROLLER.needed_players})"
        basic_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        text_rect.centery = ProjectGlobals.SCREEN_RECT.centery - 120

        screen.blit(basic_surface, text_rect)

        self.loading_circle.draw(screen, dt)

        self.cancel_button.render(screen)

    def update(self, dt):
        if self.cancel_button.pressed:
            ControllerGlobals.MATCHMAKING_CONTROLLER.send_queue_cancel()
            self.cancel_button.pressed = False

        self.cancel_button.update(dt)

    def show(self):
        HandlerGlobals.BUTTON_HANDLER.active_buttons.clear()
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.cancel_button)