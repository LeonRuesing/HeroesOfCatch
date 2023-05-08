from math import sqrt

from pygame.color import lerp

import backend.shared
from backend.supers import Character, TextButton
from foundation import pygame
from backend.shared import ProjectGlobals
from backend.shared import HandlerGlobals


class HeroSelection:
    def __init__(self, path):
        self.hero_img = ProjectGlobals.load_image(path)
        self.background = ProjectGlobals.load_image("hero_select_hero_bg")
        self.selected_background = ProjectGlobals.load_image("hero_select_hero_selected_bg")
        self.selected = False

class LobbyScreen:

    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background")

        self.profile = ProjectGlobals.load_image("profile_background")

        self.profile_rect = self.profile.get_rect()
        self.profile_rect.left = 10
        self.profile_rect.top = 10

        self.profile_level = ProjectGlobals.load_image("profile_level_background")

        self.profile_level_rect = self.profile_level.get_rect()
        self.profile_level_rect.left = self.profile_rect.left + 10
        self.profile_level_rect.centery = self.profile_rect.centery

        self.font = pygame.font.Font(pygame.font.get_default_font(), 22)

        self.hero_select = True
        self.hero_select_bg = ProjectGlobals.load_image("hero_select_bg")
        self.hero_select_hero_bg = ProjectGlobals.load_image("hero_select_hero_bg")


        texture = ProjectGlobals.load_image("button_play")
        self.play_button_rect = texture.get_rect()
        self.play_button_rect.center = ProjectGlobals.SCREEN_RECT.center
        self.play_button = TextButton(texture, self.play_button_rect, "Spielen")

        texture = ProjectGlobals.load_image("button_change_hero")
        self.change_hero_button_rect = texture.get_rect()
        self.change_hero_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.change_hero_button_rect.top = self.play_button_rect.bottom + 10
        self.change_hero_button = TextButton(texture, self.change_hero_button_rect, "Held wechseln")

        texture = ProjectGlobals.load_image("button_red")
        self.close_button_rect = texture.get_rect()
        self.close_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.close_button_rect.top = self.change_hero_button_rect.bottom + 10
        self.close_button = TextButton(texture, self.close_button_rect, "Spiel beenden")

        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.play_button)
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.change_hero_button)
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.close_button)

        # TODO: Starke Cleanup-Baustelle!
        self.heroes = [HeroSelection("/heroes/digla/idle/idle_0"), HeroSelection("/heroes/rageo/idle"),
                       HeroSelection("/heroes/vaaslen/idle")]

        pass

    def draw(self, screen, dt):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)
        self.play_button.render(screen)
        self.change_hero_button.render(screen)
        self.close_button.render(screen)

        #screen.blit(self.profile, self.profile_rect)

        #self.profile_level.get_rect().centery = self.profile_rect.centery

        #screen.blit(self.profile_level, self.profile_level_rect)

        #text = backend.shared.HandlerGlobals.LOGIN_HANDLER.username

        #basic_surface = self.font.render(text, True, (255, 255, 255))

        #text_rect = basic_surface.get_rect()
        #text_rect.centery = self.profile_rect.centery
        #text_rect.left = self.profile_level_rect.left + 10

        #screen.blit(basic_surface, text_rect)

        #if self.hero_select:
        #    rect = self.hero_select_bg.get_rect()
         #   rect.center = ProjectGlobals.SCREEN_RECT.center

            # Background
            #screen.blit(self.hero_select_bg, rect)

    def update(self, dt):
        pass


class IngameScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("ingame_grass_background")

    def draw(self, screen, dt):
        screen.blit(self.background, (0, 0))

        for i in HandlerGlobals.INGAME_ENTITY_HANDLER.entities:
            # screen.blit(self.entities[i.hero_id], (i.x, i.y))
            i.draw(screen)
            i.update(dt)

    def update(self, dt):
        pass
