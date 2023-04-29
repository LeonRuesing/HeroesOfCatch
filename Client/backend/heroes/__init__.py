import pygame

from backend.shared import ProjectGlobals
from backend.supers import Hero


class Rageo(Hero):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.idle_texture = ProjectGlobals.load_image("/heroes/rageo/idle")

    def update(self, dt):
        super().update(dt)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.idle_texture, (self.interpolation_x, self.interpolation_y))


class Digla(Hero):

    IDLE_SPRITES = []
    WALKING_SPRITES = []

    def __init__(self, id: int, username):
        super().__init__(id, username)

        for i in range(12):
            Digla.IDLE_SPRITES.append(ProjectGlobals.load_image(f"/heroes/digla/idle/idle_{i}"))

        for i in range(37):
            Digla.WALKING_SPRITES.append(ProjectGlobals.load_image(f"/heroes/digla/walking/walking_{i}"))

        self.current_walking_index = 0
        self.current_idle_index = 0
        self.walking = False


    def update(self, dt):
        if self.walking:
            self.current_walking_index += 1
            if self.current_walking_index >= len(Digla.WALKING_SPRITES):
                self.current_walking_index = 0
        else:
            self.current_idle_index += 1
            if self.current_idle_index >= len(Digla.IDLE_SPRITES):
                self.current_idle_index = 0

        self.walking = self.interpolation_x != self.x or self.interpolation_y != self.y

        super().update(dt)

    def draw(self, screen: pygame.Surface):
        if self.walking:
            screen.blit(Digla.WALKING_SPRITES[self.current_walking_index], (self.interpolation_x, self.interpolation_y))
        else:
            screen.blit(Digla.IDLE_SPRITES[self.current_idle_index], (self.interpolation_x, self.interpolation_y))



class Vaaslen(Hero):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.idle_texture = ProjectGlobals.load_image("/heroes/vaaslen/idle")

    def update(self, dt):
        super().update(dt)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.idle_texture, (self.interpolation_x, self.interpolation_y))