import time

import pygame

from backend.shared import ProjectGlobals, HandlerGlobals


class AbilityUI:
    def __init__(self):
        self.ability = None

        self.ability_background = ProjectGlobals.load_image("ability_background")
        self.ability_available_background = ProjectGlobals.load_image("ability_available_background")

        self.ability_timer_background = ProjectGlobals.load_image("ability_timer_background")

        self.main_rect = self.ability_background.get_rect()
        self.main_rect.right = ProjectGlobals.SCREEN_RECT.right - 25
        self.main_rect.bottom = ProjectGlobals.SCREEN_RECT.bottom - 25

        self.time = 0

        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)

    def draw(self, screen, dt):
        if not self.ability.available:
            screen.blit(self.ability_background, self.main_rect)
        else:
            screen.blit(self.ability_available_background, self.main_rect)

        if self.ability is not None:
            rect = self.ability.texture.get_rect()

            rect.centerx = self.main_rect.centerx
            rect.top = self.main_rect.top + 10

            screen.blit(self.ability.texture, rect)

        rect = self.ability_timer_background.get_rect()

        rect.centerx = self.main_rect.centerx
        rect.bottom = self.main_rect.bottom - 10

        screen.blit(self.ability_timer_background, rect)

        if not self.ability.available:
            text = str(self.time) + " Sek."
        else:
            text = "SPACE"
        basic_surface = self.font.render(text, True, (128, 90, 40))

        text_rect = basic_surface.get_rect()
        text_rect.center = rect.center

        screen.blit(basic_surface, text_rect)

    def update(self):
        if self.ability is not None:
            time_for_next_use = self.ability.last_used + (self.ability.time * 1_000_000_000)
            now = time.time_ns()

            time_left = (time_for_next_use - now) / 1_000_000_000

            self.time = round(time_left, 1)

            if time_left <= 0:
                self.ability.available = True
            else:
                self.ability.available = False


class IngameScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("ingame_grass_background")

        self.ability_ui = AbilityUI()

    def draw(self, screen, dt):
        screen.blit(self.background, (0, 0))

        for i in HandlerGlobals.INGAME_ENTITY_HANDLER.entities:
            # screen.blit(self.entities[i.hero_id], (i.x, i.y))
            if not i.hunted:
                i.draw(screen)
                i.update(dt)

        if HandlerGlobals.MOVEMENT_HANDLER.get_player() is not None:
            ability = HandlerGlobals.MOVEMENT_HANDLER.get_player().ability
            if ability is not None:
                self.ability_ui.ability = HandlerGlobals.MOVEMENT_HANDLER.get_player().ability
                self.ability_ui.draw(screen, dt)

    def update(self, dt):
        self.ability_ui.update()

    def show(self):
        pass

