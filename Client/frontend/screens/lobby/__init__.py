import backend.shared
from foundation import pygame
from backend.shared import ProjectGlobals


class LobbyScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background").convert()
        self.background = pygame.transform.scale(self.background, ProjectGlobals.SCREEN_RECT.size)

        self.font = pygame.font.Font(pygame.font.get_default_font(), 22)
        pass

    def draw(self, screen):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

        text = backend.shared.HandlerGlobals.LOGIN_HANDLER.username

        basic_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.left = ProjectGlobals.SCREEN_RECT.left + 25
        text_rect.top = ProjectGlobals.SCREEN_RECT.top + 25

        screen.blit(basic_surface, text_rect)
        pass

    def update(self):
        pass