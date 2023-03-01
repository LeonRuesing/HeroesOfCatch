import backend.shared
from foundation import pygame
from backend.shared import ProjectGlobals
from backend.shared import HandlerGlobals


class LobbyScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background").convert()

        self.profile = ProjectGlobals.load_image("profile_background").convert()

        self.profile_rect = self.profile.get_rect()
        self.profile_rect.left = 10
        self.profile_rect.top = 10

        self.profile_level = ProjectGlobals.load_image("profile_level_background").convert_alpha()

        self.profile_level_rect = self.profile_level.get_rect()
        self.profile_level_rect.left = self.profile_rect.left + 10
        self.profile_level_rect.centery = self.profile_rect.centery

        self.font = pygame.font.Font(pygame.font.get_default_font(), 22)
        pass

    def draw(self, screen):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

        screen.blit(self.profile, self.profile_rect)

        self.profile_level.get_rect().centery = self.profile_rect.centery

        # screen.blit(self.profile_level, self.profile_level_rect)

        text = backend.shared.HandlerGlobals.LOGIN_HANDLER.username

        basic_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.centery = self.profile_rect.centery
        text_rect.left = self.profile_level_rect.right + 15

        screen.blit(basic_surface, text_rect)
        pass

    def update(self):
        pass


class IngameScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("ingame_grass_background")
        self.hero_test = ProjectGlobals.load_image("test")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for i in HandlerGlobals.INGAME_ENTITY_HANDLER.entities:
            screen.blit(self.hero_test, (i.x, i.y))

    def update(self):
        pass
